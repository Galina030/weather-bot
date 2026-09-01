import os
import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 57.10,
    "longitude": 65.34,
    "daily": "temperature_2m_max,temperature_2m_min,weathercode,windspeed_10m_max,relative_humidity_2m_mean,precipitation_probability_max",
    "timezone": "Asia/Yekaterinburg",
    "forecast_days": 3
}

response = requests.get(url, params=params)
data = response.json()
weather_groups = {
    "ясно": ([0], "☀️"),
    "облачно": ([1, 2, 3], "☁️"),
    "туман": ([45, 48], "🌫️"),
    "морось": ([51, 53, 55, 56, 57], "🌦️"),
    "дождь": ([61, 63, 65, 66, 67], "🌧️"),
    "ливень": ([80, 81, 82], "⛈️"),
    "снег": ([71, 73, 75, 77, 85, 86], "❄️"),
    "гроза": ([95, 96, 99], "⚡")
}

def get_weather_text(code):
    for name, (codes, emoji) in weather_groups.items():
        if code in codes:
            return name, emoji
    return "неизвестно", "🌀"

days = ["Сегодня", "Завтра", "Послезавтра"]

message = "Доброе утро, Тюмень! ☀️ Вот какой сегодня день нас ждёт.\n\n"

for i in range(3):
    date = data["daily"]["time"][i]
    temp_max = round(data["daily"]["temperature_2m_max"][i])
    temp_min = round(data["daily"]["temperature_2m_min"][i])
    wind = round(data["daily"]["windspeed_10m_max"][i])
    humidity = round(data["daily"]["relative_humidity_2m_mean"][i])
    rain_chance = round(data["daily"]["precipitation_probability_max"][i])
    code = data["daily"]["weathercode"][i]

    name, emoji = get_weather_text(code)

    year, month, day = date.split("-")
    date = f"{day}.{month}.{year}"

    message += f"{days[i]}, {date}\n"
    message += f"{emoji} {name.capitalize()}\n"
    message += f"Температура: от {temp_min}°C до {temp_max}°C\n"
    message += f"Ветер: до {wind} км/ч\n"
    message += f"Влажность: {humidity}%\n"
    message += f"Вероятность осадков: {rain_chance}%\n\n"

message += "Пусть день будет тёплым и добрым, а настроение — солнечным, чем бы вы сегодня ни занимались! А ещё у тебя всё получится 🌞"

print(message)

bot_token = os.environ["BOT_TOKEN"]
chat_id = "710040547"

send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
send_params = {
    "chat_id": chat_id,
    "text": message
}
send_response = requests.post(send_url, data=send_params)
print("Отправлено, статус:", send_response.status_code)
