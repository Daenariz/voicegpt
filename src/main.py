import os
from dotenv import load_dotenv
import openai
import speech_recognition as sr
import pyttsx3
from commands import get_language_change_commands
from set_voice import set_voice

load_dotenv()
api_key = os.getenv('API_KEY')
if api_key is None:
    print("API_KEYが環境変数から取得できませんでした。設定を確認してください。")
    exit(1)  # Terminate the program if you don't have the API key

openai.api_key = api_key

LANGUAGES = {
    'Japanese': 'ja',  
    'English': 'en',   
    'German': 'de',    
}

engine = pyttsx3.init()

def get_voice_input(language):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please talk...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=language)
        print(f"You: {text}")
        return text
    except sr.UnknownValueError:
        print("The voice could not be recognized. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"request error: {e}")
        return None

def get_gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Model name to use
            messages=[{"role": "user", "content": prompt}]
        )
        message = response.choices[0].message['content']
        print(f"GPT: {message}")
        return message
    except Exception as e:
        print(f"An error occurred while requesting to GPT: {e}")
        return "An error has occurred."

def speak(text, language):
    set_voice(engine, language)  # Apply audio settings
    engine.say(text)
    engine.runAndWait()  # Wait until speech synthesis is complete

def change_language(command):
    commands = get_language_change_commands()  # get command
    return commands.get(command.lower())

def main():
    current_language = 'en' # Set initial language to english
    wake_up_word = "wake up"  # set wake word
    sleep_command = "sleep"  
    
    while True:
        print("ウェイクワードを待っています...") # wait for wake word
        user_input = get_voice_input('en')  # Recognize wake word in English
        
        if user_input:
            if wake_up_word in user_input.lower():
                print(f"ウェイクワード '{wake_up_word}' が認識されました。")
                speak("こんにちは、何をお手伝いできますか？", current_language)

                # Switch to normal interaction mode
                while True:
                    user_input = get_voice_input(current_language)
                    if user_input:
                        # Check if sleep command is included
                        if sleep_command in user_input.lower():
                            print("スリープコマンドが認識されました。アプリケーションを終了します。")
                            speak("お休みなさい。", current_language)
                            break  # exit interactive mode and return to main loop

                        # Check if language change command is included
                        new_language = change_language(user_input)
                        if new_language:
                            current_language = new_language
                            print(f"言語が変更されました: {new_language}")
                            set_voice(engine, current_language)  # Set to new language voice
                            continue  # Continue typing in new language

                        response = get_gpt_response(user_input)
                        speak(response, current_language)

if __name__ == "__main__":
    main()