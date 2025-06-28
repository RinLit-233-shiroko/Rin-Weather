cd ..
.venv\Scripts\pyinstaller.exe ^
  --icon=assets/resources/images/logo.ico ^
  --noconsole ^
  --contents-directory="." ^
  --add-data="assets;assets" ^
  --paths=. ^
  --name=RinWeather ^
  app.py
