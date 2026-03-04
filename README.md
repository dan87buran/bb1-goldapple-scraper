# Парсер товаров Gold Apple (BB1)

Проект для сбора информации о товарах из раздела «Парфюмерия» интернет-магазина Gold Apple.

## Технологии
- Python 3.11+
- Selenium (Firefox)
- BeautifulSoup4
- Регулярные выражения
- CSV
- Pytest (покрытие >75%)

## Установка и запуск
1. Клонировать репозиторий
2. Создать виртуальное окружение: `python -m venv venv`
3. Активировать: `venv\Scripts\activate` (Windows)
4. Установить зависимости: `pip install -r requirements.txt`
5. Запустить парсер: `python main.py`
6. Результат появится в `data/products.csv`

## Тестирование
```bash
pytest --cov=scraper tests/
Пример полученных данных
Ссылка	Наименование	Цена	Рейтинг	Описание	Инструкция	Страна
https://goldapple.ru/...	Maison Francis Kurkdjian Gentle Fluidity Gold	22510	4.7	...	...	Франция
text

### 4. Залить на GitHub
- Создайте репозиторий на GitHub.
- Выполните в папке проекта:
  ```powershell
  git init
  git add .
  git commit -m "final version"
  git remote add origin https://github.com/ваш-username/название-репозитория.git
  git push -u origin main