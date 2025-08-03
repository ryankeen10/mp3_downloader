#!/bin/bash
# MP3 Downloader Launcher
# Activates virtual environment and runs the application

cd "$(dirname "$0")"
source .venv/bin/activate
python main.py
