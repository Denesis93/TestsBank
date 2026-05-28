from playwright.sync_api import Page

class LoginPage:
    URL = 'https://www.saucedemo.com'
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder('Username')
        self.password_input = page.get_by_placeholder('Password')
        self.login_btn = page.get_by_role('button', name='Login')
        self.error_text = page.locator('h3[data-test="error"]')

    # метод для открытия страницы авторизации
    def open(self):
        self.page.goto(self.URL)

    # метод для логина
    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_btn.click()

    # метод для получения текста ошибки
    def get_error_text(self):
       return self.error_text.inner_text()













