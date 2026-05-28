from playwright.sync_api import Page, expect


class CatalogPage:
    URL='https://www.saucedemo.com'
    def __init__(self, page: Page):
        self.page = page
        # карточки товара
        self.product_cards = page.locator('.inventory_item')
        # кнопка сортировки
        self.sort_menu_btn = page.locator('.product_sort_container')
        # наименования всех товаров
        self.product_names = page.locator('.inventory_item_name')
        # цены всех товаров
        self.product_prices = page.locator('.inventory_item_price')
        # кнопка корзины
        self.cart_btn = page.locator('#shopping_cart_container')
        # иконка количества на корзине
        self.cart_badge = page.locator(".shopping_cart_badge")
        # поле ввода юзернейма
        self.username_input = page.get_by_placeholder('Username')
        # поле ввода пароля
        self.password_input = page.get_by_placeholder('Password')
        # кнопка Логин
        self.login_btn = page.get_by_role('button', name='Login')
        # кнопка berger-menu
        self.burger_menu = page.get_by_role('button', name='Open Menu')
        # кнопка логаут
        self.logout_btn = page.get_by_role('link', name='Logout')
        # # кнопка внутри карточки товара, отвечающая за добавить/удалить из корзины
        self.details = page.locator('.inventory_details')
        self.inventory_items = page.locator('.inventory_item')

    # переход на страницу авторизации
    def open(self):
        self.page.goto(self.URL)

    # авторизация
    def login(self, username, password):
        self.open()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_btn.click()

    # логаут
    def logout(self):
        self.burger_menu.click()
        expect(self.logout_btn).to_be_visible()
        self.logout_btn.click()

    # сортировка (передаём опшны az, za, hilo, lohi)
    def sort(self, option):
        self.sort_menu_btn.select_option(option)

    # добавление товара в корзину
    def add_to_cart(self, prod_name):
        prod_path_card = self.product_cards.filter(has_text=prod_name)
        button = prod_path_card.locator('button')
        button.click()
        return button

    # удаление товара из корзины
    def remove_from_cart(self, prod_name):
        prod_path_card = self.product_cards.filter(has_text=prod_name)
        button = prod_path_card.locator('button')
        button.click()
        return button

    # получение кнопки внутри карточки товара
    def get_button(self, prod_name):
        return self.product_cards.filter(has_text=prod_name).get_by_role('button')

    # получение всех наименований товаров
    def get_products_names(self):
        return self.product_names.all_inner_texts()

    # получение цен всех товаров
    def get_products_prices(self):
        prices_text = self.product_prices.all_inner_texts()
        return [float(price.replace('$', '')) for price in prices_text]

    # получение цены и наименования продукта из каталога
    def get_product_data_from_catalog(self, prod_name):
        card = self.product_cards.filter(has_text=prod_name)
        catalog_name = card.locator('.inventory_item_name').inner_text()
        price_text = card.locator('.inventory_item_price').inner_text()
        price = float(price_text.replace('$', ''))
        return catalog_name, price

    # получение цены и наименования продукта из карточки с деталями
    def get_product_data_from_card(self, prod_name):
        self.product_names.filter(has_text=prod_name).click()
        expect(self.details.locator('.inventory_details_name.large_size')).to_be_visible()
        product_name_detail = self.details.locator('.inventory_details_name.large_size').inner_text()
        price_text = self.details.locator('.inventory_details_price').inner_text()
        price = float(price_text.replace('$', ''))
        return product_name_detail, price


    # подсчёт товаров на странице
    def count_prods_catalog(self):
        return self.inventory_items.count()

    # подсчёт количества у иконки корзины
    def cart_badge_count(self):
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0





















