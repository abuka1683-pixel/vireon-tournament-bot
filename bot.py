import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Logging орнотуу
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Бот токені
TOKEN = os.getenv("BOT_TOKEN", "СЕНИН_BOT_TOKENИҢДИ_УШУЛ ЖЕРГЕ_ЖАЗ")

# Тілдерге жараша мәтіндер (Қазақша, Русский, English)
TEXTS = {
    'KK': {
        'main_menu': "Басты мәзірге қош келдіңіз! Төмендегі батырмалардың бірін таңдаңыз:",
        'btn_lang': "🌐 Тілді өзгерту",
        'btn_admin': "👑 Админ профилі",
        'btn_brawl': "⚔️ Brawl Турнири",
        'select_lang': "Тілді таңдаңыз / Выберите язык / Select language:",
        'admin_info': "👑 **Админ профилі және байланыс**\n\n"
                      "• Бот бойынша сұрақтар мен қолдау\n"
                      "• TikTok: Nexor6589\n"
                      "• YouTube: Nexor6589\n\n"
                      "Біздің әлеуметтік желілерге жазылуды ұмытпаңыз!",
        'brawl_menu': "⚔️ **Brawl Турнири мәзірі**\n\nҚажетті бөлімді таңдаңыз:",
        'brawl_info': "ℹ️ **Турнир туралы ақпарат:**\nБұл жерде 1v1 және 3v3 форматтарында таза және әділеттүү бәсекелер өтеді!",
        'brawl_reg': "📝 **Турнирге тіркелу:**\nТіркелу үшін өзіңіздің Game ID'ңізді және қатысатын форматыңызды админге жіберіңіз.",
        'brawl_channels': "📢 **Турнир арналары:**\nБарлық жаңалықтар мен сеткалар біздің ресми арнада жарияланады.",
        'brawl_duels': "🥊 **1v1 және 3v3 Дуэльдер:**\n1v1 немесе 3v3 форматын таңдап, қарсыласыңызбен күшіңізді сынасыңыз!",
        'back': "⬅️ Басты мәзірге қайту"
    },
    'RU': {
        'main_menu': "Добро пожаловать в главное меню! Выберите одну из кнопок ниже:",
        'btn_lang': "🌐 Сменить язык",
        'btn_admin': "👑 Профиль админа",
        'btn_brawl': "⚔️ Турнир Brawl",
        'select_lang': "Выберите язык / Тілді таңдаңыз / Select language:",
        'admin_info': "👑 **Профиль админа и связь**\n\n"
                      "• Вопросы по боту и поддержка\n"
                      "• TikTok: Nexor6589\n"
                      "• YouTube: Nexor6589\n\n"
                      "Не забудьте подписаться на наши соцсети!",
        'brawl_menu': "⚔️ **Меню Турнира Brawl**\n\nВыберите нужный раздел:",
        'brawl_info': "ℹ️ **Информация о турнире:**\nЗдесь проводятся честные турниры в форматах 1v1 и 3v3!",
        'brawl_reg': "📝 **Регистрация на турнир:**\nДля регистрации отправьте свой Game ID и формат участия админу.",
        'brawl_channels': "📢 **Каналы турнира:**\nВсе новости и сетки публикуются в нашем официальном канале.",
        'brawl_duels': "🥊 **Дуэли 1v1 и 3v3:**\nВыбирайте формат 1v1 или 3v3 и сражайтесь с соперниками!",
        'back': "⬅️ Назад в главное меню"
    },
    'EN': {
        'main_menu': "Welcome to the main menu! Select one of the options below:",
        'btn_lang': "🌐 Change Language",
        'btn_admin': "👑 Admin Profile",
        'btn_brawl': "⚔️ Brawl Tournament",
        'select_lang': "Select language / Тілді таңдаңыз:",
        'admin_info': "👑 **Admin Profile & Contacts**\n\n"
                      "• Bot support & questions\n"
                      "• TikTok: Nexor6589\n"
                      "• YouTube: Nexor6589\n\n"
                      "Don't forget to follow our social media!",
        'brawl_menu': "⚔️ **Brawl Tournament Menu**\n\nSelect a section:",
        'brawl_info': "ℹ️ **Tournament Info:**\nFair tournaments in 1v1 and 3v3 formats!",
        'brawl_reg': "📝 **Registration:**\nSend your Game ID and selected format to the admin to register.",
        'brawl_channels': "📢 **Channels:**\nAll news and brackets are published in our official channel.",
        'brawl_duels': "🥊 **1v1 & 3v3 Duels:**\nChoose 1v1 or 3v3 format and challenge your opponents!",
        'back': "⬅️ Back to Main Menu"
    }
}

# Қолданушылардың таңдаған тілі (Әдепкі бойынша: KK)
user_languages = {}

def get_user_lang(user_id):
    return user_languages.get(user_id, 'KK')

# Басты мәзір пернетақтасы (Тек 3 батырма)
def main_keyboard(lang):
    t = TEXTS[lang]
    keyboard = [
        [InlineKeyboardButton(t['btn_lang'], callback_data='menu_lang')],
        [InlineKeyboardButton(t['btn_admin'], callback_data='menu_admin')],
        [InlineKeyboardButton(t['btn_brawl'], callback_data='menu_brawl')]
    ]
    return InlineKeyboardMarkup(keyboard)

# /start командасы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    await update.message.reply_text(
        TEXTS[lang]['main_menu'],
        reply_markup=main_keyboard(lang)
    )

# Батырмалардың әрекетін өңдеу
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    t = TEXTS[lang]

    data = query.data

    # Басты мәзірге қайту
    if data == 'main_menu':
        await query.edit_message_text(
            t['main_menu'],
            reply_markup=main_keyboard(lang)
        )

    # 1. Тілді таңдау мәзірі
    elif data == 'menu_lang':
        keyboard = [
            [InlineKeyboardButton("🇰🇿 Қазақша", callback_data='set_lang_KK')],
            [InlineKeyboardButton("🇷🇺 Русский", callback_data='set_lang_RU')],
            [InlineKeyboardButton("🇬🇧 English", callback_data='set_lang_EN')],
            [InlineKeyboardButton(t['back'], callback_data='main_menu')]
        ]
        await query.edit_message_text(t['select_lang'], reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith('set_lang_'):
        new_lang = data.split('_')[2]
        user_languages[user_id] = new_lang
        new_t = TEXTS[new_lang]
        await query.edit_message_text(
            new_t['main_menu'],
            reply_markup=main_keyboard(new_lang)
        )

    # 2. Админ профилі
    elif data == 'menu_admin':
        keyboard = [
            [InlineKeyboardButton("🎵 TikTok", url="https://tiktok.com/@Nexor6589")],
            [InlineKeyboardButton("📺 YouTube", url="https://youtube.com/@Nexor6589")],
            [InlineKeyboardButton(t['back'], callback_data='main_menu')]
        ]
        await query.edit_message_text(
            t['admin_info'],
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 3. Brawl Турнири мәзірі (ішкі батырмалар)
    elif data == 'menu_brawl':
        keyboard = [
            [InlineKeyboardButton("ℹ️ Ақпарат", callback_data='brawl_info')],
            [InlineKeyboardButton("📝 Тіркелу", callback_data='brawl_reg')],
            [InlineKeyboardButton("📢 Арналар", callback_data='brawl_channels')],
            [InlineKeyboardButton("🥊 1v1 / 3v3 Дуэльдер", callback_data='brawl_duels')],
            [InlineKeyboardButton(t['back'], callback_data='main_menu')]
        ]
        await query.edit_message_text(
            t['brawl_menu'],
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # Brawl Турнирінің ішкі бөлімдері
    elif data == 'brawl_info':
        keyboard = [[InlineKeyboardButton(t['back'], callback_data='menu_brawl')]]
        await query.edit_message_text(t['brawl_info'], parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'brawl_reg':
        keyboard = [[InlineKeyboardButton(t['back'], callback_data='menu_brawl')]]
        await query.edit_message_text(t['brawl_reg'], parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'brawl_channels':
        keyboard = [[InlineKeyboardButton(t['back'], callback_data='menu_brawl')]]
        await query.edit_message_text(t['brawl_channels'], parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'brawl_duels':
        keyboard = [[InlineKeyboardButton(t['back'], callback_data='menu_brawl')]]
        await query.edit_message_text(t['brawl_duels'], parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Бот ішке кирди...")
    app.run_polling()
