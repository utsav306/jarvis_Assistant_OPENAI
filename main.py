import datetime
import openai
import pyttsx3
import speech_recognition as sr
import webbrowser
from config import apikey
import os
import  random
import string
import requests
import json

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Utsav: {query}\nJarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def weather(city):
    url = "https://weather-by-api-ninjas.p.rapidapi.com/v1/weather"
    say("Whats the city name you want to know weather about : \n")
    city = takecommand()
    if city == "Some error occured":
        say("Some error occured in speech recognition , please enter the city name you want to know weather about :")
        print("Enter the city name : ")
        city = input()

    querystring = {"city": city}

    headers = {
        "X-RapidAPI-Key": "61edba90famsha86f9cf13c233a7p10921ejsn6156531a5740",
        "X-RapidAPI-Host": "weather-by-api-ninjas.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    wdic = json.loads(response.text)
    humi = wdic.get("humidity")
    if humi is None:
        humi = "not found"
    min_temp = wdic.get("min_temp")
    if min_temp is None:
        min_temp = "not found"

    max_temp = wdic.get("max_temp")
    if max_temp is None:
        max_temp = "not found"

    feel = wdic.get("feels_like")
    if feel is None:
        feel = "not found"

    print(f"Maximum Temperature : {max_temp} \n")
    print(f"Minimum Temperature : {min_temp} \n")
    print(f"Humidity : {humi} \n")
    print(f"Feels Like : {feel} \n")

    say(f"The maximum temperature for {city} will be {max_temp} degree Celsius and the minimum temperature will be {min_temp} degree Celsius. The humidity is {humi} percent and It feels like {feel} degree centigrade.")


# {'cloud_pct': 75, 'temp': 28, 'feels_like': 33, 'humidity': 89, 'min_temp': 28, 'max_temp': 28, 'wind_speed': 4.63, 'wind_degrees': 170, 'sunrise': 1686957718, 'sunset': 1687006361}



def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")


    random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10))


    invalid_chars = '\\/:*?"<>|'
    prompt_filename = ''.join(c for c in prompt if c not in invalid_chars).strip()


    file_path = f"Openai\\{random_filename}_{prompt_filename}.txt"

    with open(file_path, "w") as f:
        f.write(text)
def say(text):
    engine = pyttsx3.init()
    engine.setProperty('device', '0')
    engine.say(text)
    engine.runAndWait()
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        r.pause_threshold = 1
        r.energy_threshold = 200

        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(query)
            return query
        except Exception as e:
            query="Some error occured"
            return query
if __name__ == '__main__':

    say("Hello I am Jarvis , Assistant of Master, Utsav !!")
    while True:
        print("Listening....")
        query=takecommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "the time" in query:
            strftime=datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir ,the time is{strftime} ")
        elif "weather update".lower() in query.lower():
            weather(query)
        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        elif "Exit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)