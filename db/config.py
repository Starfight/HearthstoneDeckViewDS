import os

from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv('APP_ID')
TOKEN = os.getenv("TOKEN")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

PROXY = {
    "http": os.getenv("PROXY_HTTP"),
    "https": os.getenv("PROXY_HTTPS")
}

FOLDER = "cards/"

DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}
TABLE_NAME = "leaderboard_month_history"
