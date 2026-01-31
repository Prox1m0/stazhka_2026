from aiogram import Bot
from datetime import datetime
import pytz

from config import REQUESTS_CHAT_ID

utc = pytz.utc
msc_tz = pytz.timezone('Europe/Moscow')

async def send_request(bot: Bot, name: str, task: str, contact: str, timestamp: datetime):
    try:
        if timestamp.tzinfo is None:
            utc_time = utc.localize(timestamp)
        else:
            utc_time = timestamp.astimezone(utc)

        msc_time = utc_time.astimezone(msc_tz)

        formatted_time = msc_time.strftime("%H:%M %d.%m.%Y")

        message = (
            f"📋 НОВАЯ ЗАЯВКА\n"
            f"Имя: {name}\n"
            f"Задача: {task}\n"
            f"Контакт: {contact}\n"
            f"Время: {formatted_time}"
        )

        await bot.send_message(chat_id=REQUESTS_CHAT_ID, text=message)
    except Exception as e:
        print(f"Ошибка отправки в группу: {e}")
