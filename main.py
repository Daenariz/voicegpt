import speech_recognition as sr
import pyttsx3
import openai
import os
from dotenv import load_dotenv
#load_dotenv()
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# from openai import OpenAI

openai.api_key = "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"

def speakText(command):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 230)
    engine.say(command)
    engine.runAndWait()


r = sr.Recognizer()


def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.5)
                r.dynamic_energy_threshold = True

                print("I'm listening")

                audio2 = r.listen(source2)

                MyText = r.recognize_google(audio2, language="de")
               # print(MyText)

                return MyText

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occurred")


def send_to_chatGPT(messages, model="gpt-3.5-turbo"):

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message


messages = [{"role": "user", "content": "Du bist mein persönlicher AI Assitent, der mir bei meinem Studium hilft und mich bei allen Fragen rund um die Elektrotechnik unterstützt."}]
while True:
    wake_word = record_text()
    print(wake_word)
    if(wake_word == "hey Momo"):
        while True:
            print("--> entered if case")
            speakText("Was kann ich für dich tun?")
            text2gpt = record_text()
            print(text2gpt)
            messages.append({"role": "user", "content": text2gpt})
            response = send_to_chatGPT(messages)
            speakText(response)
            print(response)
            if (text2gpt == "danke"):
                print("<-- quiting if case")
                break
    print("state : outside if statement")
