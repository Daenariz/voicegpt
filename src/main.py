import speech_recognition as sr
import pyttsx3
import openai
import random

from dotenv import load_dotenv
import os
from utils import load_phrases, check_phrase



# adjust the file path to be relative to the main.py file 
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir) 

# file paths for language switching
data_dir = '../data'
language = 'en'   # use de for german, en for english and ja for japanese
wake_words_path = os.path.join(data_dir, language, 'wake_words.txt')
welcome_phrases_path = os.path.join(data_dir, language, 'welcome_phrases.txt')
idle_words_path = os.path.join(data_dir, language, 'idle_words.txt')

# for loading your api-key
load_dotenv()
api_key = os.getenv('API_KEY')
openai.api_key = api_key


# reference between language and local modells stored
voice_mapping = {
# certain microsoft model #TODO: better management for models of different os
    'de': 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_DE-DE_HEDDA_11.0',
    'en': 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0',
    'ja': 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_JA-JP_HARUKA_11.0'
}



engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voice_mapping[language])
engine.setProperty('rate', 230)


def speakText(command):
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
                mytext = r.recognize_google(audio2, language=language)   #de for german, ja-JP for japanese
               # print(mytext)

                return mytext

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occurred")


# see prices for desired model here: https://openai.com/api/pricing/
def send_to_chatGPT(messages, model="gpt-4o-mini"):

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=256,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

def gpt_loop(welcome=None):
    idle_words = load_phrases(idle_words_path)
    welcome_phrases = load_phrases(welcome_phrases_path)
    welcome = random.sample(welcome_phrases,1)
    speakText(welcome)
    while True:
        print("   --> entered if case")
        text2gpt = record_text().lower()
        print("   User:" + text2gpt)
        messages.append({"role": "user", "content": text2gpt})
        response = send_to_chatGPT(messages)
        speakText(response)
        print("   MOMO:" + response)
        if text2gpt in idle_words:
            print("<-- quiting if case")
            break

role_str = "Du bist mein persönlicher AI Assitent, der mir bei meinem Studium hilft und mich bei allen Fragen rund um die Elektrotechnik unterstützt."
messages = [{"role": "user", "content":  ""}]

def main():
    speakText("Starte Main einen Moment")
    wake_words = load_phrases(wake_words_path)
    while True:
        wake_word = record_text().lower()
        print(wake_word)
        if wake_word in wake_words:
            gpt_loop()
            print("state : outside if statement")

if __name__ == "__main__":
    main()
