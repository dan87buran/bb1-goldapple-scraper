from scraper.utils import get_driver
from scraper.scraper import GoldAppleScraper

def main():
    driver = get_driver(headless=False)  # пока headless=False для отладки
    try:
        scraper = GoldAppleScraper(driver)
        scraper.run()
    finally:
        driver.quit()

if __name__ == '__main__':
    main()