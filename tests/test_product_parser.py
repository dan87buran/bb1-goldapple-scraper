import re
import pytest
from bs4 import BeautifulSoup
from scraper.product_parser import ProductParser
from scraper.utils import extract_price, extract_country

@pytest.fixture
def product_html():
    """Загружает сохранённый HTML страницы товара."""
    with open('tests/fixtures/product_page.html', 'r', encoding='utf-8') as f:
        return f.read()

@pytest.fixture
def soup(product_html):
    """Возвращает объект BeautifulSoup для тестов."""
    return BeautifulSoup(product_html, 'lxml')

def test_get_title(soup):
    """Проверяет извлечение названия товара."""
    parser = ProductParser(None)  # driver не нужен
    title = parser._get_title(soup)
    # Ожидаем, что название содержит бренд и имя
    assert 'Maison Francis Kurkdjian' in title
    assert 'Gentle Fluidity Gold' in title

def test_get_price(soup):
    parser = ProductParser(None)
    price = parser._get_price(soup)
    # Ожидаем цену без пробелов, например "22510"
    assert price.isdigit()
    assert int(price) > 0

def test_get_rating(soup):
    parser = ProductParser(None)
    rating = parser._get_rating(soup)
    # Рейтинг должен быть числом с плавающей точкой (как строка)
    assert rating.replace('.', '').isdigit()
    assert 0 <= float(rating) <= 5

def test_get_description(soup):
    parser = ProductParser(None)
    description = parser._get_description(soup)
    assert description, "Описание не должно быть пустым"
    assert len(description) > 20

def test_get_instructions(soup):
    parser = ProductParser(None)
    instructions = parser._get_instructions(soup)
    # Инструкция может быть пустой, но мы хотя бы проверяем, что это строка
    assert isinstance(instructions, str)

def test_get_country(soup):
    parser = ProductParser(None)
    country = parser._get_country(soup)
    # Страна может быть найдена или пуста
    assert isinstance(country, str)
    # Если страна найдена, она не должна быть слишком короткой
    if country:
        assert len(country) > 2

def test_get_title_missing(soup):
    """Проверяет, что при отсутствии заголовка возвращается пустая строка."""
    # Удалим элемент h1 из копии soup
    soup_copy = BeautifulSoup(str(soup), 'lxml')
    h1 = soup_copy.find('h1')
    if h1:
        h1.decompose()
    parser = ProductParser(None)
    title = parser._get_title(soup_copy)
    assert title == ''

def test_get_instructions_missing(soup):
    """Проверяет, что при отсутствии инструкции возвращается пустая строка."""
    soup_copy = BeautifulSoup(str(soup), 'lxml')
    instr_tab = soup_copy.find('div', attrs={'text': 'Применение'})
    if instr_tab:
        instr_tab.decompose()
    parser = ProductParser(None)
    instructions = parser._get_instructions(soup_copy)
    assert instructions == ''

