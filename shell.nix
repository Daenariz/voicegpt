{
  pkgs ? import <nixpkgs> { },
}:

let
  python = pkgs.python312;
in
pkgs.mkShell {
  packages =
    (with pkgs; [
      alsa-utils
      espeak
      portaudio
    ])
    ++ [
      (python.withPackages (
        p: with p; [
          openai
          pyttsx3
          speechrecognition
          python-dotenv
          pyaudio
        ]
      ))
    ];

  shellHook = ''
    export PATH="${pkgs.espeak}/bin:$PATH"
    export LD_LIBRARY_PATH="${pkgs.espeak}/lib:$LD_LIBRARY_PATH"
    export ESPEAK_DATA_PATH="${pkgs.espeak}/share/espeak-ng-data"
  '';
}
