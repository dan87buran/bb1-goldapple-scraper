import re
from bs4 import BeautifulSoup
from scraper.utils import wait, extract_price, extract_country

class ProductParser:
    def __init__(self, driver):
        self.driver = driver

    def parse(self, url):
        """
        Загружает страницу товара и возвращает словарь с данными.
        """
        print(f"Парсинг товара: {url}")
        self.driver.get(url)
        wait(2)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        # Здесь мы будем использовать найденные селекторы.
        # Пока оставим заглушки – их надо будет заменить реальными.
        data = {
            'Ссылка на продукт': url,
            'Наименование': self._get_title(soup),
            'Цена': self._get_price(soup),
            'Рейтинг пользователей': self._get_rating(soup),
            'Описание продукта': self._get_description(soup),
            'Инструкция по применению': self._get_instructions(soup),
            'Страна-производитель': self._get_country(soup),
        }
        return data

    def _get_title(self, soup):
        """Извлечение названия товара."""
        # Обычно это h1
        h1 = soup.find('h1')
        return h1.text.strip() if h1 else ''

    def _get_price(self, soup):
        """Извлечение цены."""
        # Попробуем найти элемент с ценой. Часто это класс 'current-price' или 'price'
        # Но мы также можем использовать регулярное выражение на весь текст.
        # Сначала ищем по селектору:
        price_elem = soup.select_one('span.current-price, span.price, div.price')
        if price_elem:
            return extract_price(price_elem.text)
        # Если не нашли, пробуем найти любой текст с рублём
        page_text = soup.get_text()
        return extract_price(page_text)

    def _get_rating(self, soup):
        """Извлечение рейтинга (например, 4.5)."""
        # Ищем элемент с рейтингом. Может быть класс 'rating' или 'stars'
        rating_elem = soup.select_one('span.rating-value, div.rating span')
        if rating_elem:
            return rating_elem.text.strip()
        # Попробуем найти число с плавающей точкой рядом со словом "рейтинг"
        match = re.search(r'(\d[.,]\d)', soup.text)
        if match:
            return match.group(1).replace(',', '.')
        return ''

    def _get_description(self, soup):
        """Извлечение описания продукта."""
        # Ищем блок с описанием. Может быть div с классом 'description' или 'product-description'
        desc_elem = soup.select_one('div.description, div.product-description, div[data-ga-product-block="description"]')
        if desc_elem:
            return desc_elem.text.strip()
        return ''

    def _get_instructions(self, soup):
        """Извлечение инструкции по применению."""
        # Ищем текст "Способ применения" или "Применение"
        # Можно найти элемент, содержащий такой текст, и взять его родителя
        elem = soup.find(string=re.compile(r'Способ\s+применения|Применение|Инструкция'))
        if elem:
            parent = elem.find_parent('div')
            if parent:
                return parent.text.strip()
            return elem.strip()
        return ''

    def _get_country(self, soup):
        """Извлечение страны-производителя через регулярные выражения."""
        return extract_country(soup.text)