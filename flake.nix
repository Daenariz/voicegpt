{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable-small";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # Importiere nixpkgs einmal und verwende es für alle Abhängigkeiten
        pkgs = import nixpkgs { inherit system; };

        # Poetry2Nix Anwendung erstellen
        myapp = poetry2nix.mkPoetryApplication {
          projectDir = self;
          overrides = poetry2nix.overrides.withDefaults (final: super:
            super // {
              # Optional: nativeBuildInputs oder andere Customizations
            }
          );
        };

      in
      {
        # Paket für das Standard-Projekt
        packages.default = pkgs.mkPoetryApplication {
          projectDir = self;
        };

        devShells = {
          # Shell für die Anwendung und Abhängigkeiten (inkl. Poetry, PortAudio, espeak)
          default = pkgs.mkShell {
            buildInputs = [
              pkgs.poetry          # Poetry für das Projekt
              pkgs.portaudio       # PortAudio, falls benötigt
              pkgs.espeak          # espeak als Abhängigkeit
              pkgs.python310       # Python 3.10, falls du es explizit brauchst
              pkgs.python310Packages.pyaudio
              pkgs.python310Packages.speechrecognition
              pkgs.python310Packages.python-dotenv
              pkgs.python310Packages.pyttsx3
              pkgs.python310Packages.openai
            ];
            shellHook = ''
            export PATH="${pkgs.espeak}/bin:$PATH" 
'';
          };

          # Separate Shell für Poetry
          poetry = pkgs.mkShell {
            packages = [pkgs.python310Packages.pip pkgs.poetry pkgs.portaudio pkgs.espeak pkgs.python310 ];  # Nur Poetry für die pyproject.toml-Verwaltung
            shellHook = ''
            export PATH="${pkgs.espeak}/bin:$PATH" 
'';
          };
        };

        # Legacy-Pakete (falls nötig für andere Umgebungen)
        legacyPackages = pkgs;
      }
    );
}

