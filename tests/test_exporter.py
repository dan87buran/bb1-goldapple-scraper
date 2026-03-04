import csv
import os
import pytest
from scraper.exporter import DataExporter

def test_save_to_csv(tmp_path):
    """Проверяет сохранение данных в CSV."""
    exporter = DataExporter()
    data = [
        {
            'Ссылка на продукт': 'https://goldapple.ru/test',
            'Наименование': 'Test Product',
            'Цена': '1000',
            'Рейтинг пользователей': '4.5',
            'Описание продукта': 'Test description',
            'Инструкция по применению': 'Test instructions',
            'Страна-производитель': 'Россия'
        }
    ]
    # Используем временную директорию pytest
    test_file = tmp_path / "test.csv"
    exporter.save_to_csv(data, filename=str(test_file))

    # Проверяем, что файл создан
    assert os.path.exists(test_file)

    # Читаем файл и проверяем содержимое
    with open(test_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]['Наименование'] == 'Test Product'
        assert rows[0]['Цена'] == '1000'

def test_save_to_csv_empty(tmp_path):
    """Проверяет, что при пустых данных файл не создаётся (или создаётся без записей)."""
    exporter = DataExporter()
    test_file = tmp_path / "empty.csv"
    exporter.save_to_csv([], filename=str(test_file))
    # Если данных нет, файл не должен создаваться (или быть пустым)
    if os.path.exists(test_file):
        with open(test_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 0  # Файл может быть пустым