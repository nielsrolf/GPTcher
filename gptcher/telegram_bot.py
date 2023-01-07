import os

from gptcher import bot
from gptcher.main import ConversationState, print_times
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


load_dotenv(override=True)
is_prod = os.getenv("IS_PROD") == "True"
if is_prod:
    print("Running in production mode")
    token = os.getenv("TELEGRAM_TOKEN_PROD")
else:
    print("Running in development mode")
    token = os.getenv("TELEGRAM_TOKEN_DEV")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    import time

    time.sleep(4)
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    user_msg = f"{update.effective_user.first_name}: {update.message.text}\n"
    print(user_msg)

    response = bot.respond(
        str(update.effective_chat.id),
        update.message.text
    ) 
    print(f"AI: {response}\n")
    print_times()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="If you like this bot, please consider donating to my patreon: patreon.com/user?u=55105539",
    )



# async def start_vocab(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     response = start_vocab_trainer(str(update.effective_chat.id))
#     await context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text=response,
#     )



async def start_converse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = bot.User(str(update.effective_chat.id))
    new_conversation = ConversationState(user)
    response = new_conversation.start()
    user.set_state(new_conversation)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("start", respond))
    app.add_handler(CommandHandler("donate", donate))
    # app.add_handler(CommandHandler("train", start_vocab))
    app.add_handler(CommandHandler("converse", start_converse))

    teach_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), respond)
    app.add_handler(teach_handler)
    app.run_polling()
