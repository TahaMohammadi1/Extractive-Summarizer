from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hi,  Im Extractive summarizer bot. give me a long text and i will summarize it for you. ")





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