"""
Тесты авторизации: успешный вход и навигация по ссылкам формы.
"""
import pytest
from pages.login_page import LoginPage


@pytest.mark.auth
@pytest.mark.skip(reason="Требуется реальный тестовый аккаунт — данные не предоставлены")
def test_login_with_valid_credentials(page, valid_user):
    """Успешная авторизация с валидными данными"""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(valid_user["email"], valid_user["password"])

    page.wait_for_url("**/dashboard**", timeout=5000)
    assert "dashboard" in page.url


@pytest.mark.auth
@pytest.mark.skip(reason="Требуется реальный тестовый аккаунт — данные не предоставлены")
def test_login_with_wrong_password_shows_error(page, valid_user):
    """Неверный пароль для существующего email должен показывать текст ошибки"""
    login_page = LoginPage(page)
    login_page.open()

    login_page.login(valid_user["email"], "WrongPassword999")

    assert login_page.password_error.text_content().strip() != ""


@pytest.mark.auth
def test_forgot_password_link_navigates(page):
    """Ссылка 'Забыли пароль?' должна вести на /recovery"""
    login_page = LoginPage(page)
    login_page.open()

    login_page.forgot_password_link.click()
    page.wait_for_url("**/recovery**", timeout=5000)
    assert "/recovery" in page.url


@pytest.mark.auth
def test_become_client_link_navigates(page):
    """Ссылка 'Стать клиентом Банка' должна вести на /sign-in"""
    login_page = LoginPage(page)
    login_page.open()

    login_page.become_client_link.click()
    page.wait_for_url("**/sign-in**", timeout=5000)
    assert "/sign-in" in page.url
