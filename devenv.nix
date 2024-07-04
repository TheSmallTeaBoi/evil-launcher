{pkgs, ...}: {
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = [pkgs.gzdoom];

  enterShell = ''
  '';

  # https://devenv.sh/tests/
  enterTest = ''
    python main.py
  '';

  # https://devenv.sh/languages/
  languages.python.enable = true;
}
