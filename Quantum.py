import os
import datetime
import openai
import speech_recognition as sr
import pyttsx3
import webbrowser
from config import apikey
import random

chatStr = ""
def chat(query):
    openai.api_key = apikey
    text = f"Human: {query} \n ********************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    generated_text = response["choices"][0]["text"]
    print("AI:", generated_text)
    text += f"AI: {generated_text}\n"
    return generated_text

def ai(prompt):
    openai.api_key = apikey
    chatStr = f"Human: {prompt} \n"  # Initialize chatStr with user's prompt

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    generated_text = response["choices"][0]["text"]
    print("AI:", generated_text)
    chatStr += f"AI: {generated_text}\n"
    return generated_text


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"you said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't understand what you said.")
            say("Sorry, I didn't understand what you said.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an issue connecting to Google's servers.")
            say("Sorry, there was an issue connecting to Google's servers.")
            return ""


if __name__ == '__main__':
    print('PyCharm')
    engine = pyttsx3.init()
    say("Hello, I am Quantum")
    print("Listening....")
    command = takeCommand()
    sites = [["youtube", "https://youtube.com"], ["facebook", "https://facebook.com"],
             ["linkedin", "https://www.linkedin.com"], ["google", "https://google.com"]]
    say("You said: " + command)

    for site in sites:
        if f"open {site[0]}".lower() in command.lower():
            say(f"opening {site[0]} sir..")
            webbrowser.open(site[1])

    if "play music" in command.lower():
        Song_path = r"C:\Users\hp\Desktop\Ai bot\On-My-Way.mp3"
        os.startfile(Song_path)
        say("Playing music sir...")

    if "time" in command.lower():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"Sir, the time is {current_time}")

    if "Artificial intelligence".lower() in command.lower():
        ai_response = ai(prompt=command)
        print("AI Response:", ai_response)
    else:
        chat_response = chat(command)
        say("Chat Response: " + chat_response)
