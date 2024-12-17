import pyttsx3
import speech_recognition as sr
import time
import re
import threading

#テキストを読み上げ　Read text aloud
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

#音声取得、テキストに変換　Capture audio and convert it to text
def get_audio():
    r = sr.Recognizer()
    while True:
        print("Listening...")

        with sr.Microphone() as source:
            audio = r.listen(source)
                
            try:
                command = r.recognize_google(audio, language='en-US')
                print("You said: " + command)
                return command
            except sr.UnknownValueError:
                    print("Error")
            return ""
    
        
#音声入力から時間を取得　Recognize time from voice input
def parse_time(text):
    matches = re.findall(r"(\d+)\s*(sec|min|hr)", text)
    time_units = {"sec": 1, "min": 60, "hr": 3600}
    total_time = sum(int(amount) * time_units[unit] for amount, unit in matches)
    return total_time, matches[0][1] if matches else None

#Chancel
timers = {}
timer_id = 0

def run_timer(timer_id, second):
    global timers
    start_time = time.time()

    while time.time() - start_time < second:
        if timers.get(timer_id) == "canceled":
                print(f"Timer {timer_id} canceled!")
                speak(f"Timer {timer_id} canceled!")
                return
        time.sleep(1)

    print(f"Time is up for Timer {timer_id}!")
    speak(f"Time is up for Timer {timer_id}!")
    timers.pop(timer_id, None)    


#タイマーをセット　set Timer
def set_timer():
    global timer_id
    while True:
        text = get_audio()
        if text:
            if "cancel all" in text.lower():
                for id in list(timers.keys()):
                    timers[id] = "canceled"
                    print(f"All Timers canceld.")
                    speak(f"All Timers canceled.")
                    continue

            if re.search(r"cancel timer (\d+)", text.lower()):
                cancel_id = int(re.search(r"cancel timer (\d+)", text.lower()).group(1))
                if cancel_id in timers:
                    timers[cancel_id] = "canceled"
                    print(f"Timer {cancel_id} canceled.")
                    speak(f"Timer {cancel_id} canceled.")
                else:
                    print(f"Timer {cancel_id} not found.")
                    speak(f"Timer {cancel_id} not found.")
                    continue   

            if "goodbye" in text.lower():
                print("Goodbye!")
                speak("Goodbye!")
                break
            
            #Get timers
            seconds, unit = parse_time(text)
            if seconds > 0:
                timer_id += 1
                timers[timer_id] = "active"

                if unit == "sec":
                    print(f"Timer set for {seconds} seconds.")
                    speak(f"Timer set for {seconds} seconds.")
                elif unit == "min":
                    print(f"Timer set for {seconds // 60} minutes.")
                    speak(f"Timer set for {seconds // 60} minutes.")
                elif unit == "hr":
                    print(f"Timer set for {seconds // 3600} hours.")
                    speak(f"Timer set for {seconds // 3600} hours.")
                timer_thread = threading.Thread(target=run_timer, args=(timer_id, seconds))
                timer_thread.start()
            else:
                    speak("Error. Please try again.")

           
            
               
def main():
    set_timer()

if __name__ == "__main__":
    main()
    