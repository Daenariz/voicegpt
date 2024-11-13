{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python310
    pkgs.python310Packages.pip
    pkgs.python310Packages.virtualenv
    pkgs.portaudio
  ];

  shellHook = ''
    # Erstelle eine virtuelle Umgebung, wenn sie noch nicht existiert
    if [ ! -d "venv" ]; then
      python3 -m venv venv
    fi
    # Aktiviere die virtuelle Umgebung
    source venv/bin/activate
    # Installiere die Pakete in der virtuellen Umgebung
    pip install --upgrade pip
    pip install wheel openai==0.28 pyttsx3 PyAudio SpeechRecognition python-dotenv
  '';
}

