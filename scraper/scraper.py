from scraper.api_category_parser import ApiCategoryParser
from scraper.product_parser import ProductParser
from scraper.exporter import DataExporter

class GoldAppleScraper:
    def __init__(self, driver):
        self.driver = driver
        self.category_parser = ApiCategoryParser()  # теперь всегда читает из файла
        self.product_parser = ProductParser(driver)
        self.exporter = DataExporter()

    def run(self, output_file='data/products.csv'):
        print("Сбор ссылок на товары через локальный файл...")
        links = self.category_parser.get_product_links()
        print(f"Всего найдено товаров: {len(links)}")

        results = []
        for idx, url in enumerate(links, start=1):
            print(f"Обработка {idx}/{len(links)}")
            try:
                product_data = self.product_parser.parse(url)
                results.append(product_data)
            except Exception as e:
                print(f"Ошибка при обработке {url}: {e}")

        self.exporter.save_to_csv(results, output_file)
        print("Готово!")