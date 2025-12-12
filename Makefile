# Переменные
PYTHON = .venv/bin/python
UV = uv
ALEMBIC = $(PYTHON) -m alembic
APP_DIR = app
MAIN_FILE = main.py

# Цели по умолчанию
.PHONY: help install dev-install run migrate makemigrations test lint format clean db-init db-commands

# Помощь - покажет все доступные команды
help:
	@echo
	@echo "Доступные команды:"
	@echo "  install         - установка production зависимостей"
	@echo "  dev-install     - установка dev зависимостей"
	@echo "  run             - запуск приложения"
	@echo "  migrate         - применение миграций"
	@echo "  makemigrations  - создание новых миграций"
	@echo "  db-init         - инициализация базы данных (первый запуск)"
	@echo "  test            - запуск тестов"
	@echo "  lint            - проверка кода ruff"
	@echo "  format          - форматирование кода black"
	@echo "  clean           - очистка временных файлов"
	@echo "  db-commands      - команды для управления базой данных"

# Установка production зависимостей
install:
	$(UV) sync --no-dev

# Установка dev зависимостей (рекомендуется для разработки)
dev-install:
	$(UV) sync --dev

# Запуск приложения
run:
	$(UV) run $(PYTHON) $(MAIN_FILE)

# Применение миграций
migrate:
	$(ALEMBIC) upgrade head

# Создание новой миграции (использование: make makemigrations msg="описание миграции")
makemigrations:
	$(ALEMBIC) revision --autogenerate -m "$(msg)"

# Инициализация базы данных (первый запуск)
db-init:
	$(ALEMBIC) upgrade head
	@echo
	@echo " ✅ База данных инициализирована"
	@echo

# Запуск тестов
test:
	$(UV) run pytest

# Проверка кода ruff
lint:
	$(UV) run ruff check $(APP_DIR)

# Форматирование кода black
format:
	$(UV) run black $(APP_DIR)

# Очистка временных файлов
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf .coverage
	@echo
	@echo " ✅ Очистка завершена"
	@echo

# Полная установка и настройка для разработки
setup: dev-install db-init
	@echo
	@echo " ✅ Проект настроен для разработки!"
	@echo

# Быстрый перезапуск (очистка, установка, миграции, запуск)
restart: clean dev-install migrate run

# Управление базой данных
SCRIPTS_DIR = scripts
SCRIPT_FILE = $(SCRIPTS_DIR)/db_control.py

.PHONY: db-comands db-add-test-animals db-dump db-load db-clear

count ?= 10

db-commands:
	@echo
	@echo "Команды управления базой данных:"
	@echo "  db-add-test-animals  - добавить тестовые данные"
	@echo "           └──count=5  - задать количество тестовых записей (по умолчанию 10)"
	@echo "  db-clear             - очистить базу (с подтверждением)"
	@echo "  db-dump              - создать бэкап"
	@echo "  db-load              - загрузить данные из бекапа"
	@echo

db-add-test-animals:
	$(UV) run $(PYTHON) $(SCRIPT_FILE) -a $(if $(filter-out 10,$(count)),-t $(count))

db-dump:
	$(UV) run $(PYTHON) $(SCRIPT_FILE) -d

db-load:
	$(UV) run $(PYTHON) $(SCRIPT_FILE) -l

db-clear:
	@echo "⚠️  Вы уверены, что хотите очистить базу данных? [y/N]"; \
    read answer; \
    if [ "$$answer" = "y" ] || [ "$$answer" = "Y" ]; then \
        $(UV) run $(PYTHON) $(SCRIPT_FILE) -c;\
    else \
		echo " "; \
        echo "❌ Операция отменена"; \
		echo " "; \
    fi


	