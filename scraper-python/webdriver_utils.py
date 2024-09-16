from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions

def setup_chrome_options() -> ChromeOptions:
    """Configure Chrome options for headless scraping."""
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return options

def initialize_driver(options: ChromeOptions) -> webdriver.Chrome:
    """Initialize the Chrome driver with configured options."""
    service = Service()
    return webdriver.Chrome(service=service, options=options)