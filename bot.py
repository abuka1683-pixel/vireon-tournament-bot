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
# VIREON TOURNAMENT BOT (ҚАЗАҚША НҰСҚА)
# ==========================================

# 1. БОТ ТОКЕНІ ЖӘНЕ АДМИН ДЕРЕКТЕРІ
BOT_TOKEN = "8639140920:AAGrRTPWG-hOksM_ssmFRUv9nSng8HxU7fE"
ADMIN_ID = 6847899606
ADMIN_USERNAME = "abukaa111222"

# 2. ТУРНИР КАНАЛЫНЫҢ СІЛТЕМЕСІ
CHANNEL_URL = "https://t.me/sabinanizhaksykoremm"

# ТУРНИР АҚПАРАТЫ
ENTRY_FEE = 250
FIRST_PRIZE = 600
SECOND_PRIZE = 400
MAP_NAME = "Двойная проблема"
PLAYER_LIMIT = 5

BANNED_BRAWLERS = "Уйымдастырушымен кейін хабарланады"

# Күйлерді бақылау (Conversation states)
WAITING_FOR_BS_ID, WAITING_FOR_RECEIPT, BROADCAST_TEXT = range(3)

# Тіркелгендер базасы
REGISTERED_PLAYERS = []  # User IDs
PLAYERS_INFO = []        # Деректер тізімі

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏆 Турнирге қатысу", callback_data="start_reg")],
        [InlineKeyboardButton("📋 Турнир ережелері", callback_data="rules")],
        [InlineKeyboardButton("❓ Турнирге қалай кіруге болады?", callback_data="join")],
        [InlineKeyboardButton("📢 Негізгі канал", url=CHANNEL_URL)],
    ])


def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ Турнирге қалай кіруге болады?", callback_data="join")],
        [InlineKeyboardButton("📢 Каналға өту", url=CHANNEL_URL)],
        [InlineKeyboardButton("⬅️ Бас мәзір", callback_data="home")],
    ])


def rules_text():
    return (
        "🏆 BRAWL STARS ТУРНИРІНІҢ ЕРЕЖЕЛЕРІ\n\n"
        f"💰 Кіру жарнасы: {ENTRY_FEE} ₸\n"
        f"👥 Қатысушылар саны: {PLAYER_LIMIT} адам\n"
        f"🗺️ Карта: {MAP_NAME}\n\n"
        f"🥇 1-орын: {FIRST_PRIZE} ₸\n"
        f"🥈 2-орын: {SECOND_PRIZE} ₸\n\n"
        f"🚫 ТЫЙЫМ САЛЫНҒАН БОЙЦТАР:\n{BANNED_BRAWLERS}\n\n"
        "📌 ҚАЛАЙ ҚАТЫСУҒА БОЛАДЫ:\n"
        "1. 'Турнирге қатысу' батырмасын басыңыз.\n"
        "2. Өз Brawl Stars ID-іңізді немесе никнейміңізді жазыңыз.\n"
        "3. Реквизит алу үшін ұйымдастырушыға жазыңыз.\n"
        "4. Төлем чегін осы чатқа жіберіңіз."
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "🎮 ҚОШ КЕЛДІҢІЗ!\n\n"
        "🏆 BRAWL STARS TOURNAMENT\n\n"
        "Турнир ережелері мен қатысу шарттарын біліңіз.\n\n"
        "Керекті бөлімді таңдаңыз:",
        reply_markup=main_menu()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "home":
        await query.edit_message_text(
            "🏆 БАС МӘЗІР\n\nБөлімді таңдаңыз:",
            reply_markup=main_menu()
        )
    elif query.data in ("tournament", "rules"):
        await query.edit_message_text(
            rules_text(),
            reply_markup=back_menu()
        )
    elif query.data == "join":
        await query.edit_message_text(
            "❓ ТУРНИРГЕ ҚАЛАЙ КІРУГЕ БОЛАДЫ?\n\n"
            "1. Негізгі каналға өтіңіз.\n"
            "2. Турнир туралы хабарландыруды табыңыз.\n"
            "3. Ботта 'Турнирге қатысу' батырмасын басыңыз.\n"
            "4. Өз ID-іңізді және төлем чегін жіберіңіз.\n\n"
            "👇 Каналды ашу үшін төмендегі батырманы басыңыз:",
            reply_markup=back_menu()
        )


# --- ТІРКЕЛУ ЖҮЙЕСІ ---

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if len(REGISTERED_PLAYERS) >= PLAYER_LIMIT:
        await query.edit_message_text(
            "❌ Кешіріңіз, турнирдегі барлық орындар толып кетті!",
            reply_markup=back_menu()
        )
        return ConversationHandler.END

    await query.edit_message_text(
        "📝 **ТУРНИРГЕ ТІРКЕЛУ**\n\n"
        "Өтініш, өзіңіздің **Brawl Stars ID**-іңізді немесе никнейміңізді жазыңыз:"
    )
    return WAITING_FOR_BS_ID


async def get_bs_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bs_id = update.message.text
    context.user_data["bs_id"] = bs_id

    pay_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Ұйымдастырушыға жазу", url=f"https://t.me/{ADMIN_USERNAME}")]
    ])

    await update.message.reply_text(
        f"✅ Нигіңіз қабылданды: `{bs_id}`\n\n"
        f"💳 **ЖАРНА ТӨЛЕУ ({ENTRY_FEE} ₸)**\n"
        f"Төлем реквизиттерін алу үшін ұйымдастырушыға жазыңыз: @{ADMIN_USERNAME}\n\n"
        "📸 **Төлем жасаған соң, чекті (скриншот/сурет/файл) осы чатқа жіберіңіз!**",
        parse_mode="Markdown",
        reply_markup=pay_keyboard
    )
    return WAITING_FOR_RECEIPT


async def get_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bs_id = context.user_data.get("bs_id", "Көрсетілмеген")

    admin_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Қабылдау", callback_data=f"approve_{user.id}_{bs_id}"),
            InlineKeyboardButton("❌ Қайтару", callback_data=f"reject_{user.id}")
        ]
    ])

    caption_text = (
        f"📥 **ТУРНИРГЕ ЖАҢА ӨТІНІШ!**\n\n"
        f"👤 Есімі: {user.full_name} (@{user.username})\n"
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
        "⏳ **Чек ұйымдастырушыға тексеруге жіберілді!**\n\n"
        "Тексерістен кейін сізге хабарлама келеді.",
        reply_markup=main_menu()
    )
    return ConversationHandler.END


async def cancel_reg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Тіркелу тоқтатылды.", reply_markup=main_menu())
    return ConversationHandler.END


# --- АДМИН ПАНЕЛІ ---

async def admin_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    action = data[0]
    target_user_id = int(data[1])

    if action == "approve":
        bs_id = data[2] if len(data) > 2 else "Қатысушы"
        if target_user_id not in REGISTERED_PLAYERS:
            REGISTERED_PLAYERS.append(target_user_id)
            PLAYERS_INFO.append({"id": target_user_id, "bs_id": bs_id})

        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **МӘРТЕБЕСІ: ҚАБЫЛДАНДЫ**")
        await context.bot.send_message(
            chat_id=target_user_id,
            text="🎉 **ҚҰТТЫҚТАЙМЫЗ!** Өтінішіңіз расталды. Сіз турнирге сәтті тіркелдіңіз!"
        )

        # Орындар толық толғанда админге хабар беру
        if len(REGISTERED_PLAYERS) >= PLAYER_LIMIT:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🔥 **БАРЛЫҚ ОРЫНДАР ТОЛДЫ!** ({len(REGISTERED_PLAYERS)}/{PLAYER_LIMIT})\n"
                     "Қатысушыларға лобби кодын жіберу үшін /broadcast командасын қолданыңыз."
            )

    elif action == "reject":
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **МӘРТЕБЕСІ: ҚАБЫЛДАНБАДЫ**")
        await context.bot.send_message(
            chat_id=target_user_id,
            text="❌ Кешіріңіз, сіздің өтінішіңіз қабылданбады. Ұйымдастырушымен байланысыңыз."
        )


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    players_list = "\n".join([f"- ID: `{p['bs_id']}` (TG: {p['id']})" for p in PLAYERS_INFO]) if PLAYERS_INFO else "Әлі ойыншылар жоқ"

    await update.message.reply_text(
        f"👑 **АДМИН ПАНЕЛІ**\n\n"
        f"👥 Қатысушылар: {len(REGISTERED_PLAYERS)}/{PLAYER_LIMIT}\n\n"
        f"📋 **Қатысушылар тізімі:**\n{players_list}\n\n"
        "💡 Админ командалары:\n"
        "/broadcast - Барлық қатысушыларға хабарлама/код жіберу\n"
        "/reset_tournament - Жаңа турнир үшін тізімді тазалау",
        parse_mode="Markdown"
    )


async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("📢 Барлық қатысушыларға жіберілетін мәтінді немесе лобби кодын жазыңыз:")
    return BROADCAST_TEXT


async def send_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_to_send = update.message.text
    count = 0
    for user_id in REGISTERED_PLAYERS:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"📢 **ҰЙЫМДАСТЫРУШЫДАН ХАБАРЛАМА:**\n\n{text_to_send}", parse_mode="Markdown")
            count += 1
        except Exception:
            pass
    await update.message.reply_text(f"✅ Хабарлама {count} қатысушыға сәтті жіберілді!")
    return ConversationHandler.END


async def reset_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    REGISTERED_PLAYERS.clear()
    PLAYERS_INFO.clear()
    await update.message.reply_text("🔄 Ойыншылар тізімі тазаланды! Жаңа турнирге дайын.")


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN табылмады.")

    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_registration, pattern="^start_reg$"),
            CommandHandler("broadcast", start_broadcast)
        ],
        states={
            WAITING_FOR_BS_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_bs_id)],
            WAITING_FOR_RECEIPT: [MessageHandler(filters.PHOTO | filters.Document.ALL, get_receipt)],
            BROADCAST_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_broadcast)],
        },
        fallbacks=[CommandHandler("cancel", cancel_reg)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("reset_tournament", reset_tournament))
    app.add_handler(CallbackQueryHandler(admin_decision, pattern="^(approve|reject)_"))
    app.add_handler(CallbackQueryHandler(buttons))

    logger.info("VIREON Tournament Bot іске қосылды!")
    app.run_polling()


if __name__ == "__main__":
    main()
