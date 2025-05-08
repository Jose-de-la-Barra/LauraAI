import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Carga variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")

if not api_key or not telegram_token:
    print("Error: configura OPENAI_API_KEY y TELEGRAM_TOKEN en tu .env.")
    exit(1)

# Inicializa cliente OpenAI
client = OpenAI(api_key=api_key)

# Historial de conversaciones por chat_id
history = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu asistente. Envíame un mensaje.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text

    # Inicializa historial con prompt del sistema si es primera vez
    if chat_id not in history:
        history[chat_id] = [{"role": "system", "content": "Eres un asistente que se llama Laura."}]

    history[chat_id].append({"role": "user", "content": user_text})

    # Llamada a la API de OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history[chat_id]
    )
    assistant_text = response.choices[0].message.content

    history[chat_id].append({"role": "assistant", "content": assistant_text})
    await update.message.reply_text(assistant_text)

def main():
    # Crea y configura el bot de Telegram
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Inicia polling
    print("Bot iniciado. Esperando mensajes...")
    app.run_polling()

if __name__ == "__main__":
    main()
