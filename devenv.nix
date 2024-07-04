{pkgs, ...}: {
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = with pkgs; [gzdoom unar];

  enterShell = ''
  '';

  # https://devenv.sh/tests/
  enterTest = ''
    python main.py
  '';

  # https://devenv.sh/languages/
  languages.python.enable = true;
}
