import time
import random
import structlog
from typing import Dict, List, Optional
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from tenacity import retry, stop_after_attempt, wait_exponential

from webdriver_utils import setup_chrome_options, initialize_driver
from data_processor import process_results
from csv_utils import create_csv, save_to_csv

logger = structlog.get_logger()

class OSDEScraper:
    def __init__(self, config: Dict):
        self.url = config['url']
        self.driver: Optional[WebDriver] = None
        self.options = setup_chrome_options()
        self.config_index = 0
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def open_site(self) -> None:
        """Navigate to the target website with retry logic."""
        logger.info("Navigating to site", url=self.url)
        self.driver.get(self.url)
        time.sleep(20)  # Allow time for the page to load completely

    def accept_cookies(self) -> None:
        """Accept cookies if the prompt is present."""
        try:
            cookie_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler'))
            )
            cookie_button.click()
            logger.info("Accepted cookies")
        except TimeoutException:
            logger.info("No cookie acceptance button found")

    def close_overlay(self):
        """Attempt to close any overlay that might be present."""
        try:
            overlay = self.driver.find_element(By.CSS_SELECTOR, ".ui-widget-overlay")
            if overlay.is_displayed():
                close_button = self.driver.find_element(By.CSS_SELECTOR, ".ui-dialog-titlebar-close")
                close_button.click()
                time.sleep(1)
        except:
            pass

    def click_element_safely(self, element):
        """Try to click an element, first normally, then with JavaScript if that fails."""
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def select_dropdown_option(self, dropdown_selector: str, option_selector: str, option_text: str) -> bool:
        """
        Select an option from a dropdown menu. Return False if option not found.
        """
        try:
            self.close_overlay()
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_selector))
            )
            self.click_element_safely(dropdown)
            time.sleep(2)

            options = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, option_selector))
            )

            for option in options:
                if option.text.strip() == option_text:
                    self.click_element_safely(option)
                    return True

            logger.error("Option not found", option_text=option_text)
            return False
        except TimeoutException:
            logger.error("Failed to select option", option_text=option_text)
            return False

    def select_plan(self, plan: str) -> bool:
        """Select the plan from the dropdown."""
        return self.select_dropdown_option('#labelSelectorPlan', '#ulplan li', plan)

    def select_location(self, provincia: str, localidad: str) -> bool:
        """Select the province and location."""
        if not self.select_dropdown_option('#labelSelectorProvincia', '#ulprovincia li', provincia):
            return False
        time.sleep(2)
        return self.select_dropdown_option('#labelSelectorLocalidad', '#ullocalidad li', localidad)
    
    def select_specialty(self, specialty_name: str) -> bool:
        """Select the specialty by exact name using the search field."""
        try:
            specialty_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#especialidadSelected'))
            )
            self.click_element_safely(specialty_dropdown)
            time.sleep(2)

            search_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "filtroespecialidad"))
            )
            search_field.clear()
            search_field.send_keys(specialty_name)
            
            time.sleep(2)  # Wait for search results to update

            visible_specialties = self.driver.execute_script("""
                return Array.from(document.querySelectorAll('#ulespecialidad li'))
                    .filter(item => item.offsetParent !== null)
                    .map(item => ({text: item.innerText.trim(), element: item}));
            """)

            for specialty in visible_specialties:
                if specialty['text'].strip().lower() == specialty_name.lower():
                    logger.info("Found exact match for specialty", specialty=specialty['text'])
                    self.click_element_safely(specialty['element'])
                    return True

            logger.error("Exact specialty not found in search results", specialty_name=specialty_name)
            return False
        except Exception as e:
            logger.error("Error selecting specialty", specialty_name=specialty_name, error=str(e))
            return False

    def search(self) -> None:
        """Click the search button and wait for results to load."""
        try:
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#botonBuscar'))
            )
            self.click_element_safely(search_button)
            
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#listadoResultado'))
            )
            time.sleep(5)  # Ensure all elements have loaded
        except Exception as e:
            logger.error("Error clicking search button", error=str(e))

    def load_all_results(self) -> None:
        """Load all results by clicking the 'Load more' button until it's no longer available."""
        while True:
            try:
                load_more_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "verMas"))
                )
                if load_more_button.is_displayed() and load_more_button.is_enabled():
                    self.click_element_safely(load_more_button)
                    time.sleep(2)
                else:
                    logger.info("No more results to load")
                    break
            except TimeoutException:
                logger.info("No more results to load (TimeoutException)")
                break
            except Exception as e:
                logger.error(f"Error loading more results: {str(e)}")
                break

        # Ensure all results are loaded
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.ID, "verMas"))
            )
        except TimeoutException:
            logger.warning("'Ver más' button did not disappear as expected")

    def get_results(self) -> str:
        """
        Get the search results.
        
        Returns:
            str: HTML string of results
        """
        try:
            # Wait for the results to be present
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#listadoTabla'))
            )
            
            # Get the entire table of results
            results_table = self.driver.find_element(By.CSS_SELECTOR, '#listadoTabla')
            html_string = results_table.get_attribute('outerHTML')
            
            logger.info("Retrieved search results", html_length=len(html_string))
            
            return html_string
        except Exception as e:
            logger.error("Failed to get results", error=str(e))
            return ""

    def run_scraper(self, file_path: Path, configurations: List[Dict[str, str]]) -> None:
        """
        Run the scraper for the given configurations.
        """
        create_csv(file_path)
        self.driver = initialize_driver(self.options)
        self.open_site()
        self.accept_cookies()

        for config in configurations:
            self.config_index += 1
            logger.info("Processing configuration", config_index=self.config_index, config=config)
            try:
                self.close_overlay()
                if not self.select_plan(config['plan']):
                    logger.warning("Skipping configuration due to plan selection failure", config_index=self.config_index, config=config)
                    continue
                if not self.select_location(config['provincia'], config['localidad']):
                    logger.warning("Skipping configuration due to location selection failure", config_index=self.config_index, config=config)
                    continue
                if not self.select_specialty(config['especialidad']):
                    logger.warning("Skipping configuration due to specialty selection failure", config_index=self.config_index, config=config)
                    continue
                
                self.search()
                self.load_all_results()
                html_string = self.get_results()
                if html_string:
                    results = process_results(html_string, config['plan'], config['provincia'], config['localidad'], config['especialidad'], self.config_index)
                    if results:
                        save_to_csv(file_path, results)
                    else:
                        logger.warning("No results found for configuration", config_index=self.config_index, config=config)
                else:
                    logger.error("Failed to get results for configuration", config_index=self.config_index, config=config)
            except Exception as e:
                logger.error("Error processing configuration", config_index=self.config_index, config=config, error=str(e))
            finally:
                time.sleep(random.uniform(3, 5))  # Random delay between searches
        
        self.driver.quit()