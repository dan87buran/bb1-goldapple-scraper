import os

class ApiCategoryParser:
    def __init__(self):
        self.product_links = []

    def get_product_links(self):
        print("!!! Используется локальный файл data/links.txt")
        links_file = 'data/links.txt'
        if os.path.exists(links_file):
            print(f"Загружаем ссылки из {links_file}")
            with open(links_file, 'r', encoding='utf-8') as f:
                self.product_links = [line.strip() for line in f if line.strip()]
            print(f"Загружено {len(self.product_links)} ссылок.")
        else:
            print(f"Файл {links_file} не найден. Поместите список ссылок в data/links.txt")
        return self.product_links