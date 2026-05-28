import allure
from playwright.sync_api import Page, expect

from main.ui.pages.catalog_page import CatalogPage
from main.ui.pages.login_page import LoginPage

class CatalogSteps:
    BASE_URL = 'https://www.saucedemo.com'
    def __init__(self, page: Page):
        self.page = page
        self.catalog_page = CatalogPage(page)

    @allure.step('Авторизация под юзером {username}')
    def login_as(self, username, password):
        self.catalog_page.login(username, password)
        return self

    @allure.step('Подсчёт товаров на странице')
    def count_prods_catalog(self):
        return self.catalog_page.count_prods_catalog()

    @allure.step('Сортировка товаров')
    def sort_catalog(self, option):
        self.catalog_page.sort_menu_btn.select_option(option)
        return self

    @allure.step('Получение всех наименований товаров из каталога')
    def get_products_names(self):
        return self.catalog_page.product_names.all_inner_texts()

    @allure.step('Получение всех цен товаров из каталога')
    def get_products_prices(self):
        prices_text = self.catalog_page.product_prices.all_inner_texts()
        return [float(price.replace('$', '')) for price in prices_text]

    @allure.step('Добавление в корзину товара {prod_name}')
    def add_to_cart(self, prod_name):
        button = self.catalog_page.add_to_cart(prod_name)
        expect(button).to_have_text('Remove')
        return self

    @allure.step('Удаление из корзины товара {prod_name}')
    def remove_from_cart(self, prod_name):
        button = self.catalog_page.add_to_cart(prod_name)
        expect(button).to_have_text('Add to cart')
        return self


    @allure.step('Подсчёт количества товаров в корзине')
    def get_count_cart(self):
        return self.catalog_page.cart_badge_count()

    @allure.step('Получение цены и наименования продукта из карточки товара с деталями')
    def get_product_details_from_card(self, prod_name):
        return self.catalog_page.get_product_data_from_card(prod_name)


    @allure.step('Получение цены и наименования продукта из каталога')
    def get_product_details_from_catalog(self, prod_name):
        return self.catalog_page.get_product_data_from_catalog(prod_name)


    @allure.step('Выполнение логаута')
    def logout(self):
        self.catalog_page.logout()
        return self









