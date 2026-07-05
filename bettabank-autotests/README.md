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

## Важное примечание

Селекторы в `pages/login_page.py` и `pages/dashboard_page.py` — placeholder'ы
(`input[name='email']`, `data-testid='...'` и т.д.). Перед первым запуском их
нужно сверить с реальной вёрсткой приложения через DevTools (Elements tab) и
поправить под фактические атрибуты элементов.

## Известные ограничения
- Функционал переводов на демо-сайте не реализован/нестабилен — тесты на него не пишутся.
- Нет доступа к реальному тестовому аккаунту, поэтому позитивный сценарий логина
  (`test_login_with_valid_credentials`) и тест текста ошибки при неверном пароле
  используют placeholder-данные и требуют реальных кредов для прохождения.

## Что дальше можно добавить
- API-тесты (requests / httpx) для эндпоинтов, изученных через Network tab
- Allure-отчётность
- Тесты на разных viewport (мобильная адаптивность)
- Негативные API-сценарии (невалидные токены, некорректные payload)
