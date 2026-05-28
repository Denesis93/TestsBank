import allure
from playwright.sync_api import Page, expect
from main.ui.pages.basket_page import BasketPage


class BasketSteps:
    URL = 'https://www.saucedemo.com'
    def __init__(self, page: Page):
        self.page = page
        self.basket_page = BasketPage(page)

    @allure.step('Авторизация под юзером {username}')
    def login_as(self, username, password):
        self.basket_page.open()
        self.basket_page.login(username, password)
        return self

    @allure.step('Добавление товаров в корзину {prod_names}')
    def add_to_cart(self, *prod_names: str):
        self.basket_page.add_to_cart(*prod_names)
        return self

    @allure.step('Открытие корзины')
    def open_cart(self):
        self.basket_page.open_cart()
        return self

    @allure.step('Подсчёт количества товаров в корзине')
    def get_count_cart(self):
        return self.basket_page.cart_badge_count()

    @allure.step('Подсчёт количества у иконки корзины')
    def get_cart_badge_count(self):
        return self.basket_page.cart_badge_count()

    @allure.step('Получение названий товаров в корзине')
    def get_products_names_in_cart(self,):
        return self.basket_page.prods_in_cart()

    @allure.step('Нажатие на кнопку Remove')
    def click_remove_button(self, *prod_names):
        self.basket_page.remove_from_cart(*prod_names)
        return self


    @allure.step('Получение итоговой стоимости товаров в корзине')
    def get_total_price_in_cart(self):
        return self.basket_page.get_total_price_in_cart()

    @allure.step('Переход к checkout')
    def go_to_checkout(self):
        expect(self.basket_page.checkout_btn).to_be_visible()
        self.basket_page.open_checkout()
        return self

    @allure.step('Заполнение необходимых полей на станице Checkout')
    def fill_checkout_fields(self, first_name: str, last_name: str, zip_code: str):
        self.basket_page.fill_checkout_fields(first_name, last_name, zip_code)
        return self

    @allure.step('Нажатие на кнопку Continue')
    def click_continue_btn(self):
        expect(self.basket_page.continue_btn).to_be_visible()
        self.basket_page.click_continue_btn()
        return self

    @allure.step('Возврат наименований товаров со страницы чекаута')
    def get_prods_name_checkout(self, product_name):
        return self.basket_page.prods_checkout(product_name)
