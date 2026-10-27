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
# VIREON TOURNAMENT BOT (ULTRA UPGRADE - KZ/RU/EN)
# ==========================================

BOT_TOKEN = "8639140920:AAGrRTPWG-hOksM_ssmFRUv9nSng8HxU7fE"
ADMIN_ID = 6847899606
ADMIN_USERNAME = "abukaa111222"
CHANNEL_URL = "https://t.me/sabinanizhaksykoremm"

TIKTOK_HANDLE = "Nexor6589"
YOUTUBE_HANDLE = "Nexor6589"

ENTRY_FEE = 250
FIRST_PRIZE = 600
SECOND_PRIZE = 400
MAP_NAME = "Двойная проблема"
PLAYER_LIMIT = 5

# Conversation күйлері
WAITING_FOR_BS_ID = 1
WAITING_FOR_RECEIPT = 2
WAITING_MATCH_ID = 3

REGISTERED_PLAYERS = []
PLAYERS_INFO = []

QUEUE_1V1 = []
QUEUE_3V3 = []

USER_LANGS = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEXTS = {
    "KK": {
        "welcome": "🎮 VIREON БОТЫНА ҚОШ КЕЛДІҢІЗ!\n\nТурнирлерге қатысып, 1в1 немесе 3в3 форматта қарсылас табыңыз.\n\nҚажетті бөлімді таңдаңыз:",
        "btn_tour": "🏆 Турнирге қатысу",
        "btn_1v1": "⚔️ 1в1 Дуэль табу",
        "btn_3v3": "🛡️ 3в3 Команда табу",
        "btn_profile": "👤 Менің профилім",
        "btn_rules": "📋 Турнир ережелері",
        "btn_channel": "📢 Негізгі канал",
        "btn_lang": "🌐 Тілді ауыстыру / Язык / Language",
        "btn_back": "⬅️ Бас мәзір",
        "rules": f"🏆 BRAWL STARS ТУРНИРІНІҢ ЕРЕЖЕЛЕРІ\n\n💰 Кіру жарнасы: {ENTRY_FEE} ₸\n👥 Қатысушылар саны: {PLAYER_LIMIT} адам\n🗺️ Карта: {MAP_NAME}\n\n🥇 1-орын: {FIRST_PRIZE} ₸\n🥈 2-орын: {SECOND_PRIZE} ₸",
        "profile": "👤 **СІЗДІҢ ПРОФИЛІҢІЗ**\n\n🏷️ Есімі: {name}\n🆔 Telegram ID: `{id}`\n\n📱 **Әлеуметтік желілер:**\n🎵 TikTok: `{tt}` (https://tiktok.com/@{tt})\n📺 YouTube: `{yt}`",
        "reg_start": "📝 **ТУРНИРГЕ ТІРКЕЛУ**\n\nӨтініш, өзіңіздің **Brawl Stars ID**-іңізді немесе никнейміңізді жазыңыз:",
        "reg_full": "❌ Кешіріңіз, турнирдегі барлық орындар толып кетті!",
        "bs_id_accept": "✅ Нигіңіз қабылданды: `{bs_id}`\n\n💳 **ЖАРНА ТӨЛЕУ ({fee} ₸)**\nРеквизит алу үшін ұйымдастырушыға жазыңыз: @{admin}\n\n📸 **Төлем жасаған соң, чекті осы чатқа жіберіңіз!**",
        "btn_admin_write": "💬 Ұйымдастырушыға жазу",
        "receipt_sent": "⏳ **Чек ұйымдастырушыға тексеруге жіберілді!**",
        "match_1v1_start": "⚔️ **1в1 ДУЭЛЬ РЕЖИМІ**\n\nОйынға шығу үшін өзіңіздің **Brawl Stars ID** немесе никнейміңізді жазыңыз:",
        "match_3v3_start": "🛡️ **3в3 КОМАНДА РЕЖИМІ**\n\nОйынға шығу үшін өзіңіздің **Brawl Stars ID** немесе никнейміңізді жазыңыз:",
        "searching": "🔍 **{mode} ізделуде...**\n\nСіздің ID: `{bs_id}` қабылданды.\nҚарсылас ізделіп жатыр, сәл күтіңіз! ⏳",
        "match_found": "🎉 **ҚАРСЫЛАС ТАБЫЛДЫ! ({mode})**\n\n🎮 Қарсыластың ID/Нигі: `{other_bs}`\n💬 Telegram: @{other_tg}\n\nЖылдам друзя тастап, ойынға кіріңіздер!",
        "approved": "🎉 **ҚҰТТЫҚТАЙМЫЗ!** Өтінішіңіз расталды. Сіз турнирге сәтті тіркелдіңіз!",
        "rejected": "❌ Кешіріңіз, өтінішіңіз қабылданбады."
    },
    "RU": {
        "welcome": "🎮 ДОБРО ПОЖАЛОВАТЬ В VIREON БОТ!\n\nУчаствуйте в турнирах и находите соперников 1в1 или 3в3.\n\nВыберите нужный раздел:",
        "btn_tour": "🏆 Участвовать в турнире",
        "btn_1v1": "⚔️ Найти 1в1 Дуэль",
        "btn_3v3": "🛡️ Найти 3в3 Команду",
        "btn_profile": "👤 Мой профиль",
        "btn_rules": "📋 Правила турнира",
        "btn_channel": "📢 Основной канал",
        "btn_lang": "🌐 Тілді ауыстыру / Язык / Language",
        "btn_back": "⬅️ Главное меню",
        "rules": f"🏆 ПРАВИЛА ТУРНИРА BRAWL STARS\n\n💰 Взнос: {ENTRY_FEE} ₸\n👥 Участников: {PLAYER_LIMIT} чел.\n🗺️ Карта: {MAP_NAME}\n\n🥇 1 место: {FIRST_PRIZE} ₸\n🥈 2 место: {SECOND_PRIZE} ₸",
        "profile": "👤 **ВАШ ПРОФИЛЬ**\n\n🏷️ Имя: {name}\n🆔 Telegram ID: `{id}`\n\n📱 **Социальные сети:**\n🎵 TikTok: `{tt}` (https://tiktok.com/@{tt})\n📺 YouTube: `{yt}`",
        "reg_start": "📝 **РЕГИСТРАЦИЯ НА ТУРНИР**\n\nПожалуйста, напишите ваш **Brawl Stars ID** или никнейм:",
        "reg_full": "❌ Извините, все слоты на турнир уже заняты!",
        "bs_id_accept": "✅ Ваш ник принят: `{bs_id}`\n\n💳 **ОПЛАТА ВЗНОСА ({fee} ₸)**\nЧтобы получить реквизиты, напишите организатору: @{admin}\n\n📸 **После оплаты отправьте чек в этот чат!**",
        "btn_admin_write": "💬 Написать организатору",
        "receipt_sent": "⏳ **Чек отправлен организатору на проверку!**",
        "match_1v1_start": "⚔️ **РЕЖИМ 1в1 ДУЭЛЬ**\n\nНапишите ваш **Brawl Stars ID** или никнейм для поиска:",
        "match_3v3_start": "🛡️ **РЕЖИМ 3в3 КОМАНДА**\n\nНапишите ваш **Brawl Stars ID** или никнейм для поиска:",
        "searching": "🔍 **Поиск {mode}...**\n\nВаш ID: `{bs_id}` принят.\nПоиск соперника, пожалуйста подождите! ⏳",
        "match_found": "🎉 **СОПЕРНИК НАЙДЕН! ({mode})**\n\n🎮 ID/Ник соперника: `{other_bs}`\n💬 Telegram: @{other_tg}\n\nБыстрее добавляйтесь в друзья и начинайте игру!",
        "approved": "🎉 **ПОЗДРАВЛЯЕМ!** Ваша заявка одобрена. Вы успешно зарегистрированы!",
        "rejected": "❌ Извините, ваша заявка была отклонена."
    },
    "EN": {
        "welcome": "🎮 WELCOME TO VIREON BOT!\n\nJoin tournaments and find 1v1 or 3v3 opponents.\n\nSelect a section below:",
        "btn_tour": "🏆 Join Tournament",
        "btn_1v1": "⚔️ Find 1v1 Duel",
        "btn_3v3": "🛡️ Find 3v3 Team",
        "btn_profile": "👤 My Profile",
        "btn_rules": "📋 Tournament Rules",
        "btn_channel": "📢 Official Channel",
        "btn_lang": "🌐 Change Language / Тіл / Язык",
        "btn_back": "⬅️ Main Menu",
        "rules": f"🏆 BRAWL STARS TOURNAMENT RULES\n\n💰 Entry Fee: {ENTRY_FEE} ₸\n👥 Players: {PLAYER_LIMIT}\n🗺️ Map: {MAP_NAME}\n\n🥇 1st Place: {FIRST_PRIZE} ₸\n🥈 2nd Place: {SECOND_PRIZE} ₸",
        "profile": "👤 **YOUR PROFILE**\n\n🏷️ Name: {name}\n🆔 Telegram ID: `{id}`\n\n📱 **Social Networks:**\n🎵 TikTok: `{tt}` (https://tiktok.com/@{tt})\n📺 YouTube: `{yt}`",
        "reg_start": "📝 **TOURNAMENT REGISTRATION**\n\nPlease enter your **Brawl Stars ID** or nickname:",
        "reg_full": "❌ Sorry, all slots for the tournament are full!",
        "bs_id_accept": "✅ Nickname accepted: `{bs_id}`\n\n💳 **ENTRY FEE ({fee} ₸)**\nContact organizer to get payment details: @{admin}\n\n📸 **Send your payment receipt screenshot here after payment!**",
        "btn_admin_write": "💬 Contact Organizer",
        "receipt_sent": "⏳ **Receipt sent to organizer for review!**",
        "match_1v1_start": "⚔️ **1v1 DUEL MODE**\n\nEnter your **Brawl Stars ID** or nickname to start searching:",
        "match_3v3_start": "🛡️ **3v3 TEAM MODE**\n\nEnter your **Brawl Stars ID** or nickname to start searching:",
        "searching": "🔍 **Searching {mode}...**\n\nYour ID: `{bs_id}` accepted.\nLooking for an opponent, please wait! ⏳",
        "match_found": "🎉 **OPPONENT FOUND! ({mode})**\n\n🎮 Opponent ID/Nick: `{other_bs}`\n💬 Telegram: @{other_tg}\n\nAdd each other as friends and start the match!",
        "approved": "🎉 **CONGRATULATIONS!** Your application is approved. You are registered!",
        "rejected": "❌ Sorry, your application was rejected."
    }
}

def get_lang(user_id):
    return USER_LANGS.get(user_id, "KK")

def main_menu(user_id):
    lang = get_lang(user_id)
    t = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["btn_tour"], callback_data="start_reg")],
        [InlineKeyboardButton(t["btn_1v1"], callback_data="find_1v1"),
         InlineKeyboardButton(t["btn_3v3"], callback_data="find_3v3")],
        [InlineKeyboardButton(t["btn_profile"], callback_data="my_profile")],
        [InlineKeyboardButton(t["btn_rules"], callback_data="rules")],
        [InlineKeyboardButton(t["btn_channel"], url=CHANNEL_URL)],
        [InlineKeyboardButton(t["btn_lang"], callback_data="change_lang")],
    ])

def lang_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇰🇿 Қазақша", callback_data="set_lang_KK")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang_RU")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_EN")],
        [InlineKeyboardButton("⬅️ Артқа / Назад", callback_data="home")]
    ])

def back_menu(user_id):
    lang = get_lang(user_id)
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(TEXTS[lang]["btn_back"], callback_data="home")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    text = TEXTS[lang]["welcome"]
    
    if update.callback_query:
        try:
            await update.callback_query.answer()
            await update.callback_query.message.edit_text(text, reply_markup=main_menu(user_id))
        except Exception:
            await update.callback_query.message.reply_text(text, reply_markup=main_menu(user_id))
    else:
        await update.effective_message.reply_text(text, reply_markup=main_menu(user_id))


async def buttons_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_lang(user_id)
    t = TEXTS[lang]

    try:
        await query.answer()
    except Exception:
        pass

    if query.data == "home":
        await query.edit_message_text(t["welcome"], reply_markup=main_menu(user_id))
        return ConversationHandler.END

    elif query.data == "change_lang":
        await query.edit_message_text("🌐 Тілді таңдаңыз / Выберите язык / Select language:", reply_markup=lang_menu())

    elif query.data.startswith("set_lang_"):
        new_lang = query.data.split("_")[2]
        USER_LANGS[user_id] = new_lang
        new_t = TEXTS[new_lang]
        await query.edit_message_text(new_t["welcome"], reply_markup=main_menu(user_id))

    elif query.data == "rules":
        await query.edit_message_text(t["rules"], reply_markup=back_menu(user_id))

    elif query.data == "my_profile":
        user = query.from_user
        profile_txt = t["profile"].format(name=user.full_name, id=user.id, tt=TIKTOK_HANDLE, yt=YOUTUBE_HANDLE)
        await query.edit_message_text(profile_txt, parse_mode="Markdown", reply_markup=back_menu(user_id))

    elif query.data == "find_1v1":
        context.user_data["match_mode"] = "1в1"
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton(t["btn_back"], callback_data="home")]])
        await query.edit_message_text(t["match_1v1_start"], reply_markup=back_kb)
        return WAITING_MATCH_ID

    elif query.data == "find_3v3":
        context.user_data["match_mode"] = "3в3"
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton(t["btn_back"], callback_data="home")]])
        await query.edit_message_text(t["match_3v3_start"], reply_markup=back_kb)
        return WAITING_MATCH_ID

    elif query.data == "start_reg":
        if len(REGISTERED_PLAYERS) >= PLAYER_LIMIT:
            await query.edit_message_text(t["reg_full"], reply_markup=back_menu(user_id))
            return ConversationHandler.END
        
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton(t["btn_back"], callback_data="home")]])
        await query.edit_message_text(t["reg_start"], reply_markup=back_kb)
        return WAITING_FOR_BS_ID


# --- MATCHMAKING & REGISTRATION MESSAGES ---

async def process_matchmaking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    lang = get_lang(user_id)
    t = TEXTS[lang]

    if not update.message or not update.message.text:
        return WAITING_MATCH_ID

    bs_id = update.message.text
    mode = context.user_data.get("match_mode", "1в1")

    queue = QUEUE_1V1 if mode == "1в1" else QUEUE_3V3
    player_data = {"user_id": user_id, "username": user.username or user.first_name, "bs_id": bs_id, "lang": lang}

    if not any(p["user_id"] == user_id for p in queue):
        queue.append(player_data)

    await update.message.reply_text(
        t["searching"].format(mode=mode, bs_id=bs_id),
        parse_mode="Markdown",
        reply_markup=back_menu(user_id)
    )

    if len(queue) >= 2:
        p1 = queue.pop(0)
        p2 = queue.pop(0)

        for p_target, p_other in [(p1, p2), (p2, p1)]:
            target_t = TEXTS[p_target["lang"]]
            try:
                await context.bot.send_message(
                    chat_id=p_target["user_id"],
                    text=target_t["match_found"].format(mode=mode, other_bs=p_other['bs_id'], other_tg=p_other['username']),
                    parse_mode="Markdown",
                    reply_markup=main_menu(p_target["user_id"])
                )
            except Exception:
                pass

    return ConversationHandler.END


async def get_bs_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    t = TEXTS[lang]

    if not update.message or not update.message.text:
        return WAITING_FOR_BS_ID

    bs_id = update.message.text
    context.user_data["bs_id"] = bs_id

    pay_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t["btn_admin_write"], url=f"https://t.me/{ADMIN_USERNAME}")],
        [InlineKeyboardButton(t["btn_back"], callback_data="home")]
    ])

    await update.message.reply_text(
        t["bs_id_accept"].format(bs_id=bs_id, fee=ENTRY_FEE, admin=ADMIN_USERNAME),
        parse_mode="Markdown",
        reply_markup=pay_keyboard
    )
    return WAITING_FOR_RECEIPT


async def get_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    lang = get_lang(user_id)
    t = TEXTS[lang]
    bs_id = context.user_data.get("bs_id", "Unknown")

    if not update.message or not (update.message.photo or update.message.document):
        await update.message.reply_text("📸 Өтініш, төлем чегін скриншот (фото) немесе файл түрінде жіберіңіз!", reply_markup=back_menu(user_id))
        return WAITING_FOR_RECEIPT

    admin_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Қабылдау", callback_data=f"approve_{user.id}_{bs_id}"),
            InlineKeyboardButton("❌ Қайтару", callback_data=f"reject_{user.id}")
        ]
    ])

    caption_text = (
        f"📥 **НОВАЯ ЗАЯВКА НА ТУРНИР!**\n\n"
        f"👤 Имя: {user.full_name} (@{user.username})\n"
        f"🆔 Telegram ID: `{user.id}`\n"
        f"🎮 BS ID/Ник: `{bs_id}`"
    )

    try:
        if update.message.photo:
            await context.bot.send_photo(chat_id=ADMIN_ID, photo=update.message.photo[-1].file_id, caption=caption_text, reply_markup=admin_keyboard, parse_mode="Markdown")
        elif update.message.document:
            await context.bot.send_document(chat_id=ADMIN_ID, document=update.message.document.file_id, caption=caption_text, reply_markup=admin_keyboard, parse_mode="Markdown")
    except Exception:
        pass

    await update.message.reply_text(t["receipt_sent"], reply_markup=back_menu(user_id))
    return ConversationHandler.END


async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    if update.callback_query:
        try:
            await update.callback_query.answer()
            await update.callback_query.message.edit_text(TEXTS[lang]["welcome"], reply_markup=main_menu(user_id))
        except Exception:
            pass
    return ConversationHandler.END


# --- ADMIN PANEL ---

async def admin_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass

    data = query.data.split("_")
    action = data[0]
    target_user_id = int(data[1])
    target_lang = get_lang(target_user_id)

    if action == "approve":
        bs_id = data[2] if len(data) > 2 else "Player"
        if target_user_id not in REGISTERED_PLAYERS:
            REGISTERED_PLAYERS.append(target_user_id)
            PLAYERS_INFO.append({"id": target_user_id, "bs_id": bs_id})

        try:
            await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **СТАТУС: ҚАБЫЛДАНДЫ**")
        except Exception:
            pass

        await context.bot.send_message(
            chat_id=target_user_id,
            text=TEXTS[target_lang]["approved"],
            reply_markup=main_menu(target_user_id)
        )
    elif action == "reject":
        try:
            await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **СТАТУС: ҚАЙТАРЫЛДЫ**")
        except Exception:
            pass

        await context.bot.send_message(
            chat_id=target_user_id,
            text=TEXTS[target_lang]["rejected"],
            reply_markup=main_menu(target_user_id)
        )


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    players_list = "\n".join([f"- ID: `{p['bs_id']}` (TG: {p['id']})" for p in PLAYERS_INFO]) if PLAYERS_INFO else "Ойыншылар жоқ"
    await update.message.reply_text(f"👑 **АДМИН ПАНЕЛІ**\n\n👥 Қатысушылар: {len(REGISTERED_PLAYERS)}/{PLAYER_LIMIT}\n\n📋 **Тізім:**\n{players_list}", parse_mode="Markdown")


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN табылмады.")

    app = Application.builder().token(BOT_TOKEN).build()

    # Барлық түймелер мен conversation логикасын біріктіретін басты тұс
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(buttons_handler, pattern="^(start_reg|find_1v1|find_3v3|home|rules|my_profile|change_lang|set_lang_.*)$")
        ],
        states={
            WAITING_FOR_BS_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_bs_id)],
            WAITING_FOR_RECEIPT: [MessageHandler(filters.PHOTO | filters.Document.ALL | filters.TEXT, get_receipt)],
            WAITING_MATCH_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_matchmaking)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_conversation),
            CallbackQueryHandler(buttons_handler, pattern="^(home|change_lang|set_lang_.*)$")
        ],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(admin_decision, pattern="^(approve|reject)_"))
    # Жалпы callback handler басқа батырмалар үшін де қызмет етеді
    app.add_handler(CallbackQueryHandler(buttons_handler))

    logger.info("VIREON Bot (Ultra Upgrade) іске қосылды!")
    app.run_polling()


if __name__ == "__main__":
    main()
