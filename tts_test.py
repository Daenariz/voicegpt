# tts_test.py

from TTS.api import TTS
import sounddevice as sd
import numpy as np

# Lade das vortrainierte Modell
def init_tts_model():
    tts = TTS(model_name="tts_models/de/css10/vits-neon", progress_bar=True, gpu=False)
    return tts

def text_to_speech(text):
    tts = init_tts_model()
    # Erzeuge die Sprachdaten
    waveform = tts.tts(text)

    # Konvertiere die Sprachdaten in ein numpy-Array
    audio_data = np.array(waveform, dtype=np.float32)

    # Wiedergabe der Sprachdaten
    sd.play(audio_data, samplerate=tts.synthesizer.output_sample_rate)
    sd.wait()  # Warte, bis das Audio abgespielt wurde

    print("Sprachwiedergabe abgeschlossen.")
