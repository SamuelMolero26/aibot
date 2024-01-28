import threading
import time
import drivers
import RPi.GPIO as GPIO
import openai
import os
from dotenv import load_dotenv
import pyaudio
import speech_recognition as sr
import keyboard

# Load the driver and set it to "display"
display = drivers.Lcd()

# Placeholder for the response text
response_text = ""

# Sound sensor GPIO pin (adjust as needed)
SOUND_SENSOR_GPIO_PIN = 24

# Threshold for loud sound detection (adjust as needed)
LOUD_SOUND_THRESHOLD = 300

# Load the OpenAI API key
load_dotenv()
openai.api_key = os.getenv("CLIENT_KEY")

# Function to display text on the LCD
def display_text(text):
    display.lcd_clear()
    display.lcd_display_string(text, 1)

# Function to continuously update the LCD with response text
def update_lcd():
    while True:
        display_text(response_text)
        time.sleep(1)

# Function to handle loud sound events
def handle_loud_sound(channel):
    global response_text
    response_text = "Loud Sound Detected!"

# Function to generate text from speech
def textGenerator():
    reader = sr.Recognizer()
    reader.pause_threshold = 0.6
    reader.non_speaking_duration = 0.2  
    
    # Read from the microphone
    with sr.Microphone() as source:
        print("Howdy to start listening")
        
        # Wait for "Howdy" to start listening
        while True:
            audio = reader.listen(source)
            try:
                text = reader.recognize_google(audio)
                if "howdy" in text.lower():
                    print("Listening......")
                    break
                if keyboard.is_pressed('esc'):
                    print("Stopped listening.")
                    return None
            except:
                pass

        # Listen for the actual command
        audio = reader.listen(source)
        try:
            text = reader.recognize_google(audio)
            print("You said : {}".format(text))
            return text
        except:
            print("Sorry could not recognize what you said")
            return None

if __name__ == '__main__':
    # Set up interrupt for sound sensor
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOUND_SENSOR_GPIO_PIN, GPIO.IN)
    GPIO.add_event_detect(SOUND_SENSOR_GPIO_PIN, GPIO.RISING, callback=handle_loud_sound, bouncetime=200)

    # Start the LCD thread
    lcd_thread = threading.Thread(target=update_lcd)
    lcd_thread.start()

    try:
        # Main loop
        while True:
            # Your main program logic goes here
            if GPIO.input(SOUND_SENSOR_GPIO_PIN) == GPIO.HIGH:
                # Check if the sound level is above the threshold
                if response_text != "Loud Sound Detected!" and GPIO.input(SOUND_SENSOR_GPIO_PIN) > LOUD_SOUND_THRESHOLD:
                    response_text = "Loud Sound Detected!"
            else:
                response_text = textGenerator() or "No Loud Sound"
           
            time.sleep(1)

    except KeyboardInterrupt:
        # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
        print("Cleaning up!")
        GPIO.cleanup()
        lcd_thread.join()