import speech_recognition as sr
import pyttsx3
import time

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    # Implement your command processing logic here
    print("Command received:", command)

if __name__ == "__main__":
    speak("Initializing JARVIS....")

    while True:
        # Listen for the wake word "Jarvis"
        r = sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                audio = r.listen(source, timeout=5)  # Increase timeout
            word = r.recognize_google(audio)
            print("Heard word:", word)  # Debugging info
            if word.lower() == "jarvis":
                speak("Yes?")
                time.sleep(1)  # Short delay to prevent overlapping recognition
                with sr.Microphone() as source:
                    print("Jarvis Active... Please say your command.")
                    r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)  # Adjust phrase_time_limit
                    command = r.recognize_google(audio)
                    print("Heard command:", command)  # Debugging info
                    processCommand(command)
                time.sleep(1)  # Short delay after processing the command to prevent immediate reactivation
        
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except Exception as e:
            print("Error: {0}".format(e))
