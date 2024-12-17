## Directory Structure

```
.
├── data
│   ├── de
│   │   ├── idle_words.txt
│   │   ├── wake_words.txt
│   │   └── welcome_phrases.txt
│   ├── en
│   │   ├── idle_words.txt
│   │   ├── wake_words.txt
│   │   └── welcome_phrases.txt
│   └── ja
│       ├── idle_words.txt
│       ├── wake_words.txt
│       └── welcome_phrases.txt
├── poetry.lock
├── pyproject.toml
├── README.md
├── requirements.txt
└── src
    ├── main.py
    ├── __pycache__
    │   └── utils.cpython-310.pyc
    └── utils.py
```

Those are the pip commands I used:

```
pip install pyttsx3
pip install PyAudio
pip install SpeechRecognition 
pip install python-dotenv
pip install openai==0.28
```

All tested with Python 3.10 since PyAudio hasn't worked for 3.12 yet.


In case you want to start right away, type

```
pip install -r requirements.txt
```

You also need to create a .env file with your OpenAI API-Key stored which looks like this:

```
API_KEY=<YOUR-API-KEY>
```

In case you name it differently, do not forget to add it to the .gitignore file, since your key would be publicly visible otherwise.

The codebase was originally developed on Windows 10. There's already a [debian branch](https://github.com/Daenariz/voicegpt/tree/feature/debian) which will be worked on in the future. Depending on what system you are and the voice models you have installed you might want to use:

```
python
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
print(f"Name: {voice.name}, ID: {voice.id}, Language: {voice.languages}, Gender: {voice.gender}")
```

set your voice_mapping in the main.py according to the ID:<path/to/voicemodel>

Python Poetry coming soon..
