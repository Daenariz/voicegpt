{
  description = "VoiceGPT: A voice assistant using OpenAI";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable-small";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      poetry2nix,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            poetry2nix.overlays.default
            (final: _: {
              voicegpt = final.callPackage voicegpt { };
            })
          ];
        };

        voicegpt =
          { poetry2nix, lib }:
          poetry2nix.mkPoetryApplication {
            projectDir = self;

            overrides = poetry2nix.overrides.withDefaults (
              final: super:
              super
              // {
                # None of the below add the missing portaudio.h. Maybe we need to add it to pyaudio's build environment?
                nativeBuildInputs = [ pkgs.portaudio ];
                buildInputs = [ pkgs.portaudio ];
                environment = ''
                  export CFLAGS="-I${pkgs.portaudio}/include $CFLAGS"
                  export C_INCLUDE_PATH=${pkgs.portaudio}/include:$C_INCLUDE_PATH
                '';
                CFLAGS = "-I${pkgs.portaudio}/include";
                C_INCLUDE_PATH = "${pkgs.portaudio}/include";
              }
            );
          };
      in
      {
        packages.default = pkgs.voicegpt; # FIXME: "portaudio.h: No such file or directory"

        devShells = {
          default = pkgs.mkShell {
            # inputsFrom = [ pkgs.voicegpt ]; # This is what we actually want

            # Yet, we have to do this since the voicegpt package does not build:
            buildInputs = with pkgs; [
              alsa-utils
              espeak
              portaudio
              python312
              python312Packages.openai
              python312Packages.pyaudio
              python312Packages.python-dotenv
              python312Packages.pyttsx3
              python312Packages.speechrecognition
            ];
            shellHook = ''
              export PATH="${pkgs.espeak}/bin:$PATH"
              export LD_LIBRARY_PATH="${pkgs.espeak}/lib:$LD_LIBRARY_PATH"
              export ESPEAK_DATA_PATH="${pkgs.espeak}/share/espeak-ng-data"
            '';
          };

          poetry = pkgs.mkShell {
            packages = [ pkgs.poetry ];
          };
        };

        legacyPackages = pkgs;
      }
    );
}
