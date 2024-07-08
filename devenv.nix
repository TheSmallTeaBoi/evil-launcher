{pkgs, ...}: {
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = with pkgs; [gzdoom unar wget curl];

  enterShell = ''
  '';

  # https://devenv.sh/tests/
  enterTest = ''
    python evil freereelism.hell
  '';

  # https://devenv.sh/languages/
  languages.python.enable = true;
}
