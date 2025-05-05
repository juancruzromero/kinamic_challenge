from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.robotparser
from functools import wraps
import requests
import json
import time
import random

# User agent list for simulating different browsers for scrapers:
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    # Add more user agents as needed...
]

class Helpers:
    """
    A class containing utility functions for web scraping,
    decorators, data handling and other stuff.
    """
    @staticmethod
    def request_url(url,
            proxies=None,
            max_retries=5,
            timeout=10
        ) -> requests.Response:
        """
        Makes a robust HTTP GET request with retry logic, random headers, and optional proxy support.

        This function is designed for web scraping at scale. It helps avoid detection and blocking
        by rotating the User-Agent header, introducing randomized delays, handling transient errors
        with exponential backoff retries, and supporting proxy usage.

        Args:
            url (str): The URL.
            proxies (str, optional): Proxy URL to route the request through. Defaults to None.
            max_retries (int, optional): Maximum number of retry attempts on failure. Defaults to 5.
            timeout (int, optional): Timeout for each request in seconds. Defaults to 10.

        Raises:
            Exception: If all retry attempts fail or a non-recoverable error occurs.

        Returns:
            requests.Response: The HTTP response object if the request is successful (status 200).
        """
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        proxy_config = {"http": proxies, "https": proxies} if proxies else None

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(url,
                    headers=headers,
                    proxies=proxy_config,
                    timeout=timeout
                )
                if response.status_code == 200:
                    return response
                elif 500 <= response.status_code < 600:
                    print(f"Server error {response.status_code} — retrying ({attempt}/{max_retries})...")
                else:
                    response.raise_for_status()
            except requests.RequestException as e:
                print(f"Attempt {attempt} failed: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff

        raise Exception(f"Failed to fetch {url} after {max_retries} attempts.")

    @staticmethod
    def is_url_allowed(url: str, user_agent: str = "*") -> bool:
        """
        Checks if a URL is allowed to be fetched according to the site's robots.txt rules.

        Args:
            url (str): The full URL to check.
            user_agent (str): The user agent to use when checking the rules (default is "*").

        Returns:
            bool: True if access is allowed, False otherwise.
        """
        print("-" * 50)
        print("Checking robots.txt for URL access...")
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)

        try:
            rp.read()
        except Exception as e:
            print(f"Could not read robots.txt: {e}")
            # If robots.txt is not accessible, assume not allowed
            return False

        if rp.can_fetch(user_agent, url):
            print(f"Access allowed for {user_agent} to {url}")
            print("-" * 50)
        else:
            raise Exception(f"Access denied for {user_agent} to {url}")

    @staticmethod
    def save_to_json(name_file: str, books_list_data: list) -> None:
        """
        Saves the list of book data to a JSON file.

        Args:
            name_file (str): Name of the output file.
            books_list (list): List of book dictionaries.
        """
        json_file_name = f"data/raw/{name_file}.json"
        with open(json_file_name, "w", encoding='utf-8') as file:
            json.dump(books_list_data, file, indent=4)

    @staticmethod
    def create_soup(html_text: str,
            parser: str = 'html.parser'
        ) -> BeautifulSoup:
        """
        Parses raw HTML text into a BeautifulSoup object.

        Args:
            html_text (str): The HTML content as a string.
            parser (str, optional): The parser to use. Defaults to 'html.parser'.

        Returns:
            BeautifulSoup: Parsed HTML soup object.
        """
        return BeautifulSoup(html_text, parser)

    @staticmethod
    def timer(func):
        """
        Decorator to measure the execution time
        of a function/scraper in minutes.

        Args:
            func (function): The function to wrap.

        Returns:
            function: Wrapped function with timing.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            duration_minutes = (end - start) / 60
            print(f"Scraper executed in {duration_minutes:.3f} minutes")
            return result
        return wrapper
    
