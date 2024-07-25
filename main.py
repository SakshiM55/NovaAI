import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import pyttsx3
from config import apikey
from unittest.mock import patch, Mock

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\n Nova: "
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ],
        temperature=0.7
    )
    answer = response.choices[0].message['content'].strip()
    say(answer)
    chatStr += f"{answer}\n"
    return answer

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    text += response.choices[0].message['content'].strip()
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(e)
            return "Some Error Occurred. Sorry from Nova"

if __name__ == '__main__':
    print('Welcome to Nova A.I')
    say("Nova A.I")

    while True:
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} ma'am...")
                webbrowser.open(site[1])
        if "open music" in query:
            musicPath = r"C:\Users\mohit\Downloads\tvari-hawaii-vacation-159069.mp3"  # Use raw string
            os.startfile(musicPath)
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Ma'am, the time is {hour} hours and {minute} minutes")
        elif "open vscode".lower() in query.lower():
            vscodePath = r"C:\Users\mohit\AppData\Local\Programs\Microsoft VS Code\Code.exe"  # Use raw string
            os.startfile(vscodePath)
        elif "using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        elif "Nova quit".lower() in query.lower():
            exit()
        elif "reset chat".lower() in query.lower():
            chatStr = ""
        else:
            chat(query)
