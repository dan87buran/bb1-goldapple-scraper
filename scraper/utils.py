import re
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

def get_driver(headless=False):
    """Возвращает драйвер Firefox."""
    service = Service(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument('--headless')
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)
    return webdriver.Firefox(service=service, options=options)

def wait(seconds=2):
    time.sleep(seconds)

def extract_price(text):
    match = re.search(r'(\d{1,3}(?:\s?\d{3})*)\s?₽', text)
    if match:
        return match.group(1).replace(' ', '')
    return ''

def extract_country(text):
    """
    Ищет страну-производителя в тексте.
    Поддерживает форматы:
        - Страна производитель: Франция
        - Страна: Франция
        - Производитель: Италия
        - Made in Germany
    """
    patterns = [
        # Ищем "Страна" или "Производитель" или "Made in", затем двоеточие (необязательно),
        # затем захватываем название страны (буквы и пробелы) до запятой, точки или конца строки.
        r'(?:Страна|Производитель|Made in)\s*:?\s*([А-Яа-яA-Za-z\s]+?)(?:,|\.|$)',
    ]
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ''