from playwright.sync_api import Page

class CheckoutPage:
    BASE_URL = 'https://www.saucedemo.com/checkout-step-one.html'
    def __init__(self, page):
        self.page = page
        # кнопка checkout
        self.checkout_btn = page.get_by_role('button', name='Checkout')
        # текст на странице чекаута на первом шаге
        self.checkout_s1_title = page.locator('.title', has_text='Checkout: Your Information')
        # необходимые поля на странице Checkout
        self.first_name_input = page.get_by_placeholder('First Name')
        self.last_name_input = page.get_by_placeholder('Last Name')
        self.zip_input = page.get_by_placeholder('Zip/Postal Code')
        # кнопка Continue на странице Checkout
        self.continue_btn = page.get_by_role('button', name='Continue')
        # текст на странице чекаута на втором шаге
        self.checkout_s2_title = page.locator('.title', has_text='Checkout: Overview')
        # контейнер с товарами на странице чекаута
        self.checkout_cont = page.locator('.checkout_summary_container')
        # путь к item total на странице чекаута
        self.item_total = page.locator('.summary_subtotal_label')
        # путь к tax
        self.tax = page.locator('.summary_tax_label')
        # путь к total
        self.total = page.locator('.summary_total_label')
        # кнопка Finish
        self.finish_btn = page.get_by_role('button', name='Finish')
        # контейнер финальной страницы
        self.finish = page.locator('#checkout_complete_container')
        # кнопка Back Home
        self.back_home_btn = page.get_by_role('button', name='Back Home')


    # нажатие на кнопку Checkout
    def open_checkout(self):
        self.checkout_btn.click()

    # заполнение необходимых полей на станице Checkout
    def fill_checkout_fields(self, first_name: str, last_name: str, zip_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.zip_input.fill(zip_code)

    # нажатие на кнопку Continue
    def click_continue_btn(self):
        self.continue_btn.click()

    # возврат наименований товаров со страницы чекаута
    def prods_checkout(self, product_name: str):
        return self.checkout_cont.locator('.inventory_item_name', has_text=product_name)

    # удаляю текст и оставляю только цену
    def get_item_total_price(self):
        return float((self.item_total.inner_text()).replace('Item total: $', ''))

    # удаляю текст и оставляю только цену tax
    def get_tax(self):
        return float((self.tax.inner_text()).replace('Tax: $', ''))

    # удаляю текст и оставляю только цену
    def get_total_price(self):
        return float((self.total.inner_text()).replace('Total: $', ''))

    # нажатие на кнопку Finish
    def click_finish(self):
        self.finish_btn.click()

    # нажатие на кнопку Back Home
    def click_back_home(self):
        self.back_home_btn.click()










































