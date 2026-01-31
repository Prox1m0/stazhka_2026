import json
import os

SETTINGS_FILE = "data/buttons.json"

_settings = {
    "greeting": "👋 Добро пожаловать! Выберите, что вас интересует:",
    "buttons": []
}

def load_settings():
    global _settings

    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            _settings["buttons"] = json.load(f)
    else:
        save_settings()
    return _settings

def save_settings():
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(_settings["buttons"], f, ensure_ascii=False, indent=2)

def get_greeting():
    return _settings["greeting"]

def set_greeting(text: str):
    _settings["greeting"] = text

def get_buttons():
    return _settings["buttons"]

def add_button(button: dict):
    _settings["buttons"].append(button)
    save_settings()

def remove_button(index: int):
    if 0 <= index < len(_settings["buttons"]):
        _settings["buttons"].pop(index)
        save_settings()

def update_button(index: int, button: dict):
    if 0 <= index < len(_settings["buttons"]):
        _settings["buttons"][index] = button
        save_settings()
