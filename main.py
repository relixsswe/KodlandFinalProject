import telebot
from telebot import types
import botlogic  # Убедись, что botlogic.py из прошлого шага лежит рядом!

# Инициализируем бота
bot = telebot.TeleBot("8843433411:AAHWDmRkJCKADNVeupwPxCWBxzwDqmyhGhI")

# Страницы статьи о глобальном потеплении
PAGES = [
    "📰 *Глобальное потепление: Часть 1. Что происходит?*\n\n"
    "Глобальное потепление — это постепенный рост средней температуры на Земле за последние 100-150 лет. "
    "Главная причина — *деятельность человека*. Сжигание угля, нефти и газа приводит к выбросам парниковых газов. "
    "Они создают вокруг планеты подобие «теплицы», которая задерживает тепло Солнца.",
    
    "📰 *Глобальное потепление: Часть 2. Последствия*\n\n"
    "Изменение климата — это не просто жаркое лето. Это глобальная угроза:\n"
    "• Ускоренное таяние ледников и вечной мерзлоты\n"
    "• Повышение уровня Мирового океана (угроза затопления городов)\n"
    "• Частые погодные аномалии: сильнейшие засухи, лесные пожары, наводнения и ураганы.",
    
    "📰 *Глобальное потепление: Часть 3. Мировые шаги*\n\n"
    "Государства по всему миру объединяются для борьбы с кризисом. Страны подписывают соглашения "
    "(например, *Парижское соглашение*), чтобы ограничить выбросы заводов. Активно развиваются "
    "эко-движения, такие как Гринпис и WWF, призывающие спасти экосистему планеты."
]

# Клавиатура для перелистывания страниц статьи
def get_article_keyboard(page=0):
    markup = types.InlineKeyboardMarkup()
    buttons = []

    if page > 0:
        buttons.append(types.InlineKeyboardButton("⬅️ Назад", callback_data=f"article_page_{page-1}"))
    
    if page < len(PAGES) - 1:
        buttons.append(types.InlineKeyboardButton("Вперед ➡️", callback_data=f"article_page_{page+1}"))
        
    markup.row(*buttons)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn_hello = types.KeyboardButton("👋 Привет")
    btn_pass = types.KeyboardButton("🔑 Сгенерировать пароль")
    btn_emodji = types.KeyboardButton("😊 Рандомный смайлик")
    btn_coin = types.KeyboardButton("🪙 Подбросить монетку")
    btn_guess = types.KeyboardButton("🎲 Угадай число")
    btn_bye = types.KeyboardButton("🚪 Пока")
    btn_Statya = types.KeyboardButton("📰 Статья о потеплении")
    btn_help_planet = types.KeyboardButton("🌱 Как помочь планете?")
    
    markup.add(btn_hello, btn_pass, btn_emodji, btn_coin, btn_guess, btn_bye, btn_Statya, btn_help_planet)
    
    bot.send_message(
        message.chat.id, 
        "Привет! Я твой Telegram бот. Выбери нужное действие в меню ниже или используй команды!", 
        reply_markup=markup
    )

# --- ОБРАБОТЧИКИ КОМАНД ---

@bot.message_handler(commands=['hello'])
def cmd_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def cmd_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['pass'])
def cmd_password(message):
    password = botlogic.gen_pass(10)
    bot.reply_to(message, f"Вот твой сгенерированный пароль: {password}")

@bot.message_handler(commands=['emodji'])
def cmd_emodji(message):
    emodji = botlogic.gen_emodji()
    bot.reply_to(message, f"Вот эмоджи: {emodji}")

@bot.message_handler(commands=['coin'])
def cmd_coin(message):
    coin = botlogic.flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")

@bot.message_handler(commands=['guess'])
def cmd_guess(message):
    number = botlogic.gen_guess()
    bot.reply_to(message, f"Загадано число от 1 до 10. Твое случайное число удачи сегодня: {number}")

# --- ИНЛАЙН ПЕРЕЛИСТЫВАНИЕ СТАТЬИ ---

@bot.callback_query_handler(func=lambda call: call.data.startswith('article_page_'))
def handle_article_pages(call):
    data_parts = call.data.split('_')
    page = int(data_parts[2]) # ИСПРАВЛЕНО: Добавлен индекс [2] для корректного сплита
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=PAGES[page],
        parse_mode="Markdown",
        reply_markup=get_article_keyboard(page)
    )
    bot.answer_callback_query(call.id)

# --- ОБРАБОТКА ТЕКСТОВЫХ КНОПОК МЕНЮ ---

@bot.message_handler(content_types=['text'])
def handle_menu_buttons(message):
    if message.text == "👋 Привет":
        bot.reply_to(message, "Привет! Как дела?")
        
    elif message.text == "🔑 Сгенерировать пароль":
        password = botlogic.gen_pass(10)
        bot.reply_to(message, f"Вот твой сгенерированный пароль: {password}")
        
    elif message.text == "😊 Рандомный смайлик":
        emodji = botlogic.gen_emodji()
        bot.reply_to(message, f"Вот эмоджи: {emodji}")
        
    elif message.text == "🪙 Подбросить монетку":
        coin = botlogic.flip_coin()
        bot.reply_to(message, f"Монетка выпала так: {coin}")
        
    elif message.text == "🎲 Угадай число":
        number = botlogic.gen_guess()
        bot.reply_to(message, f"Загадано число от 1 до 10. Попробуй угадать! Твое случайное число: {number}")
        
    elif message.text == "🚪 Пока":
        bot.reply_to(message, "Пока! Удачи!")
        
    elif message.text == "📰 Статья о потеплении":
        # ИСПРАВЛЕНО: Передаем PAGES[0] (первый элемент), а не весь список PAGES целиком
        bot.send_message(
            message.chat.id, 
            PAGES[0], 
            parse_mode="Markdown", 
            reply_markup=get_article_keyboard(0)
        )
        
    elif message.text == "🌱 Как помочь планете?":
        help_text = (
            "🌍 *Как лично ты можешь помочь остановить глобальное потепление?*\n\n"
            "Каждый человек влияет на климат. Вот простые шаги, которые спасут планету:\n\n"
            "1. 💡 *Экономь электроэнергию:* Выключай свет и приборы из розетки. Меньше потребления — меньше работы загрязняющих ТЭЦ.\n"
            "2. ♻️ *Сортируй мусор и используй меньше пластика:* Переработка отходов выбрасывает в разы меньше СО2, чем создание новых вещей.\n"
            "3. 🚴 *Выбирай экологичный транспорт:* Чаще ходи пешком, катайся на велосипеде или самокате. Автомобили — один из главных источников парниковых газов.\n"
            "4. 🌳 *Сажай деревья и береги растения:* Деревья — это легкие Земли, они буквально «впитывают» углекислый газ из атмосферы.\n"
            "5. 🛍️ *Откажись от избыточного потребления:* Покупай только то, что действительно нужно. Производство и доставка товаров сжигают тонны топлива."
        )
        bot.send_message(message.chat.id, help_text, parse_mode="Markdown")
        
    else:
        bot.reply_to(message, "Я не знаю такой команды. Пожалуйста, используйте кнопки меню.")

if __name__ == '__main__':
    print("Бот успешно запущен...")
    bot.infinity_polling()