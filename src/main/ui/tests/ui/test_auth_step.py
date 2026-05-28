from src.main.ui.utils.constants import URLs
from playwright.sync_api import expect
from main.ui.steps.auth_steps import AuthSteps
from main.ui.steps.catalog_steps import CatalogSteps

# проверка авторизации
def test_open_login_page(page):
    # создаю объект StepObject
    auth_steps = AuthSteps(page)
    catalog_steps = CatalogSteps(page)
    # открываю страницу авторизации, ввожу логин/пароль и жму кнопку Логин
    auth_steps.open_login_page().login_as('standard_user', 'secret_sauce')
    # проверяю, что оказался на нужной странице
    expect(page).to_have_url(URLs.CATALOG_URL)
    # проверяю, что на странице каталога 6 товаров
    assert catalog_steps.count_prods_catalog() == 6, "Количество товаров не совпадает"

# проверка авторизации заблокированным пользователем
def test_blocked_user_login(page):
    # создаю объект класса LoginSteps
    auth_steps = AuthSteps(page)
    # открываю нужную страницу и ввожу логин
    auth_steps.open_login_page().login_as('locked_out_user', 'secret_sauce')
    # проверяю текст ошибки
    expect(auth_steps.get_error()).to_contain_text('this user has been locked out')

# проверка разлогина стандартным юзером
def test_logout(page):
    # создаю объект StepObject
    auth_steps = AuthSteps(page)
    # открываю страницу авторизации, ввожу логин/пароль и жму кнопку Логин
    auth_steps.open_login_page().login_as('standard_user', 'secret_sauce')
    # разлогин
    auth_steps.logout()
    # проверяю, что перешёл на нужную страницу после разлогина
    expect(page).to_have_url(f'{URLs.BASE_URL}/')
    expect(page.get_by_role('button', name='Login')).to_be_visible()


# проверка разлогина визуальным юзером
def test_logout_visual_user(page):
    # создаю объект StepObject
    auth_steps = AuthSteps(page)
    # открываю страницу авторизации, ввожу логин/пароль и жму кнопку Логин
    auth_steps.open_login_page().login_as('visual_user', 'secret_sauce')
    # разлогин
    auth_steps.logout()
    # проверяю, что перешёл на нужную страницу после разлогина
    expect(page).to_have_url(f'{URLs.BASE_URL}/')
    expect(page.get_by_role('button', name='Login')).to_be_visible()



















