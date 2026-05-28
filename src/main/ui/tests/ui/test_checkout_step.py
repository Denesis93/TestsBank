from playwright.sync_api import expect
from src.main.ui.utils.constants import URLs
from main.ui.steps.basket_steps import BasketSteps
from main.ui.steps.catalog_steps import CatalogSteps
from main.ui.steps.checkout_step import CheckoutSteps


# проверка оформления заказа
def test_checkout(page):
    checkout_steps = CheckoutSteps(page)
    basket_steps = BasketSteps(page)
    catalog_steps = CatalogSteps(page)

    # авторизация
    catalog_steps.login_as('standard_user', 'secret_sauce')
    # добавление товаров в корзину
    basket_steps.add_to_cart('Sauce Labs Fleece Jacket', 'Sauce Labs Bolt T-Shirt')
    # открытие корзины
    basket_steps.open_cart()
    # получаю итоговую стоимость товаров в корзине
    total_price_in_cart = basket_steps.get_total_price_in_cart()
    # перехожу к checkout
    basket_steps.go_to_checkout()
    # проверка, что перешёл на нужную страницу
    expect(page).to_have_url(URLs.CHECKOUT_1st_URL)
    # заполнение необходимых полей
    checkout_steps.checkout_fill('Denis', 'Shaev', '654011')
    # проверка, что перешёл на нужную страницу
    expect(page).to_have_url(URLs.CHECKOUT_2nd_URL)

    # проверяю, что на странице отображаются нужные товары
    expect(basket_steps.get_prods_name_checkout('Sauce Labs Fleece Jacket')).to_be_visible()
    expect(basket_steps.get_prods_name_checkout('Sauce Labs Bolt T-Shirt')).to_be_visible()

    # возвращаю tax и total
    prices = checkout_steps.get_all_prices()
    tax = prices['tax']
    total = prices['total']
    # проверяю, что сумма товаров совпадает
    assert round(total_price_in_cart +tax, 2) == round(total, 2), 'Сумма товаров не совпадает'

    # жму кнопку Finish для завершения заказа
    checkout_steps.click_finish()
    # проверяю, что перешёл на нужную страницу
    expect(page).to_have_url(URLs.CHECKOUT_COMPLETE_URL)
    # жму кнопку Back Home
    checkout_steps.click_back_home()
    # проверяю, что попал на страницу с каталогом
    expect(page).to_have_url(URLs.CATALOG_URL)


# проверка оформления заказа с пустой корзиной
# по-хорошему тут должна появляться ошибка при попытке оформить заказ
# с пустой корзиной, но на учебном сайте этого не предусмотрено
def test_checkout_with_no_items(page):
    checkout_steps = CheckoutSteps(page)
    basket_steps = BasketSteps(page)
    catalog_steps = CatalogSteps(page)

    # авторизация
    catalog_steps.login_as('standard_user', 'secret_sauce')
    # добавление товаров в корзину
    #basket_steps.add_to_cart('Sauce Labs Fleece Jacket', 'Sauce Labs Bolt T-Shirt')
    # открытие корзины
    basket_steps.open_cart()
    # перехожу к checkout
    basket_steps.go_to_checkout()
    # проверка, что перешёл на нужную страницу
    expect(page).to_have_url(URLs.CHECKOUT_1st_URL)
    # заполнение необходимых полей
    checkout_steps.checkout_fill('Denis', 'Shaev', '654011')
    # проверка, что перешёл на нужную страницу
    expect(page).to_have_url(URLs.CHECKOUT_2nd_URL)
    # проверяю, что на странице все цены равны 0
    prices = checkout_steps.get_all_prices()
    item_total = prices['item_total']
    tax = prices['tax']
    total = prices['total']
    assert item_total == 0, 'item_total не равен 0'
    assert tax == 0, 'tax не равен 0'
    assert total == 0, 'total не равен 0'









































