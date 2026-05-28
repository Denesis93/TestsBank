from playwright.sync_api import expect
from main.ui.steps.basket_steps import BasketSteps
from src.main.ui.utils.constants import URLs

# проверка добавления товара в корзину
def test_add_to_cart(page):
    basket_step = BasketSteps(page)
    # авторизация
    basket_step.login_as('standard_user', 'secret_sauce')
    # добавление товаров в корзину
    basket_step.add_to_cart('Sauce Labs Fleece Jacket', 'Sauce Labs Bolt T-Shirt')
    # проверка количества на иконке корзины
    assert basket_step.get_cart_badge_count() == 2, "Количество товаров на иконке корзины не совпадает"
    # открытие корзины
    basket_step.open_cart()
    # проверка перехода на нужную страницу
    expect(page).to_have_url(URLs.CART_URL)
    # проверка количества товаров в корзине
    assert basket_step.get_count_cart() == 2, "Количество товаров не совпадает"
    # проверка, что в корзине нужные товары
    expected_names = basket_step.get_products_names_in_cart()
    assert 'Sauce Labs Fleece Jacket' in expected_names, "Товар Sauce Labs Fleece Jacket не добавился в корзину"
    assert 'Sauce Labs Bolt T-Shirt' in expected_names, "Товар Sauce Labs Bolt T-Shirt не добавился в корзину"

# проверка удаления товаров из корзины
def test_remove_from_cart(page):
    basket_step = BasketSteps(page)
    # авторизация
    basket_step.login_as('standard_user', 'secret_sauce')
    # добавление товаров в корзину
    basket_step.add_to_cart('Sauce Labs Fleece Jacket', 'Sauce Labs Bolt T-Shirt')
    # проверка количества на иконке корзины
    assert basket_step.get_cart_badge_count() == 2, "Количество товаров на иконке корзины не совпадает"
    # открытие корзины
    basket_step.open_cart()
    # удаляю товары
    basket_step.click_remove_button('Sauce Labs Fleece Jacket', 'Sauce Labs Bolt T-Shirt')












