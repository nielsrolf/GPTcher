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
from gptcher.gpt_client import measure_time, print_times
from gptcher.settings import token


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

    voice_url = None
    if update.message.voice:
        file_id = update.message.voice.file_id
        # Use the bot to get the file object
        file = await context.bot.get_file(file_id)
        voice_url = file.file_path

    async def reply_func(text):
        print(f"Bot: {text}\n")
        if text.startswith("http"):
            await context.bot.send_voice(
                chat_id=update.effective_chat.id,
                voice=text,
            )
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='html')

    await bot.respond(
        str(update.effective_chat.id), update.message.text, voice_url=voice_url, reply_func=reply_func
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
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='html')

    user = bot.User(str(update.effective_chat.id) , reply_func=reply_func)
    new_conversation = VocabTrainingState(user)
    await user.enter_state(new_conversation)


async def start_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async def reply_func(text):
        print(f"Bot: {text}\n")
        if text.startswith("http"):
            await context.bot.send_voice(
                chat_id=update.effective_chat.id,
                voice=text,
            )
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='html')

    user = bot.User(str(update.effective_chat.id) , reply_func=reply_func)
    new_conversation = ConversationState(user)
    await user.enter_state(new_conversation)


async def start_exercise_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    async def reply_func(text):
        print(f"Bot: {text}\n")
        if text.startswith("http"):
            await context.bot.send_voice(
                chat_id=update.effective_chat.id,
                voice=text,
            )
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='html')

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


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Available commands:\n"
        "/train - Start an exercise from a list of topics\n"
        "/vocab - Start an exercise created just for you - with the words you are learning\n"
        "/chat - Start an open conversation with the bot\n"
        "/donate - Donate to the bot's patreon\n"
        "/help - Show this message\n",
    )


async def set_german(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async def reply_func(text):
        print(f"Bot: {text}\n")
        if text.startswith("http"):
            await context.bot.send_voice(
                chat_id=update.effective_chat.id,
                voice=text,
            )
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='html')
    
    await bot.change_language(str(update.effective_chat.id), "German", reply_func=reply_func)


async def set_spanish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async def reply_func(text):
        print(f"Bot: {text}\n")
        if text.startswith("http"):
            await context.bot.send_voice(
                chat_id=update.effective_chat.id,
                voice=text,
            )
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='html')
    
    await bot.change_language(str(update.effective_chat.id), "Spanish", reply_func=reply_func)


if __name__ == "__main__":
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("start", respond))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(CommandHandler("train", start_exercise_conversation))
    app.add_handler(CommandHandler("vocab", start_vocab))
    app.add_handler(CommandHandler("chat", start_chat))
    app.add_handler(CommandHandler("help", show_help))
    app.add_handler(CommandHandler("german", set_german))
    app.add_handler(CommandHandler("deutsch", set_german))
    app.add_handler(CommandHandler("spanish", set_spanish))
    app.add_handler(CommandHandler("espanol", set_spanish))


    app.add_handler(MessageHandler(filters.VOICE, respond))
    teach_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), respond)
    app.add_handler(teach_handler)
    app.run_polling()
