# shell.nix
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  # Die Python-Umgebung und benötigten Pakete hinzufügen
  buildInputs = [
    pkgs.python310          # Installiert Python 3.10
    pkgs.python310Packages.pip # Installiert pip für Python 3.10
    pkgs.python310Packages.pyttsx3  # Installiert pyttsx3
    pkgs.python310Packages.pyaudio  # Installiert PyAudio
    pkgs.python310Packages.speechrecognition # Installiert SpeechRecognition
    pkgs.python310Packages.python-dotenv  # Installiert python-dotenv
  ];

  # Optional: Shell-Umgebungsvariablen oder benutzerdefinierte Konfiguration
  shellHook = ''
    # Zum Beispiel: Setze PYTHONPATH auf den richtigen Pfad
    pip install openai == 0.28
    export PYTHONPATH=${pkgs.python310Packages.pyttsx3}:${pkgs.python310Packages.pyaudio}:${pkgs.python310Packages.speechrecognition}:${pkgs.python310Packages.python-dotenv}
  '';
}

