"""
Page Object для страницы авторизации BettaBank.

ВАЖНО: селекторы ниже — placeholder'ы (data-testid / примерные css).
Перед запуском сверьте их с реальной вёрсткой через DevTools (Elements tab):
правый клик по полю -> Inspect -> скопировать id/class/data-testid.
"""

from playwright.sync_api import Page


class LandingPage:
    """Главная страница — подтверждено реальной разметкой сайта."""

    def __init__(self, page: Page):
        self.page = page
        self.url = "https://test-mrn.astondevs.ru/"
        self.sign_in_link = page.locator("a._link_dkhf7_48")  # "Войти" -> /sign-up

    def open(self):
        self.page.goto(self.url)

    def go_to_sign_up(self):
        self.sign_in_link.click()


class LoginPage:
    """Форма входа. Селекторы подтверждены реальной разметкой /sign-up."""

    def __init__(self, page: Page):
        self.page = page
        self.url = "https://test-mrn.astondevs.ru/sign-up"

        self.email_input = page.locator("#E-mail")
        self.password_input = page.locator("#Пароль")
        self.submit_button = page.get_by_role("button", name="Продолжить")
        self.password_error = page.locator(".massage-error-password .error")
        self.forgot_password_link = page.locator("a[href='/recovery']")
        self.become_client_link = page.locator("a[href='/sign-in']")

    def open(self):
        self.page.goto(self.url)

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def get_password_error_text(self) -> str:
        return self.password_error.text_content()

    def is_submit_enabled(self) -> bool:
        return self.submit_button.is_enabled()

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def get_error_text(self) -> str:
        return self.error_message.text_content()
