import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

# ==========================================
# VIREON TOURNAMENT BOT (SAFE VERSION)
# ==========================================

# 1. БОТ ТОКЕНІ
BOT_TOKEN = "8639140920:AAGrRTPWG-hOksM_ssmFRUv9nSng8HxU7fE"

# 2. ӨЗІҢІЗДІҢ ТЕЛЕГРАМ ID-ҢІЗ (Сандармен)
ADMIN_ID = 6847899606

# 3. ӨЗІҢІЗДІҢ ТЕЛЕГРАМ ЛОГИНИҢІЗ (Төлем алу үшін)
ADMIN_USERNAME = "@abukaa111222"

# 4. ТУРНИР КАНАЛЫНЫҢ СІЛТЕМЕСІ
CHANNEL_URL = "https://t.me/sabinanizhaksykoremm"

# ТУРНИР АҚПАРАТЫ
ENTRY_FEE = 250
FIRST_PRIZE = 600
SECOND_PRIZE = 400
MAP_NAME = "Двойная проблема"
PLAYER_LIMIT = 5

BANNED_BRAWLERS = "Будут объявлены организатором"

# Күйлерді бақылау (Conversation states)
WAITING_FOR_BS_ID, WAITING_FOR_RECEIPT = range(2)

# Тіркелгендер тізімі
REGISTERED_PLAYERS = []

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏆 Войти в турнир", callback_data="start_reg")],
        [InlineKeyboardButton("📋 Правила турнира", callback_data="rules")],
        [InlineKeyboardButton("❓ Как попасть на турнир?", callback_data="join")],
        [InlineKeyboardButton("📢 Оригинальный канал", url=CHANNEL_URL)],
    ])


def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ Как попасть на турнир?", callback_data="join")],
        [InlineKeyboardButton("📢 Перейти в канал", url=CHANNEL_URL)],
        [InlineKeyboardButton("⬅️ Главное меню", callback_data="home")],
    ])


def rules_text():
    return (
        "🏆 ПРАВИЛА ТУРНИРА BRAWL STARS\n\n"
        f"💰 Вход: {ENTRY_FEE} ₸\n"
        f"👥 Участников: {PLAYER_LIMIT} человек\n"
        f"🗺️ Карта: {MAP_NAME}\n\n"
        f"🥇 1 место: {FIRST_PRIZE} ₸\n"
        f"🥈 2 место: {SECOND_PRIZE} ₸\n\n"
        f"🚫 ЗАПРЕЩЁННЫЕ БОЙЦЫ:\n{BANNED_BRAWLERS}\n\n"
        "📌 КАК УЧАСТВУАТЬ:\n"
        "1. Нажмите 'Войти в турнир'.\n"
        "2. Укажите ваш Brawl Stars ID.\n"
        "3. Напишите организатору для получения реквизитов.\n"
        "4. Отправьте чек оплаты в этот чат."
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "🎮 ДОБРО ПОЖАЛОВАТЬ!\n\n"
        "🏆 BRAWL STARS TOURNAMENT\n\n"
        "Узнай правила и условия участия в нашем турнире.\n\n"
        "Выбери нужный раздел:",
        reply_markup=main_menu()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "home":
        await query.edit_message_text(
            "🏆 ГЛАВНОЕ МЕНЮ\n\nВыбери раздел:",
            reply_markup=main_menu()
        )
    elif query.data in ("tournament", "rules"):
        await query.edit_message_text(
            rules_text(),
            reply_markup=back_menu()
        )
    elif query.data == "join":
        await query.edit_message_text(
            "❓ КАК ПОПАСТЬ НА ТУРНИР?\n\n"
            "1. Перейди в оригинальный канал.\n"
            "2. Найди объявление о турнире.\n"
            "3. Нажми 'Войти в турнир' в боте.\n"
            "4. Отправь свой ID и чек оплаты.\n\n"
            "👇 Нажми кнопку, чтобы открыть канал:",
            reply_markup=back_menu()
        )


# --- ТІРКЕЛУ ЖҮЙЕСІ ---

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if len(REGISTERED_PLAYERS) >= PLAYER_LIMIT:
        await query.edit_message_text(
            "❌ Извините, все слоты на турнир уже заняты!",
            reply_markup=back_menu()
        )
        return ConversationHandler.END

    await query.edit_message_text(
        "📝 **РЕГИСТРАЦИЯ НА ТУРНИР**\n\n"
        "Пожалуйста, напишите ваш **Brawl Stars ID** или игровой никнейм:"
    )
    return WAITING_FOR_BS_ID


async def get_bs_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bs_id = update.message.text
    context.user_data["bs_id"] = bs_id

    pay_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Написать организатору", url=f"https://t.me/{ADMIN_USERNAME}")]
    ])

    await update.message.reply_text(
        f"✅ Ваш ID принят: `{bs_id}`\n\n"
        f"💳 **ОПЛАТА ВЗНОСА ({ENTRY_FEE} ₸)**\n"
        f"Чтобы получить реквизиты, напишите организатору: @{ADMIN_USERNAME}\n\n"
        "📸 **После оплаты отправьте скриншот/чек в этот чат!**",
        parse_mode="Markdown",
        reply_markup=pay_keyboard
    )
    return WAITING_FOR_RECEIPT


async def get_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bs_id = context.user_data.get("bs_id", "Не указан")

    admin_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{user.id}")
        ]
    ])

    caption_text = (
        f"📥 **НОВАЯ ЗАЯВКА НА ТУРНИР!**\n\n"
        f"👤 Имя: {user.full_name} (@{user.username})\n"
        f"🆔 Telegram ID: `{user.id}`\n"
        f"🎮 BS ID/Ник: `{bs_id}`"
    )

    if update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=caption_text,
            reply_markup=admin_keyboard,
            parse_mode="Markdown"
        )
    elif update.message.document:
        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=update.message.document.file_id,
            caption=caption_text,
            reply_markup=admin_keyboard,
            parse_mode="Markdown"
        )

    await update.message.reply_text(
        "⏳ **Чек отправлен организатору!**\n\n"
        "После проверки вы получите уведомление.",
        reply_markup=main_menu()
    )
    return ConversationHandler.END


async def cancel_reg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Регистрация отменена.", reply_markup=main_menu())
    return ConversationHandler.END


# --- АДМИН ПАНЕЛЬ ---

async def admin_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    action = data[0]
    target_user_id = int(data[1])

    if action == "approve":
        if target_user_id not in REGISTERED_PLAYERS:
            REGISTERED_PLAYERS.append(target_user_id)
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **СТАТУС: ОДОБРЕНО**")
        await context.bot.send_message(
            chat_id=target_user_id,
            text="🎉 **ПОЗДРАВЛЯЕМ!** Ваша заявка одобрена. Вы успешно зарегистрированы на турнир!"
        )
    elif action == "reject":
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **СТАТУС: ОТКЛОНЕНО**")
        await context.bot.send_message(
            chat_id=target_user_id,
            text="❌ Извините, ваша заявка на турнир была отклонена. Свяжитесь с организатором."
        )


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        f"👑 **АДМИН ПАНЕЛЬ**\n\n"
        f"👥 Зарегистрировано участников: {len(REGISTERED_PLAYERS)}/{PLAYER_LIMIT}\n"
        f"🆔 ID участников: {REGISTERED_PLAYERS}"
    )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден.")

    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_registration, pattern="^start_reg$")],
        states={
            WAITING_FOR_BS_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_bs_id)],
            WAITING_FOR_RECEIPT: [MessageHandler(filters.PHOTO | filters.Document.ALL, get_receipt)],
        },
        fallbacks=[CommandHandler("cancel", cancel_reg)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(admin_decision, pattern="^(approve|reject)_"))
    app.add_handler(CallbackQueryHandler(buttons))

    logger.info("VIREON Tournament Bot запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
