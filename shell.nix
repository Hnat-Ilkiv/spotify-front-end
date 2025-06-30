{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python311
    python311Packages.sqlalchemy
    python311Packages.flask
    python311Packages.faker
    python311Packages.pytest
  ];

  shellHook = ''
    alias main="python -m src.main"
    export FLASK_APP=src.app
    export FLASK_ENV=development
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    echo "Spotify App Dev Environment Ready"
    pytest
  '';
}

