import pyttsx3

def set_voice(engine, language):
    # デフォルトの声を設定
    engine.setProperty('voice', engine.getProperty('voices')[0].id)  # 最初の音声をデフォルトに設定
    engine.setProperty('rate', 200)  # 話す速度を設定

    # 音声のリストを取得
    voices = engine.getProperty('voices')

voice_mapping = {
    'de': 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_DE-DE_HEDDA_11.0',
    'en': 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0',
    'ja': 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_JA-JP_HARUKA_11.0'
}

def set_voice(engine, language):
    if language in voice_mapping:
        engine.setProperty('voice', voice_mapping[language])
    else:
        print("指定された言語の音声が見つかりません。")    