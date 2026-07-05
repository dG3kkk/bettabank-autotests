"""
Тесты валидации полей email и пароля на форме /sign-up.

Спецификация email:
- Общая длина email <= 50 символов
- Локальная часть (до @): от 1 до 30 символов
- Часть между @ и последней точкой: от 2 до 15 символов
- Доменная зона (после последней точки): от 2 до 3 символов
- Разрешены: латинские буквы (a-z, A-Z), цифры (0-9), символы . _ - @
- Без пробелов, без двух спецсимволов подряд
- Точка не может быть первым/последним символом, не может стоять перед @,
  не может повторяться подряд (john..doe@example.com — невалидно)
- Email не может начинаться с пробела, дефиса или нижнего подчеркивания

Спецификация пароля:
- Длина от 8 до 50 символов
"""
import pytest
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page):
    lp = LoginPage(page)
    lp.open()
    return lp


# ---------- EMAIL: позитивные кейсы ----------

@pytest.mark.validation
@pytest.mark.parametrize("email", [
    "a@ab.ru",                          # минимальные границы: 1 до @, 2 после, 2 в зоне
    "john.doe@example.com",             # стандартный кейс с точкой в локальной части
    "user_name-1@mail-service.org",     # подчёркивание и дефис
    "a" * 30 + "@" + "b" * 15 + ".com", # максимальные границы (30/15/3)
])
def test_email_valid_formats_enable_submit(login_page, email):
    """Корректные email должны позволять активировать кнопку (при валидном пароле)"""
    login_page.email_input.fill(email)
    login_page.password_input.fill("ValidPass123")

    assert login_page.is_submit_enabled()


# ---------- EMAIL: длина локальной части (до @) ----------

@pytest.mark.validation
def test_email_local_part_exceeds_30_chars_rejected(login_page):
    """Локальная часть длиннее 30 символов должна блокировать отправку"""
    email = "a" * 31 + "@example.com"
    login_page.email_input.fill(email)
    login_page.password_input.fill("ValidPass123")

    assert not login_page.is_submit_enabled()


# ---------- EMAIL: длина части после @ и до точки ----------

@pytest.mark.validation
def test_email_domain_name_too_short_rejected(login_page):
    """Часть между @ и точкой короче 2 символов должна блокировать отправку"""
    login_page.email_input.fill("user@a.com")
    login_page.password_input.fill("ValidPass123")

    assert not login_page.is_submit_enabled()


@pytest.mark.validation
def test_email_domain_name_exceeds_15_chars_rejected(login_page):
    """Часть между @ и точкой длиннее 15 символов должна блокировать отправку"""
    email = "user@" + "b" * 16 + ".com"
    login_page.email_input.fill(email)
    login_page.password_input.fill("ValidPass123")

    assert not login_page.is_submit_enabled()


# ---------- EMAIL: доменная зона (после точки) ----------

@pytest.mark.validation
@pytest.mark.parametrize("email", [
    "user@example.c",       # 1 символ — короче минимума
    "user@example.abcd",    # 4 символа — длиннее максимума
])
def test_email_tld_length_out_of_range_rejected(login_page, email):
    """Доменная зона короче 2 или длиннее 3 символов должна блокировать отправку"""
    login_page.email_input.fill(email)
    login_page.password_input.fill("ValidPass123")

    assert not login_page.is_submit_enabled()


# ---------- EMAIL: общая длина ----------

@pytest.mark.validation
def test_email_total_length_exceeds_50_chars_rejected(login_page):
    """Email длиннее 50 символов суммарно должен блокировать отправку"""
    # локальная часть 30 + @ + 15 + . + 3 = 50 ровно, добавим ещё символ сверху лимита
    email = "a" * 30 + "@" + "b" * 15 + ".com1"
    login_page.email_input.fill(email)
    login_page.password_input.fill("ValidPass123")

    assert not login_page.is_submit_enabled()


# ---------- EMAIL: недопустимые символы и пробелы ----------

@pytest.mark.validation
@pytest.mark.parametrize("email", [
    "john doe@example.com",   # пробел в локальной части
    "john@ example.com",      # пробел после @
    "john#doe@example.com",   # запрещённый символ #
    "john!doe@example.com",   # запрещённый символ !
])
def test_email_invalid_characters_rejected(login_page, email):
    """Пробелы и неразрешённые символы должны блокировать отправку"""
    login_page.email_input.fill(email)
    login_page.password_input.fill("ValidPass123")

    assert not login_page.is_submit_enabled()


# ---------- EMAIL: правила для точки и первого символа ----------

@pytest.mark.validation
@pytest.mark.parametrize("email", [
    ".john@example.com",        # точка первым символом
    "john.@example.com",        # точка перед @ (последний символ локальной части)
    "john..doe@example.com",    # две точки подряд
    "-john@example.com",        # начинается с дефиса
    "_john@example.com",        # начинается с подчёркивания
    " john@example.com",        # начинается с пробела
]) 
def test_email_dot_and_leading_char_rules_rejected(login_page, email):
    """Точка не может быть первой/последней/перед @/повторяться;
    email не может начинаться с пробела, дефиса или подчёркивания"""
    login_page.email_input.fill(email)
    login_page.password_input.fill("ValidPass123")

    assert not login_page.is_submit_enabled()


@pytest.mark.validation
def test_email_double_special_chars_rejected(login_page):
    """Два спецсимвола подряд (кроме проверенных выше точек) должны блокировать отправку"""
    login_page.email_input.fill("john--doe@example.com")
    login_page.password_input.fill("ValidPass123")

    assert not login_page.is_submit_enabled()


# ---------- PASSWORD: длина 8-50 символов ----------

@pytest.mark.validation
@pytest.mark.parametrize("password", [
    "1234567",     # 7 символов — короче минимума
])
def test_password_shorter_than_8_rejected(login_page, password):
    """Пароль короче 8 символов должен блокировать отправку"""
    login_page.email_input.fill("valid@example.com")
    login_page.password_input.fill(password)

    assert not login_page.is_submit_enabled()


@pytest.mark.validation
def test_password_exceeds_50_chars_rejected(login_page):
    """Пароль длиннее 50 символов должен блокировать отправку"""
    login_page.email_input.fill("valid@example.com")
    login_page.password_input.fill("a" * 51)

    assert not login_page.is_submit_enabled()


@pytest.mark.validation
@pytest.mark.parametrize("password", [
    "12345678",          # ровно 8 символов — граничное значение, должно приниматься
    "a" * 50,             # ровно 50 символов — граничное значение, должно приниматься
])
def test_password_within_length_boundaries_accepted(login_page, password):
    """Пароль длиной ровно 8 или ровно 50 символов должен считаться валидным по длине"""
    login_page.email_input.fill("valid@example.com")
    login_page.password_input.fill(password)

    assert login_page.is_submit_enabled()
