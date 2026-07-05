# BettaBank Autotests

UI-автотесты для демо-приложения [BettaBank](https://test-mrn.astondevs.ru/) на Playwright + pytest.

Проект написан на основе ручного exploratory-тестирования приложения (около 50 задокументированных багов: UI, функциональные, API, валидационные) — автотесты покрывают ключевые сценарии, включая найденные ранее проблемные места (валидация суммы перевода, обработка невалидных данных при авторизации).

## Стек
- Python 3.11
- Playwright (sync API)
- pytest
- Page Object Model
- GitHub Actions (CI)

## Структура проекта

```
bettabank-autotests/
├── pages/                  # Page Object классы
│   ├── login_page.py
│   └── dashboard_page.py
├── tests/
│   ├── conftest.py         # фикстуры (browser, page, тестовые данные)
│   ├── test_smoke.py       # базовые smoke-проверки
│   ├── test_auth.py        # авторизация: позитивные/негативные кейсы
│   └── test_transfer.py    # переводы: функциональные и валидационные тесты
├── .github/workflows/
│   └── tests.yml           # CI pipeline
├── requirements.txt
├── pytest.ini
└── README.md
```

## Установка

```bash
git clone <repo-url>
cd bettabank-autotests
pip install -r requirements.txt
playwright install chromium
```

## Запуск тестов

```bash
# все тесты
pytest -v

# только smoke
pytest -v -m smoke

# только авторизация
pytest -v -m auth

# с отчётом
pytest -v --junitxml=results.xml
```

## Известные ограничения
- Функционал переводов на демо-сайте не реализован/нестабилен — тесты на него не пишутся.
- Нет доступа к реальному тестовому аккаунту, поэтому позитивный сценарий логина
  (`test_login_with_valid_credentials`) и тест текста ошибки при неверном пароле
  используют placeholder-данные и требуют реальных кредов для прохождения.
