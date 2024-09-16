import logging
import datetime
from pathlib import Path

import structlog
import yaml

from config import load_config
from scraper import OSDEScraper

# Configure logging
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

def main():
    config_file = 'scraper_config.yaml'
    config = load_config(config_file)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = Path(f'csv/osde_scraping_python_{timestamp}.csv')
    
    scraper = OSDEScraper(config)
    scraper.run_scraper(file_path, config['configurations'])

if __name__ == '__main__':
    main()