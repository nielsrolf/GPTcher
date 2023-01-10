import os

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

from gptcher import bot
from gptcher.main import ConversationState, VocabTrainingState

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
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")
    from gptcher.content.text_to_voice import read_and_save_voice

    voice_url = read_and_save_voice(
        "Hola tio, como estas mi amigo? Toto bien? yo", "Spanish"
    )
    # send voice message
    await context.bot.send_voice(
        chat_id=update.effective_chat.id,
        voice=voice_url,
    )


async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    user_msg = f"{update.effective_user.first_name}: {update.message.text}\n"
    print(user_msg)

    async def reply_func(text):
        print(f"Bot: {text}\n")
        if text.startswith("http"):
            await context.bot.send_voice(
                chat_id=update.effective_chat.id,
                voice=text,
            )
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    await bot.respond(
        str(update.effective_chat.id), update.message.text, reply_func=reply_func
    )


async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="If you like this bot, please consider donating to my patreon: patreon.com/user?u=55105539",
    )


async def start_vocab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async def reply_func(text):
        print(f"Bot: {text}\n")
        if text.startswith("http"):
            await context.bot.send_voice(
                chat_id=update.effective_chat.id,
                voice=text,
            )
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    user = bot.User(str(update.effective_chat.id) + "tmp4", reply_func=reply_func)
    new_conversation = VocabTrainingState(user)
    await user.enter_state(new_conversation)


async def start_converse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async def reply_func(text):
        print(f"Bot: {text}\n")
        if text.startswith("http"):
            await context.bot.send_voice(
                chat_id=update.effective_chat.id,
                voice=text,
            )
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    user = bot.User(str(update.effective_chat.id) + "tmp4", reply_func=reply_func)
    new_conversation = ConversationState(user)
    await user.enter_state(new_conversation)


async def start_exercise_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    async def reply_func(text):
        print(f"Bot: {text}\n")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    await bot.start_exercise(str(update.effective_chat.id), reply_func=reply_func)


if __name__ == "__main__":
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("start", respond))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(CommandHandler("train", start_exercise_conversation))
    app.add_handler(CommandHandler("vocab", start_vocab))
    app.add_handler(CommandHandler("converse", start_converse))

    teach_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), respond)
    app.add_handler(teach_handler)
    app.run_polling()
