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
    MIGRATIONS_DIR = PROJECT_DIR / "tag"

    MODELS_DIR = PROJECT_DIR / "models"
    SCHEMAS_DIR = PROJECT_DIR / "schemas"
    SERVISES_DIR = PROJECT_DIR / "services"  # Бизнес-логика
    # ├── api/                  # Веб-интерфейс
    REPOSITORIES_DIR = PROJECT_DIR / "repositories"  # Работа с данными
    FRONTEND_DIR = PROJECT_DIR / "frontend"
    # ├── utils/                # Вспомогательные функции
    # ├── config/               # Конфигурация
    TEST_DIR = PROJECT_DIR / "tests"  # Тесты
    # ├── scripts/              # Скрипты управления
    # ├── migrations/           # Миграции базы данных
    # └── docs/

    DATABASE_FILE = DATA_DIR / "shelter.db"
    TEST_DATABSE_FILE = TEST_DIR / "test.db"
    FIXTURES_FILE = FIXTURES_DIR / "all_data.json"

    ENV_FILE = BASE_DIR / ".env"

    @classmethod
    def setup_directories(cls):
        """Создает все необходимые директории"""
        directories = [
            cls.DATA_DIR,
            cls.FIXTURES_DIR,
            cls.MODELS_DIR,
            cls.SCHEMAS_DIR,
            cls.SERVISES_DIR,
            cls.REPOSITORIES_DIR,
        ]

        for directory in directories:

            directory.mkdir(parents=True, exist_ok=True)
            init_file = directory / "__init__.py"
            init_file.touch(exist_ok=True)

        print(f"Директории созданы в: {cls.BASE_DIR}")


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
    load_dotenv(PathConfig.ENV_FILE)
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

    APP_NAME = "Wool Shelter"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    def __init__(self):
        # Инициализируем пути
        self.paths = PathConfig()
        self.database = DatabaseConfig()

    # # Создаем директории при инициализации
    # if not os.getenv("TESTING"):
    #     self.paths.setup_directories()


# Создаем глобальный экземпляр конфигурации
config = AppConfig()
