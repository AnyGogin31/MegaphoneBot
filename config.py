import os
from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DB_URL")


if not BOT_TOKEN:
    exit("Error: BOT_TOKEN not found in .env file")

if not DB_URL:
    exit("Error: DB_URL not found in .env file")
