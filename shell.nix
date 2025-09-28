{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.ffmpeg
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.stdenv.cc.cc.lib
  ];
}
