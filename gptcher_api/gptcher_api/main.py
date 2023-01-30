import click
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Union

from gptcher_api.authentication import TokenPayload, get_current_user


load_dotenv()


app = FastAPI()


class Message(BaseModel):
    text: str
    # user_id: Optional[str] = None
    # sender: Optional[str] = None
    # text_en: Optional[str] = None
    # text_translated: Optional[str] = None
    # voice_url: Optional[str] = None
    # session: Optional[str] = None
    # created_at: Optional[str] = None
    # updated_at: Optional[str] = None
    # id: Optional[Union[str, int]] = None
    # evaluation: Optional[Dict] = None


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


@app.get("/user")
async def whoami(user: TokenPayload = Depends(get_current_user)):
    return user


@app.post("/chat")
async def send_message(
    message: Message, user: TokenPayload = Depends(get_current_user)
) -> List[Message]:
    messages = [
        Message(id=1, text='hi'),
        Message(id=2, text='hello'),
        message
    ]

    return messages


@app.get("/chat")
async def send_message(
    user: TokenPayload = Depends(get_current_user)
) -> List[Message]:
    messages = [
        Message(id=1, text='hi'),
        Message(id=2, text='hello'),
    ]
    return messages


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
