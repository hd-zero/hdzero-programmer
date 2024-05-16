#!/usr/bin/env bash

rm -rf build dist
pyinstaller -i HDZeroIcon.ico -w --onefile --add-data="resource:resource" hdzero_programmer.py
