import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_driver(headless=True):
    """Настраивает и возвращает экземпляр ChromeDriver."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def wait(seconds=2):
    """Принудительная задержка (чтобы не нагружать сервер)."""
    time.sleep(seconds)

def extract_price(text):
    """
    Извлекает цену из строки, например: '2 599 ₽' -> '2599'
    Использует регулярное выражение.
    """
    match = re.search(r'(\d{1,3}(?:\s?\d{3})*)\s?₽', text)
    if match:
        # Убираем пробелы внутри числа
        return match.group(1).replace(' ', '')
    return ''

def extract_country(text):
    """
    Ищет страну-производителя в тексте с помощью регулярных выражений.
    """
    patterns = [
        r'Страна[:\s]+([А-Яа-я\s]+)',
        r'Производитель[:\s]+([А-Яа-я\s]+)',
        r'Made in\s+([A-Za-z\s]+)'
    ]
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ''