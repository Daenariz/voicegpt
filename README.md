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
Python Poetry coming soon..