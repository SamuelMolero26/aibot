
import openai
from dotenv import load_dotenv
import pyaudio
import speech_recognition as sr
import openai
import os
from dotenv import load_dotenv
import keyboard
import RLPCD
from RPLCD import CharLCD




load_dotenv()

openai.api_key = os.getenv("CLIENT_KEY")

def textGenerator():
    # initializing the microphone
    reader = sr.Recognizer()
    reader.pause_threshold = 0.6
    reader.non_speaking_duration = 0.2  
    
    # read microphone
    with sr.Microphone() as source:
        print("Howdy to start listening")
        while True:
            audio = reader.listen(source)
            try:
                text = reader.recognize_google(audio)
                if "howdy" in text.lower(): # start listening when "Howdy"
                    print("Listening......")
                    break
                if keyboard.is_pressed():  
                    print("Stopped listening.")
                    return None
            except:
                pass
        if keyboard.is_pressed(): 
            print("Stopped listening.")
            return None
        audio = reader.listen(source)
        try:
            text = reader.recognize_google(audio)
            print("You said : {}".format(text))
            return text
        except:
            if keyboard.is_pressed(): 
                print("Stopped listening.")
                return None
            print("Sorry could not recognize what you said")
            return None

def openChat(prompt):
    if prompt.lower() == "read notification":
        todos = ['Finish the project', 'Do the laundry', 'Buy groceries', 'Call mom']
        print("Reading notifications...")
        return todos
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()

def display_response(response):
    lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23])
    lcd.write_string(u'{}'.format(response))
   

if __name__ == '__main__':
    while True:
        prompt = textGenerator()
        if prompt is not None:
            response = openChat(prompt)
            display_response(response)
            print("AI: ", response)
        else:
            break