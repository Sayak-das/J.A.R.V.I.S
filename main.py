import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import google.generativeai as genai
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv
import re

load_dotenv() 

genai.configure(api_key=os.environ["API_KEY"])
recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = os.getenv("NEWS_API")

def clean_text(text):
    # Remove unwanted characters
    text = re.sub(r'[*"“”]', '', text)  # Remove asterisks, quotes, and smart quotes
    text = re.sub(r'[,]', '', text)  # Remove commas
    # Optionally, replace punctuation with spaces
    text = re.sub(r'[.]', '.', text)  # Keep periods for natural pauses
    text = re.sub(r'[!]', '!', text)  # Keep exclamation marks for emphasis
    text = re.sub(r'[?]', '?', text)  # Keep question marks for natural intonation
    return text

def speak(text):
    cleaned_text = clean_text(text)
    tts = gTTS(cleaned_text)
    tts.save('temp.mp3') 

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    genai.configure(api_key=os.environ['API_KEY'])
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = command

    response = model.generate_content(prompt)
    return response.text

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open twitter" in c.lower():
        webbrowser.open("https://twitter.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open reddit" in c.lower():
        webbrowser.open("https://reddit.com")
    elif "open amazon" in c.lower():
        webbrowser.open("https://amazon.com")
    elif "open netflix" in c.lower():
        webbrowser.open("https://netflix.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open stackoverflow" in c.lower():
        webbrowser.open("https://stackoverflow.com")
    elif "open wikipedia" in c.lower():
        webbrowser.open("https://wikipedia.org")
    elif "open pinterest" in c.lower():
        webbrowser.open("https://pinterest.com")
    elif "open quora" in c.lower():
        webbrowser.open("https://quora.com")
    elif "open yahoo" in c.lower():
        webbrowser.open("https://yahoo.com")
    elif "open bing" in c.lower():
        webbrowser.open("https://bing.com")
    elif "open apple" in c.lower():
        webbrowser.open("https://apple.com")
    elif "open microsoft" in c.lower():
        webbrowser.open("https://microsoft.com")
    elif "open ebay" in c.lower():
        webbrowser.open("https://ebay.com")
    elif "open twitch" in c.lower():
        webbrowser.open("https://twitch.tv")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song} in the music library.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
                word = recognizer.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)
        except Exception as e:
            print(f"Error: {str(e)}")
