import os
import openai
from  dotenv import load_dotenv

import pyaudio
import speech_recognition as sr
import openai

import keyboard

import threading

load_dotenv()

openai.api_key = os.getenv("CLIENT_KEY")

def textGenerator():
    #intializing the microphone
    reader = sr.Recognizer()
    reader.pause_threshold = 0.6
    reader.non_speaking_duration = 0.2  
    #read microphone
    
    with sr.Microphone() as source:
        print("Howdy to start listening")
        while True:
            audio = reader.listen(source)
            try:
                text = reader.recognize_google(audio)
                if "howdy" in text.lower(): #start listening when "Howdy"
                    print("Listening......")
                    break
                if keyboard.is_pressed('q'):  
                    print("Stopped listening.")
                    return None
            except:
                pass
        audio = reader.listen(source)
        try:
            text = reader.recognize_google(audio)
            print("You said : {}".format(text))
            return text
        except:
            if keyboard.is_pressed('q'):  # stop listening when 'q' is pressed
                print("Stopped listening.")
                return None
            print("Sorry could not recognize what you said")
            return None
            
    q

def openChat(prompt):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

if __name__ == '__main__':
   while True:
        prompt = textGenerator()
        if prompt is not None:
            response = openChat(prompt)
            print("AI: ", response)
        else:
            break