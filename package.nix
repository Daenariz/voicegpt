{
  python312,
  alsa-utils,
  espeak,
  portaudio,
}:

let
  python = python312;
in
python.pkgs.buildPythonApplication {
  pname = "voicegpt";
  version = "0.1.0";
  pyproject = true;

  src = ./.;

  build-system = [
    python.pkgs.setuptools
    python.pkgs.wheel
  ];

  dependencies =
    [
      alsa-utils
      espeak
      portaudio
    ]
    ++ (with python.pkgs; [
      openai
      pyttsx3
      speechrecognition
      python-dotenv
      pyaudio
    ]);

  # TODO
  # pythonImportsCheck = [
  # ];
}
