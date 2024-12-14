def load_phrases(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        phrases = file.readlines()
    # Entfernen von Leerzeichen und Zeilenumbrüchen
    phrases = [phrase.strip() for phrase in phrases]
    return phrases

def check_phrase(input_string, phrases):
    return any(phrase in input_string for phrase in phrases)