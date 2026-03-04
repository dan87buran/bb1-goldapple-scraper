from curl_cffi import requests
import json

class ApiCategoryParser:
    def __init__(self):
        self.base_url = 'https://goldapple.ru/front/api/catalog/cards-list?locale=ru'
        # Минимальные заголовки, остальное эмулируется
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36',
        }
        self.product_links = []

    def get_product_links(self, category_id=1000000007, page_size=24):
        page = 1
        while True:
            payload = {
                "categoryId": category_id,
                "pageNumber": page,
                "pageSize": page_size,
                "filters": [],
                "mode": "dynamic",
                "cityId": "5bf5ddff-6353-4a3d-80c4-6fb27f00c6c1",
                "cityDistrict": None,
                "geoPolygons": [
                    "EKB-000000449",
                    "EKB-000000403",
                    "EKB-000000584",
                    "EKB-000001281",
                    "EKB-000001403",
                    "EKB-000000404"
                ],
                "regionId": "b756fe6b-bbd3-44d5-9302-5bfcc740f46e"
            }

            print(f"Загрузка страницы {page}...")
            try:
                response = requests.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload,
                    impersonate="chrome124"  # эмуляция Chrome 124
                )
            except Exception as e:
                print(f"Ошибка запроса: {e}")
                break

            if response.status_code != 200:
                print(f"Ошибка {response.status_code}: {response.text}")
                break

            data = response.json()
            if not data.get('data') or not data['data'].get('cards'):
                break

            found = 0
            for card in data['data']['cards']:
                if card.get('cardType') == 'product':
                    product = card.get('product', {})
                    url_path = product.get('url')
                    if url_path:
                        full_url = 'https://goldapple.ru' + url_path
                        if full_url not in self.product_links:
                            self.product_links.append(full_url)
                            found += 1
            print(f"Страница {page}: добавлено {found} ссылок. Всего: {len(self.product_links)}")

            pagination = data['data'].get('pagination', {})
            if not pagination.get('nextPage'):
                break

            page += 1
            import time
            time.sleep(1)  # небольшая задержка между страницами

        return self.product_links