import os
import datetime
import openai
import speech_recognition as sr
import pyttsx3
import webbrowser
from config import apikey  # You're importing your API key from a separate configuration file
import random

# Initialize an empty chat string
chatStr = ""

# Function to interact with the AI using the OpenAI API
def chat(query):
    openai.api_key = apikey

    # Create a prompt by formatting the user's query
    text = f"Human: {query} \n ********************\n\n"

    # Generate a response from the AI
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

# Function to interact with the AI with a conversation prompt
def ai(prompt):
    openai.api_key = apikey
    chatStr = f"Human: {prompt} \n"  # Initialize chatStr with the user's prompt

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

# Function to make the AI say something using text-to-speech
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech input
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

# Main program starts here
if __name__ == '__main__':
    print('PyCharm')
    engine = pyttsx3.init()
    say("Hello, I am Quantum")
    print("Listening....")
    command = takeCommand()

    # List of websites to open based on user's command
    sites = [["youtube", "https://youtube.com"], ["facebook", "https://facebook.com"],
             ["linkedin", "https://www.linkedin.com"], ["google", "https://google.com"]]
    say("You said: " + command)

    # Check if the user's command contains a website keyword and open the corresponding website
    for site in sites:
        if f"open {site[0]}".lower() in command.lower():
            say(f"opening {site[0]} sir..")
            webbrowser.open(site[1])

    # Play music if the user's command contains "play music"
    if "play music" in command.lower():
        Song_path = r"C:\Users\hp\Desktop\Ai bot\On-My-Way.mp3"
        os.startfile(Song_path)
        say("Playing music sir...")

    # Display the current time if the user's command contains "time"
   
    if "time" in command.lower():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"Sir, the time is {current_time}")

    # If the user's command contains "Artificial intelligence", interact with the AI using the ai() function
    if "Artificial intelligence".lower() in command.lower():
        ai_response = ai(prompt=command)
        print("AI Response:", ai_response)
    else:
        # If not, interact with the AI using the chat() function
        chat_response = chat(command)
        say("Chat Response: " + chat_response)
