import allure
from playwright.sync_api import Page, expect

from main.ui.pages.catalog_page import CatalogPage
from main.ui.pages.login_page import LoginPage


class AuthSteps:
    URL = 'https://www.saucedemo.com'
    def __init__(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.catalog_page = CatalogPage(page)

    @allure.step('Открытие страницы логина')
    def open_login_page(self):
        self.login_page.open()
        return self

    @allure.step('Заполнение полей логин и пароль и нажатие кнопки Логин')
    def login_as(self, username, password):
        self.login_page.login(username, password)
        return self

    @allure.step('Получение текста ошибки')
    def get_error(self):
        return self.login_page.error_text

    @allure.step('Разлогин')
    def logout(self):
        self.catalog_page.burger_menu.click()
        expect(self.catalog_page.logout_btn).to_be_visible()
        self.catalog_page.logout_btn.click()




































