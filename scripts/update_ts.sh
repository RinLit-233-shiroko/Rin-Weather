#!/bin/bash

cd ..

pyside6-lupdate $(find assets/RinWeather -name "*.py" -o -name "*.qml") -ts assets/locales/en_US.ts
pyside6-lupdate $(find assets/RinWeather -name "*.py" -o -name "*.qml") -ts assets/locales/zh_CN.ts

pyside6-lrelease assets/locales/en_US.ts
pyside6-lrelease assets/locales/zh_CN.ts
