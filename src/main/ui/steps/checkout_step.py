import allure
from playwright.sync_api import Page, expect

from main.ui.pages.checkout_page import CheckoutPage


class CheckoutSteps:
    URL = 'https://www.saucedemo.com'
    def __init__(self, page):
        self.page = page
        self.checkout_page = CheckoutPage(page)

    @allure.step('Заполнение необходимых полей')
    def checkout_fill(self, first_name: str, last_name: str, zip_code: str):
        expect(self.checkout_page.first_name_input).to_be_visible()
        expect(self.checkout_page.last_name_input).to_be_visible()
        expect(self.checkout_page.zip_input).to_be_visible()
        # заполнение необходимых полей на станице Checkout
        self.checkout_page.first_name_input.fill(first_name)
        self.checkout_page.last_name_input.fill(last_name)
        self.checkout_page.zip_input.fill(zip_code)
        # нажатие на кнопку Continue
        expect(self.checkout_page.continue_btn).to_be_visible()
        self.checkout_page.continue_btn.click()

    @allure.step('Получение числовых значений без текста')
    def get_all_prices(self):
        item_total = float((self.checkout_page.item_total.inner_text()).replace('Item total: $', ''))
        tax = float((self.checkout_page.tax.inner_text()).replace('Tax: $', ''))
        total = float((self.checkout_page.total.inner_text()).replace('Total: $', ''))
        return {
                'item_total': item_total,
                'tax': tax,
                'total': total
                }


    @allure.step('Нажатие кнопки Finish для завершения заказа')
    def click_finish(self):
        self.checkout_page.finish_btn.click()


    @allure.step('Нажатие кнопки BAck Home для завершения заказа')
    def click_back_home(self):
        self.checkout_page.back_home_btn.click()





























