import csv

class DataExporter:
    @staticmethod
    def save_to_csv(data, filename='data/products.csv'):
        """
        Сохраняет данные в CSV-файл. Если файл существует, перезаписывает.
        """
        if not data:
            print("Нет данных для сохранения.")
            return
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"Данные сохранены в {filename}")
