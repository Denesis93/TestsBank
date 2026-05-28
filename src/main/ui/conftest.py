import pytest
from playwright.sync_api import sync_playwright, expect


# 🔹 Фикстура уровня СЕССИИ
# создаётся ОДИН раз на все тесты
@pytest.fixture(scope="session")
def playwright_instance():

    # запускаем Playwright (движок, который управляет браузерами)
    # with гарантирует, что он корректно закроется после всех тестов
    with sync_playwright() as playwright:

        # отдаём playwright в другие фикстуры/тесты
        yield playwright

    # ⬅️ сюда выполнение вернётся после ВСЕХ тестов
    # и Playwright автоматически завершится (thanks to "with")


# 🔹 Фикстура браузера (тоже на всю сессию)
@pytest.fixture(scope="session")
def browser(playwright_instance):

    # запускаем браузер (Chromium)
    # headless=False → браузер будет открываться (видно UI)
    browser = playwright_instance.chromium.launch(headless=False)

    # отдаём браузер в тесты
    yield browser

    # ⬅️ после ВСЕХ тестов
    # закрываем браузер
    browser.close()


# 🔹 Фикстура страницы (создаётся для КАЖДОГО теста)
@pytest.fixture(scope="function")
def page(browser):

    # создаём новый "контекст браузера"
    # это как отдельный чистый профиль (куки, локалка и т.д.)
    context = browser.new_context()

    # создаём новую вкладку (page)
    page = context.new_page()

    # отдаём страницу в тест
    yield page

    # ⬅️ после КАЖДОГО теста
    # закрываем контекст (и все вкладки внутри)
    context.close()

"""Стандартный URL"""

@pytest.fixture
def url():
    return 'https://www.saucedemo.com'

"""Логин standard user"""

@pytest.fixture
def auth_page(page, url):
    page.goto(url)
    # ввожу логин
    page.get_by_placeholder('Username').fill('standard_user')
    # ввожу пароль
    page.get_by_placeholder('Password').fill('secret_sauce')
    # жму кнопку "логин"
    page.get_by_role('button', name='Login').click()
    return page






































