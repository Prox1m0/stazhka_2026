from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
REQUESTS_CHAT_ID = os.getenv("REQUESTS_CHAT_ID")

