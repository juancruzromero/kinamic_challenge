# Python libraries:
import re
from typing import List, Dict
# My modules:
from utils.helpers import Helpers
from utils.logger import setup_logger
from config.config import load_config

class BooksScraper:
    """ Main class for scraping books data from 'books.toscrape.com'."""
    def __init__(self):
        config = load_config()
        self.logger = setup_logger(__name__)
        self.base_url = config['books_to_scrape']
        Helpers.is_url_allowed(self.base_url) # Check robots.txt

    @Helpers.timer
    def run_scraper(self) -> None:
        """ Main method to run the scraper. """
        self.logger.info("Starting process...")
        print("-" * 50)

        try:
            books_data_list = []

            response = Helpers.request_url(self.base_url)
            links = self.get_links(response)

            total_books = 0
            for category, url in links.items():
                data = self.get_results(category, url)
                books_data_list.extend(data)
                total_books += len(data)

            print(f"\nTotal books scraped: {total_books}\n")
            Helpers.save_to_json("books", books_data_list)

            self.logger.info("Scraping completed successfully.")
            print("-" * 50)

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            self.logger.exception("An error occurred during scraping.")
            print(f"An error occurred: {e}")

    def get_links(self, response) -> Dict[str, str]:
        """
        Extracts book category links from the main page.

        Args:
            response: Response object.

        Returns:
            dict: Dictionary where keys are category names and values are URLs.
        """
        soup = Helpers.create_soup(response.text)
        categories = {}
        
        # Itarete over the <ul> and <li> tags to get the links.
        # The first two and last elements are not categories
        # and are removed from the list
        links_list = [li.get('href') for li in soup.select('ul li a')][2:-1]

        for link in links_list:
            url = self.base_url + link
            category = url.split('/')[-2].split('_')[0].capitalize()
            clean_category = category.replace('-', ' ')
            categories[clean_category] = url

        return categories

    def get_data(self, category: str, text: str) -> List[Dict[str, str]]:
        """
        Extracts book data (title, price, rating) from a category page.
        
        Args:
            category (str): Name of the category.
            text (str): HTML content of the category page.

        Returns:
            list: List of book data dictionaries.
        """
        soup = Helpers.create_soup(text)
        # Find all book data from <article> tags:
        articles = soup.find_all('article')

        books = []
        for book in articles:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text.replace('Â', '')
            rating = book.p['class'][1]
            # TODO: Get image URL and stock:
            # image = self.base_url + book.img['src']
            # stock = book.find('p', class_='instock availability').text.strip()
            books.append({
                'title': title,
                'category': category,
                'price': price,
                'rating': rating
            })

        return books
    
    def get_results(self, category: str, url: str) -> List[Dict[str, str]]:
        """
        Iterates over all pages of a category and collects book data.

        Args:
            category (str): Name of the category.
            url (str): URL of the first category page.

        Returns:
            list: Aggregated list of book data dictionaries.
        """
        print(f"Scraping category: {category}")
        results = []

        while url:            
            response = Helpers.request_url(url)
            data = self.get_data(category, response.text)
            results.extend(data)

            next_button = Helpers.create_soup(response.text).find('li', class_='next')
            if next_button:
                next_page = next_button.a['href']
                url = re.sub(r'[^/]+(?=\.html$)', next_page.split('.')[0] , url)
            else:
                url = None
        print("-" * 50)
        return results