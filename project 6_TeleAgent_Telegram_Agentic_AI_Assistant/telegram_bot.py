import logging
from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from agent import run_agent

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("teleagent")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to TeleAgent!\n\n"
        "I am an agentic AI assistant. Send me a question and I will "
        "analyze it, choose a tool/knowledge source when useful, validate the result, "
        "and generate a response.\n\n"
        "Try: explain LangGraph, calculate 25*8, or ask for the current time."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/start — introduction\n"
        "/help — usage help\n\n"
        "Or simply send a normal message."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    try:
        result = run_agent(update.message.text)
        answer = result.get("answer", "I could not generate a response.")
        await update.message.reply_text(answer)
    except Exception as exc:
        logger.exception("Agent failure")
        await update.message.reply_text(
            f"⚠️ The agent could not complete the request.\n{exc}"
        )


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is missing. Create a bot with @BotFather and add the token to .env."
        )

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("TeleAgent Telegram bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
