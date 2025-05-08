import telebot
import requests
import openai

# ====== ВСТАВЬ СЮДА СВОИ ТОКЕНЫ ======
TELEGRAM_TOKEN = '7753608741:AAGuR4R7wwwPKLgViJ-_nwnBLVk-FJ4r7KQ'
OPENAI_API_KEY = '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'
# ====================================

bot = telebot.TeleBot('7753608741:AAGuR4R7wwwPKLgViJ-_nwnBLVk-FJ4r7KQ')
openai.api_key = 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

# ===== ФУНКЦИЯ ПОГОДЫ =====
def get_weather(city):
    url = f"https://api.open-meteo.com/v1/forecast?latitude=55.75&longitude=37.61&current_weather=true"
    params = {
        "current_weather": "true",
        "timezone": "Europe/Moscow"
    }
    response = requests.get(url, params=params)
    data = response.json()
    temp = data['current_weather']['temperature']
    wind = data['current_weather']['windspeed']
    return f"Сейчас в {city}: {temp}°C, ветер {wind} км/ч."

# ===== ФУНКЦИЯ YOUTUBE =====
def get_youtube_link(query):
    return f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"

# ===== ФУНКЦИЯ GPT =====
def ask_gpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response['choices'][0]['message']['content']

# ======= ОБРАБОТЧИКИ КОМАНД =======

@bot.message_handler(commands=['start'])
def start(message):
    text = ("Привет! Я умный бот-информатор!\n\n"
            "Вот что я умею:\n"
            "/weather [город] — Узнать погоду\n"
            "/schedule — Посмотреть расписание\n"
            "/youtube [запрос] — Найти видео на YouTube\n"
            "/ask [вопрос] — Задать вопрос ChatGPT\n")
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['weather'])
def weather(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) == 2:
        city = parts[1]
        weather_info = get_weather(city)
        bot.send_message(message.chat.id, weather_info)
    else:
        bot.send_message(message.chat.id, 'Напиши команду так: /weather Москва')

@bot.message_handler(commands=['schedule'])
def schedule(message):
    schedule_text = ("📅 Расписание на сегодня:\n\n"
                     "1️⃣ Математика — 09:00\n"
                     "2️⃣ Русский язык — 10:00\n"
                     "3️⃣ Информатика — 11:30\n"
                     "4️⃣ Обществознание — 13:00")
    bot.send_message(message.chat.id, schedule_text)

@bot.message_handler(commands=['youtube'])
def youtube(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) == 2:
        query = parts[1]
        link = get_youtube_link(query)
        bot.send_message(message.chat.id, f'🔗 Вот ссылка на YouTube:\n{link}')
    else:
        bot.send_message(message.chat.id, 'Напиши команду так: /youtube котики')

@bot.message_handler(commands=['ask'])
def ask(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) == 2:
        question = parts[1]
        reply = ask_gpt(question)
        bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, 'Напиши команду так: /ask Что такое Python?')

# ======= ЗАПУСК =======
bot.polling(none_stop=True)
