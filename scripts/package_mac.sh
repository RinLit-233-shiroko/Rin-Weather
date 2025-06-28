#!/bin/bash

cd ..
.venv/bin/pyinstaller \
  --icon=assets/resources/images/logo.icns \
  --noconsole \
  --contents-directory="." \
  --add-data="assets:assets" \
  --paths=. \
  --name=RinWeather \
  app.py
