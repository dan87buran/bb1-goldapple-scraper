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
        wait(3)  # ждём загрузки динамического контента

        soup = BeautifulSoup(self.driver.page_source, 'lxml')

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
        """Название товара (бренд + наименование) из h1."""
        h1 = soup.select_one('h1._ga-pdp-title__heading_1yrfv_155')
        if h1:
            return h1.get_text(strip=True)
        return ''

    def _get_price(self, soup):
        """Цена из элемента с классом _ga-price_1dj1y_114."""
        price_elem = soup.select_one('._ga-price_1dj1y_114')
        if price_elem:
            return extract_price(price_elem.get_text())
        return ''

    def _get_rating(self, soup):
        """Рейтинг из meta-тега с itemprop='ratingValue'."""
        rating_meta = soup.find('meta', attrs={'itemprop': 'ratingValue'})
        if rating_meta and rating_meta.get('content'):
            return rating_meta['content']
        return ''

    def _get_description(self, soup):
        """Описание из вкладки 'Описание'."""
        # Ищем div с атрибутом text="Описание", внутри него блок с описанием
        desc_tab = soup.find('div', attrs={'text': 'Описание'})
        if desc_tab:
            desc_elem = desc_tab.find('div', class_='_ga-pdp-wysiwyg_rmnt6_55')
            if desc_elem:
                return desc_elem.get_text(strip=True)
        # Запасной вариант: поиск по itemprop
        desc = soup.find(attrs={'itemprop': 'description'})
        if desc:
            return desc.get_text(strip=True)
        return ''

    def _get_instructions(self, soup):
        """Инструкция из вкладки 'Применение'."""
        instr_tab = soup.find('div', attrs={'text': 'Применение'})
        if instr_tab:
            instr_elem = instr_tab.find('div', class_='_ga-pdp-wysiwyg_rmnt6_55')
            if instr_elem:
                return instr_elem.get_text(strip=True)
        return ''

    def _get_country(self, soup):
        """
        Страна-производитель. Ищем во вкладке 'Дополнительная информация'
        или в подзаголовке бренда.
        """
        # Сначала ищем в дополнительной информации
        info_tab = soup.find('div', attrs={'text': 'Дополнительная информация'})
        if info_tab:
            info_text = info_tab.get_text()
            country = extract_country(info_text)
            if country:
                return country

        # Если не нашли, пробуем из подзаголовка бренда
        brand_subtitle = soup.select_one('._ga-pdp-tabs-content__sub-title_1ikd4_223')
        if brand_subtitle:
            return brand_subtitle.get_text(strip=True)

        return ''