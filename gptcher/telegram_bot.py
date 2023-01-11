import os

import banana_dev as banana
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
from gptcher.language_codes import code_of
from gptcher.utils import measure_time, print_times

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


@measure_time
def speech_recognition_api_request(file_url, language_code):
    model_key = "86b4a6b0-425f-4767-9ce9-faf62a0b8ca2"
    banana_api_key = os.environ['BANANA_API_KEY']
    model_payload = {
        "audio": file_url,
        "language": language_code,
    }
    out = banana.run(banana_api_key, model_key, model_payload)
    return out['modelOutputs'][0]['transcription'].strip()


async def speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await context.bot.send_chat_action(
    #     chat_id=update.effective_chat.id, action=ChatAction.SPEAKING
    # )
    # Get the update object and extract the message and file_id
    update = update
    message = update.message
    file_id = message.voice.file_id
    # Use the bot to get the file object
    file = await context.bot.get_file(file_id)

    # Get the user

    async def reply_func(text):
        print(f"Bot: {text}\n")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    user = bot.User(str(update.effective_chat.id) + "tmp4", reply_func=reply_func)
    # Get the text from the audio file
    text = speech_recognition_api_request(file.file_path, code_of[user.language])
    await user.reply(f"Understood: {text}")
    print_times()
    # Reply
    update.message.text = text
    await respond(update, context)


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Available commands:\n"
        "/train - Start an exercise from a list of topics\n"
        "/vocab - Start an exercise created just for you - with the words you are learning\n"
        "/converse - Start an open conversation with the bot\n"
        "/donate - Donate to the bot's patreon\n"
        "/help - Show this message\n",
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("start", respond))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(CommandHandler("train", start_exercise_conversation))
    app.add_handler(CommandHandler("vocab", start_vocab))
    app.add_handler(CommandHandler("converse", start_converse))
    app.add_handler(CommandHandler("help", show_help))

    app.add_handler(MessageHandler(filters.VOICE, speech))

    teach_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), respond)
    app.add_handler(teach_handler)
    app.run_polling()
