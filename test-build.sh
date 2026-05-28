#!/bin/sh

rm -rf ./dist/beatsketch/
python -m PyInstaller beatsketch_launcher.spec
cp -r ./testing/* ./dist/beatsketch/
