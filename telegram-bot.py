import os
import sys
import subprocess
import asyncio 
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

APP_FOLDER = "app"

def summarize_text(text) -> str :
     input_path = os.path.join(APP_FOLDER, "input.txt")
     summary_path = os.path.join(APP_FOLDER, "summary.txt")

     #craete input.txt file
     with open(input_path, "w", encoding="utf-8") as f:
          f.write(text)

     # remove old files of Embedding
     for file_name in ["sentences.json", "embedded.npy"]:
          path = os.path.join(APP_FOLDER, file_name)
          if os.path.exists(path):
               os.remove(path)

     # remove old summary.txt file
     if os.path.exists(summary_path):
          os.remove(summary_path)


     VENV_python = sys.executable

     # run embed_sentences.py
     subprocess.run([VENV_python, os.path.join(APP_FOLDER, "embed_sentences.py"), input_path], check=True)
     subprocess.run([VENV_python, os.path.join(APP_FOLDER, "main.py"), input_path], check = True)

     # read new summary.txt
     with open(summary_path, "r", encoding="utf-8") as f:
          summary = f.read()

     return summary


# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hi,  Im Extractive summarizer bot. Give me a long text and i will summarize it for you. ")


# regular text messages handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
     user_text = update.message.text

     #response
     await update.message.reply_text("َALright, just a moment ...")
     await update.message.reply_text("👾")

     #process

     try:
        summary = await asyncio.to_thread(summarize_text, user_text) 
        await update.message.reply_text(summary)
     except Exception as e:
        error = str(e)
        await update.message.reply_text(f"Error while processing : {error}")


# Run bot
def main():
    token = "insert telegram bot token here" # insert telegram bot token here
    app = ApplicationBuilder().token(token).build()

    # add /start command handler
    app.add_handler(CommandHandler("start", start))
    # add regular text messege handler
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot started ...")
    app.run_polling()


if __name__ == "__main__":
    main()