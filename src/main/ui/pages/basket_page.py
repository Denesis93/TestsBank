from playwright.sync_api import Page

class BasketPage:
    URL = 'https://www.saucedemo.com'
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder('Username')
        self.password_input = page.get_by_placeholder('Password')
        self.login_btn = page.get_by_role('button', name='Login')
        # карточки товара
        self.product_cards = page.locator('.inventory_item')
        # наименования всех товаров
        self.product_names = page.locator('.inventory_item_name')
        # корзина
        self.cart = page.locator('.shopping_cart_link')
        # товары в корзине
        self.items_in_cart = page.locator('.cart_item')
        # иконка количества на корзине
        self.cart_badge = page.locator(".shopping_cart_badge")


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



        # открытие сайта
    def open(self):
        self.page.goto(self.URL)

    # логин
    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_btn.click()


    # добавление товаров в корзину
    def add_to_cart(self, *prod_names: str):
        for name in prod_names:
            card = self.product_cards.filter(has_text=name)
            card.get_by_role('button', name='Add to cart').click()

    # открытие корзины
    def open_cart(self):
        self.cart.click()

    # подсчёт количества у иконки корзины
    def cart_badge_count(self):
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    # подсчёт кол-ва товаров в корзине
    def count_items(self):
        return self.items_in_cart.count()


    # возврат наименований товаров из корзины
    def prods_in_cart(self):
       return self.items_in_cart.locator('.inventory_item_name').all_inner_texts()



    # удаление товаров из корзины
    def remove_from_cart(self, *prod_names: str):
        for name in prod_names:
            prod_name = self.items_in_cart.filter(has_text=name)
            prod_name.get_by_role('button', name='Remove').click()

    # получение кнопки Remove внутри товары в корзине
    def get_remove_button(self, prod_name: str):
        return self.items_in_cart.filter(has_text=prod_name).get_by_role('button', name='Remove')


    # получаю итоговую стоимость товаров в корзине
    def get_total_price_in_cart(self):
        # получаю все цены всех товаров (удобно, чтоб не считать товары самому)
        all_prices_text = self.items_in_cart.locator('.inventory_item_price').all_inner_texts()
        # считаю сумму с помощью генератора generator expression
        return sum(float(price.replace('$', '')) for price in all_prices_text)

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
    def click_finish_btn(self):
        self.finish_btn.click()

    # нажатие на кнопку Back Home
    def click_back_home_btn(self):
        self.back_home_btn.click()





