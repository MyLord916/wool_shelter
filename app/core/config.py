from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
import os


class PathConfig:
    """Конфигурация путей приложения"""

    # Базовые пути
    BASE_DIR = Path(__file__).resolve().parents[2]
    PROJECT_DIR = BASE_DIR / "app"

    # Директории данных
    DATA_DIR = BASE_DIR / "data"
    FIXTURES_DIR = PROJECT_DIR / "fixtures"
    MIGRATIONS_DIR = PROJECT_DIR / "migrations"
    TEST_DIR = PROJECT_DIR / "tests"

    # Прочие директории
    MODELS_DIR = PROJECT_DIR / "models"  # Модели
    SCHEMAS_DIR = PROJECT_DIR / "schemas"  # Схемы валидации
    SERVISES_DIR = PROJECT_DIR / "services"  # Бизнес-логика
    REPOSITORIES_DIR = PROJECT_DIR / "repositories"  # Работа с данными
    FRONTEND_DIR = PROJECT_DIR / "frontend"
    # ├── api/                  # Веб-интерфейс
    # ├── utils/                # Вспомогательные функции
    # ├── config/               # Конфигурация
    # ├── scripts/              # Скрипты управления
    # ├── migrations/           # Миграции базы данных
    # └── docs/

    # Функциональные файлы
    DATABASE_FILE = DATA_DIR / "shelter.db"
    TEST_DATABSE_FILE = TEST_DIR / "test.db"
    FIXTURES_FILE = FIXTURES_DIR / "all_data.json"
    ENV_FILE = BASE_DIR / ".env"


class DatabaseConfig:
    """Конфигурация базы данных"""

    @classmethod
    def database_url(cls, test=False) -> str:
        """Возвращает URL для подключения к БД"""
        if test:
            db_path = PathConfig.TEST_DATABSE_FILE
        else:
            db_path = PathConfig.DATABASE_FILE
        return f"sqlite:///{db_path}"


class JWTConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    @classmethod
    def get_access_token_expires(cls):
        return timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)

    @classmethod
    def get_refresh_token_expires(cls):
        return timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS)


class AppConfig:
    """Основная конфигурация приложения"""

    load_dotenv(PathConfig.ENV_FILE)
    APP_NAME = "Wool Shelter"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    def __init__(self):
        # Инициализируем пути
        self.paths = PathConfig()
        self.database = DatabaseConfig()


# Создаем глобальный экземпляр конфигурации
config = AppConfig()
