
import os
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==================================================
# VIREON TOURNAMENT BOT
# ==================================================

# 🔴 ТОКЕНДІ ОСЫ ЖЕРГЕ ҚОЙМА!
# Төмендегі BOT_TOKEN Render ортасынан автоматты алынады.
# Render → Environment → Add Environment Variable
# Key: BOT_TOKEN
# Value: осында BotFather берген токеніңді енгіз.

BOT_TOKEN = os.getenv("8639140920:AAGrRTPWG-hOksM_ssmFRUv9nSng8HxU7fE", "").strip()

# ==================================================
# ⚙️ ТУРНИР БАПТАУЛАРЫ
# ==================================================

# 🟡 ӨЗІҢНІҢ ОРИГИНАЛ КАНАЛЫҢНЫҢ СІЛТЕМЕСІН ОСЫ ЖЕРГЕ ҚОЙ!
CHANNEL_URL = "https://t.me/https:/sabinanizhaksykoremm"

ENTRY_FEE = 250
FIRST_PLACE = 600
SECOND_PLACE = 400

MAP_NAME = "Двойная проблема"
PLAYER_LIMIT = 5

# 🚫 ТЫЙЫМ САЛЫНҒАН БОЙЦТАРДЫ КЕЙІН ОСЫ ЖЕРГЕ ЖАЗАМЫЗ
BANNED_BRAWLERS = "Будут объявлены организатором"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ==================================================
# 🏠 БАСТЫ МӘЗІР
# ==================================================

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "🏆 Войти в турнир",
                callback_data="tournament",
            )
        ],
        [
            InlineKeyboardButton(
                "📋 Правила турнира",
                callback_data="rules",
            )
        ],
        [
            InlineKeyboardButton(
                "❓ Как попасть на турнир?",
                callback_data="join",
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Оригинальный канал",
                url=CHANNEL_URL,
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ==================================================
# 🔙 ҚАЙТУ МӘЗІРІ
# ==================================================

def back_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "❓ Как попасть на турнир?",
                callback_data="join",
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Перейти в оригинальный канал",
                url=CHANNEL_URL,
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Главное меню",
                callback_data="home",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ==================================================
# 📋 ТУРНИР ЕРЕЖЕЛЕРІ
# ==================================================

def tournament_rules():
    return (
        "🏆 ПРАВИЛА ТУРНИРА BRAWL STARS\n\n"
        "💰 СТОИМОСТЬ УЧАСТИЯ\n"
        f"Взнос: {ENTRY_FEE} ₸\n\n"
        "👥 КОЛИЧЕСТВО УЧАСТНИКОВ\n"
        f"В турнире участвуют {PLAYER_LIMIT} игроков.\n\n"
        "🗺️ КАРТА\n"
        f"{MAP_NAME}\n\n"
        "🚫 ЗАПРЕЩЁННЫЕ БОЙЦЫ\n"
        f"{BANNED_BRAWLERS}\n\n"
        "🥇 ПРИЗОВЫЕ МЕСТА\n"
        f"🥇 1 место — {FIRST_PLACE} ₸\n"
        f"🥈 2 место — {SECOND_PLACE} ₸\n\n"
        "📌 ВАЖНО\n"
        "Перед участием внимательно прочитай правила.\n"
        "Следуй указаниям организатора.\n"
        "Регистрация подтверждается организатором."
    )


# ==================================================
# 🚀 /START
# ==================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    text = (
        "🎮 ДОБРО ПОЖАЛОВАТЬ!\n\n"
        "🏆 BRAWL STARS TOURNAMENT\n\n"
        "Здесь ты можешь узнать условия участия, "
        "правила турнира и перейти в наш оригинальный канал.\n\n"
        "👇 Выбери нужный раздел:"
    )

    await update.effective_message.reply_text(
        text,
        reply_markup=main_menu(),
    )


# ==================================================
# 🔘 МӘЗІР БАТЫРМАЛАРЫ
# ==================================================

async def buttons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    if query.data == "home":
        await query.edit_message_text(
            "🏆 ГЛАВНОЕ МЕНЮ\n\nВыбери нужный раздел:",
            reply_markup=main_menu(),
        )

    elif query.data in ("tournament", "rules"):
        await query.edit_message_text(
            tournament_rules(),
            reply_markup=back_menu(),
        )

    elif query.data == "join":
        text = (
            "❓ КАК ПОПАСТЬ НА ТУРНИР?\n\n"
            "1️⃣ Перейди в наш оригинальный Telegram-канал.\n"
            "2️⃣ Найди публикацию о турнире.\n"
            "3️⃣ Прочитай условия регистрации.\n"
            "4️⃣ Выполни инструкции организатора.\n"
            "5️⃣ Дождись подтверждения участия.\n\n"
            "📢 Все подробности и объявления "
            "публикуются в оригинальном канале."
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "📢 Открыть оригинальный канал",
                    url=CHANNEL_URL,
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Главное меню",
                    callback_data="home",
                )
            ],
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


# ==================================================
# ⚠️ ҚАТЕЛЕРДІ ЖАЗУ
# ==================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.error(
        "Произошла ошибка при обработке обновления",
        exc_info=context.error,
    )


# ==================================================
# ▶️ БОТТЫ ІСКЕ ҚОСУ
# ==================================================

def main():
    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN табылмады!\n"
            "Render → твой сервис → Environment бөліміне кір.\n"
            "Key: BOT_TOKEN\n"
            "Value: BotFather берген токенің."
        )

    if "ТВОЙ_КАНАЛ" in CHANNEL_URL:
        logger.warning(
            "CHANNEL_URL әлі өзгертілмеген! "
            "Өз Telegram каналыңның сілтемесін қой."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_error_handler(error_handler)

    logger.info("VIREON Tournament Bot іске қосылды!")

    app.run_polling()


if __name__ == "__main__":
    main()

