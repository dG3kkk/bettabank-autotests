"""
Smoke-тесты: проверяем, что приложение открывается и базовые элементы на месте.
"""
import pytest
from pages.login_page import LandingPage, LoginPage


@pytest.mark.smoke
def test_app_loads(page):
    """Приложение должно открываться и иметь заголовок"""
    landing = LandingPage(page)
    landing.open()
    assert page.title() == "Бэтта Банк"


@pytest.mark.smoke
def test_sign_in_link_leads_to_login_form(page):
    """Клик по 'Войти' на главной должен вести на форму /sign-up"""
    landing = LandingPage(page)
    landing.open()
    landing.go_to_sign_up()

    page.wait_for_url("**/sign-up**", timeout=5000)
    assert "/sign-up" in page.url


@pytest.mark.smoke
def test_login_form_elements_visible(page):
    """На странице /sign-up должны быть поля email, пароля и кнопка"""
    login_page = LoginPage(page)
    login_page.open()

    assert login_page.email_input.is_visible()
    assert login_page.password_input.is_visible()
    assert login_page.submit_button.is_visible()
