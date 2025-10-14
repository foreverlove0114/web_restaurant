from dotenv import load_dotenv
import os

load_dotenv()

class DBConfig:
    _USER = os.getenv("PGUSER")
    _PASSWORD = os.getenv("PGPASS")
    _HOST = os.getenv("IP")
    _PORT = os.getenv("PORT")
    _DATABASE = os.getenv("DATABASE")

    @classmethod
    def get_connection_string(cls):
        return f"postgresql+psycopg2://{cls._USER}:{cls._PASSWORD}@{cls._HOST}:{cls._PORT}/{cls._DATABASE}"


class TelegramConfig:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")


class AppConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    MAX_FORM_MEMORY_SIZE = 1024 * 1024  # 1MB
    MAX_FORM_PARTS = 500
    SESSION_COOKIE_SAMESITE = 'Strict'