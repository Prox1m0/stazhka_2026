from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from services.settings_service import get_buttons

def get_main_menu():
    buttons = [[KeyboardButton(text=b["text"])] for b in get_buttons()]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
