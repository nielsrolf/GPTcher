import click
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from gptcher import bot
from gptcher.main import ConversationState, WelcomeUser

from gptcher_api.authentication import TokenPayload, get_current_user
from gptcher_api.db_client import supabase
from gptcher_api.schema import Message
from gptcher.settings import is_prod, table_prefix


load_dotenv()


app = FastAPI()


origins = [
    "http://localhost:*",
    "http://localhost:3000",
    "https://gptcher.com",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"healthy": "yes"}


# @app.get("/user")
# async def whoami(user: TokenPayload = Depends(get_current_user)):
#     return user


@app.post("/chat")
async def send_message(
    message: Message, user: TokenPayload = Depends(get_current_user)
) -> List[Message]:
    await user.state.respond(message.text, voice_url=None)
    # get student message and append to the beginning
    student_message = [i for i in user.state.messages if i.sender == 'Student'][-1]
    user.new_messages.insert(0, Message(**student_message.__dict__))
    return user.new_messages


@app.get("/clearchat")
async def send_message(
    user: bot.User = Depends(get_current_user)
) -> List[Message]:
    new_conversation = WelcomeUser(user)
    await user.enter_state(new_conversation)
    return user.new_messages


@app.get("/chat")
async def get_history(
    user: bot.User = Depends(get_current_user)
) -> List[Message]:
    messages = [
        Message(**i.__dict__) for i in user.state.messages
    ]
    if len(messages) == 0:
        await user.state.respond("/start")
        messages = user.new_messages
    return messages


@app.get("/exercises")
async def get_exercises(user: bot.User = Depends(get_current_user)):
    exercises = (
        supabase.table(table_prefix + "exercises")
        .select("*")
        .eq("language", user.language)
        .is_("user_id", 'null')
        .execute()
        .data
    )
    # Get all done exercises
    done_exercises = (
        supabase.table(table_prefix + "finished_exercises")
        .select("*")
        .eq("user_id", user.user_id)
        .execute()
        .data
    )
    


@click.command()
@click.option("--host", default="0.0.0.0", help="Host to listen on")
@click.option("--port", default=5555, help="Port to listen on")
def main(host: str, port: int) -> None:
    """
    Run the server.
    """
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
