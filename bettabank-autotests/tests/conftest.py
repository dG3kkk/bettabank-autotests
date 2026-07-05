import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://test-mrn.astondevs.ru/"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(BASE_URL)
    yield page
    context.close()


@pytest.fixture
def valid_user():
    """Тестовый пользователь для позитивных сценариев.
    Замените на реальные тестовые данные BettaBank."""
    return {"email": "test.user@example.com", "password": "TestPass123!"}
