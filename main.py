from scrapers.books_scraper import BooksScraper
from etls.books_etl import run_etl

if __name__ == "__main__":
    scraper = BooksScraper()
    # Execute the scraper
    scraper.run_scraper()
    # Execute the ETL process:
    run_etl()