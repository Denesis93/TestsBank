from playwright.sync_api import expect
from main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.utils.constants import URLs


def test_count_catalog(page):
    step_catalog = CatalogSteps(page)
    # авторизация
    step_catalog.login_as('standard_user', 'secret_sauce')
    # проверка, что на странице каталога 6 товаров
    assert step_catalog.count_prods_catalog() == 6

# проверка сортировки товаров по наименованию
def test_sort_by_name(page):
    step_catalog = CatalogSteps(page)
    # авторизация
    step_catalog.login_as('standard_user', 'secret_sauce')
    # проверка сортировки A-Z
    step_catalog.sort_catalog('az')
    assert step_catalog.get_products_names() == sorted(step_catalog.get_products_names()), 'Сортировка по наименованию A-Z не произвелась'
    # проверка сортировки Z-A
    step_catalog.sort_catalog('za')
    assert step_catalog.get_products_names() == sorted(
        step_catalog.get_products_names(), reverse=True), 'Сортировка по наименованию Z-A не произвелась'
    page.wait_for_timeout(2000)

# проверка сортировки товаров по цене
def test_sort_by_price(page):
    step_catalog = CatalogSteps(page)
    # авторизация
    step_catalog.login_as('standard_user', 'secret_sauce')
    # удостоверяюсь, что меню сортировки стало видимым
    expect(page.locator('.product_sort_container')).to_be_visible()

    # ставлю сортировку low to high
    step_catalog.sort_catalog('lohi')
    assert step_catalog.get_products_prices() == sorted(step_catalog.get_products_prices()), 'Сортировка по возрастанию цены не произвелась'

    # ставлю сортировку high to low
    step_catalog.sort_catalog('hilo')
    assert step_catalog.get_products_prices() == sorted(step_catalog.get_products_prices(), reverse=True), 'Сортировка по убыванию цены не произвелась'


# проверка добавления товара в корзину
def test_add_to_cart(page):
    step_catalog = CatalogSteps(page)
    #авторизация
    step_catalog.login_as('standard_user', 'secret_sauce')
    # добавление товара в корзину
    step_catalog.add_to_cart('Sauce Labs Onesie')
    # проверяю, что появилась иконка с количеством на кнопке корзины
    assert step_catalog.get_count_cart() == 1, "Количество товаров на иконке корзины не совпадает"

# проверка удаления товара из корзины
def test_remove_from_cart(page):
    step_catalog = CatalogSteps(page)
    # авторизация
    step_catalog.login_as('standard_user', 'secret_sauce')
    # добавление товара в корзину
    step_catalog.add_to_cart('Sauce Labs Onesie')
    # удаление товара из корзины
    step_catalog.remove_from_cart('Sauce Labs Onesie')
    # проверяю, что появилась иконка с количеством на кнопке корзины
    assert step_catalog.get_count_cart() == 0, "Количество товаров на иконке корзины не совпадает"

# проверка верного отображения деталей товара (при открытии карточки товара)
def test_open_details_product(page):
    step_catalog = CatalogSteps(page)
    # авторизация
    step_catalog.login_as('standard_user', 'secret_sauce')
    # получение имени и цены товара из каталога
    name_from_catalog, price_from_catalog = step_catalog.get_product_details_from_catalog('Sauce Labs Onesie')
    # получение имени и цены товара из карточки с деталями
    name_from_card, price_from_card = step_catalog.get_product_details_from_card('Sauce Labs Onesie')
    # проверка совпадения имени и цены товара в каталоге и карточке
    assert (name_from_catalog, price_from_catalog) == (name_from_card, price_from_card), "Данные не совпадают"


















