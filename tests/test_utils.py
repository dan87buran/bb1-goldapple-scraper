import pytest
from scraper.utils import extract_price, extract_country

def test_extract_price():
    assert extract_price('2 599 ₽') == '2599'
    assert extract_price('1290₽') == '1290'
    assert extract_price('Цена: 1 230 ₽') == '1230'
    assert extract_price('Бесплатно') == ''

def test_extract_country():
    assert extract_country('Страна производитель: Франция') == 'Франция'
    assert extract_country('Производитель: Италия') == 'Италия'
    assert extract_country('Made in Germany') == 'Germany'
    assert extract_country('') == ''

def test_extract_price_no_match():
    assert extract_price('Бесплатно') == ''
    assert extract_price('Цена: 0 ₽') == '0'

def test_extract_country_no_match():
    assert extract_country('Не указано') == ''
    assert extract_country('') == ''