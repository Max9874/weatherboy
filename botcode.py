import telebot
import requests
import datetime
import json

TOKEN = "6903276271:AAFSFrjMsSNG3pCU6Lu0WwfY1o3le0kkzvo"
climate_API = "f8b52b361-6250-4531-b539-987bd2d5e90"
start_text = open("starttext.txt", "r")

bot = telebot.TeleBot(TOKEN)


def temperature_converter(temperature):
    x_variable = round((temperature - 32) / 1.8, 0)

    return int(x_variable)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, start_text.read())


@bot.message_handler(content_types=["text"])
def weather(message):
    date = datetime.datetime.now().date()
    try:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{message.text}/{date}/?key=C59PD26W2JFRMD7JMLBGUQBGV"
        response = requests.get(url)
        data = json.loads(response.text)
        temperature = temperature_converter(data["currentConditions"]["temp"])
        feels_like = temperature_converter(data["currentConditions"]["feelslike"])
        pressure = data["currentConditions"]["pressure"]
        wind_speed = data["currentConditions"]["windspeed"]
        conditions = data["currentConditions"]["conditions"]
        preciptype = data["currentConditions"]["preciptype"]
        precipprob = data["currentConditions"]["precipprob"]
        description = data["description"]
        address = data["resolvedAddress"]
        print(data)
        if preciptype is None:
            info_output = f"\t{message.text}\nWeather now: {temperature} Cº, no precip\nFeels like: {feels_like} Cº\n" \
                          f"Wind speed: {wind_speed} m/s\nPrecip probability: {precipprob} %\n{conditions}." \
                          f" Forecast: {description}\n" \
                          f"Pressure: {pressure} millibars\n"
            bot.send_message(message.chat.id, info_output)
        else:
            info_output = f"\t{message.text}\nWeather now: {temperature} Cº, {preciptype}\nFeels like: {feels_like} Cº\n" \
                          f"Wind speed: {wind_speed} m/s\nPrecip probability: {precipprob} %\n{conditions}." \
                          f" Forecast: {description}\n" \
                          f"Pressure: {pressure} millibars\n"
            bot.send_message(message.chat.id, info_output)
    except json.decoder.JSONDecodeError:
        bot.send_message(message.chat.id, "Name of the city is incorrect. Try again")
        print("City name is incorrect")


bot.polling(none_stop=True)
