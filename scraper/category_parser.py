from bs4 import BeautifulSoup
from scraper.utils import wait

class CategoryParser:
    BASE_URL = 'https://goldapple.ru/parfumerija'

    def __init__(self, driver):
        self.driver = driver
        self.product_links = []

    def get_product_links(self):
        """
        Обходит все страницы категории и возвращает список URL товаров.
        """
        page = 1
        while True:
            url = f'{self.BASE_URL}?page={page}' if page > 1 else self.BASE_URL
            print(f"Загрузка страницы {page}: {url}")
            self.driver.get(url)
            wait(3)  # даём время загрузиться

            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            links = self._extract_links(soup)

            if not links:
                print("Ссылки не найдены, завершаем.")
                break

            self.product_links.extend(links)
            print(f"Найдено {len(links)} ссылок на странице {page}. Всего: {len(self.product_links)}")

            # Проверяем, есть ли следующая страница
            if not self._has_next_page(soup):
                break

            page += 1

        # Убираем дубликаты (на всякий случай)
        self.product_links = list(set(self.product_links))
        return self.product_links

    def _extract_links(self, soup):
        """
        Извлекает ссылки на товары из текущей страницы.
        Здесь нужно подставить реальный селектор.
        """
        # ПРЕДПОЛОЖИМ, что ссылки находятся в <a> с href, содержащим '/parfumerija/'
        # и не содержащим '?' (чтобы отсеять служебные ссылки)
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/parfumerija/' in href and '?' not in href:
                full_url = 'https://goldapple.ru' + href if href.startswith('/') else href
                links.append(full_url)
        return links

    def _has_next_page(self, soup):
        """
        Проверяет наличие кнопки "Следующая страница" или подобного элемента.
        Возвращает True, если есть.
        """
        # Ищем элемент пагинации – например, ссылку с текстом "Далее"
        next_btn = soup.find('a', string=re.compile(r'Далее|Следующая|>'))
        # Или можно проверить наличие класса "pagination__next"
        # Если не нашли – считаем, что страниц больше нет
        return bool(next_btn)