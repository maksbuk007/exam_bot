from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackContext

# Твой токен бота (замени на свой из @BotFather)
TOKEN = "7949149318:AAEKc_tnuByPQO8yFiZbj4hW0Xq06h-c51s"

# Разрешённые Telegram ID (можно добавить несколько)
ALLOWED_IDS = [804816309, 1151301056]  # Замени на свои ID

# Ссылка на мини-приложение
APP_URL = "https://mlogin.ct.ws/"

async def start(update: Update, context: CallbackContext) -> None:
    """Команда /start проверяет ID и отправляет доступ или отказ."""
    user_id = update.message.from_user.id

    if user_id in ALLOWED_IDS:
        keyboard = [[InlineKeyboardButton("🚀 Открыть мини-приложение", web_app=WebAppInfo(url=APP_URL))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("✅ Доступ разрешён! Нажми кнопку ниже:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("❌ У вас нет доступа к этому боту.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()

if __name__ == "__main__":
    main()
