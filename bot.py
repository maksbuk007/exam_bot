from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes
from dotenv import load_dotenv
import os
import threading
import http.server
import socketserver

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PASSWORD = "18579141"  # Пароль для доступа

# Разрешённые Telegram ID (можно добавить несколько)
ALLOWED_IDS = [804816309, 1151301056, 1970302855, 6052484872, 6370543849]  # Замени на свои ID

# Ссылка на мини-приложение
APP_URL = "https://mlogin.ct.ws/"

# Словарь для отслеживания авторизованных пользователей
authorized_users = set()

async def start(update: Update, context: CallbackContext) -> None:
    """Команда /start запрашивает пароль перед доступом."""
    user_id = update.message.from_user.id

    if user_id in authorized_users:
        await send_access(update)
    else:
        await update.message.reply_text("\U0001F511 Введите пароль для доступа:")

async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message

    if user_id in authorized_users:
        return  # Если пользователь уже авторизован, ничего не делаем

    if message.text == PASSWORD:
        authorized_users.add(user_id)
        await send_access(update)
    else:
        await message.reply_text("❌ Неверный пароль. Попробуйте снова.")
    
    try:
        await message.delete()  # Удаляем сообщение с паролем
    except:
        pass  # Игнорируем ошибки, если удаление невозможно

async def send_access(update: Update):
    """Отправляет пользователю доступ к мини-приложению."""
    user_id = update.message.from_user.id
    if user_id in ALLOWED_IDS:
        keyboard = [[InlineKeyboardButton("🚀 Открыть сверхсекретный сайт", web_app=WebAppInfo(url=APP_URL))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("✅ Доступ разрешён! Нажми кнопку ниже:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("❌ У вас нет доступа к этому боту.")

# Фиктивный HTTP-сервер для обхода ошибки с портом на Render
PORT = 8080

def run_fake_server():
    with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_password))

    print("Бот запущен...")
    threading.Thread(target=run_fake_server, daemon=True).start()  # Запускаем сервер в отдельном потоке
    app.run_polling()

if __name__ == "__main__":
    main()
