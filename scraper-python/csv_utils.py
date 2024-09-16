import csv
from pathlib import Path
from typing import List, Dict
import structlog

logger = structlog.get_logger()

def create_csv(file_path: Path) -> None:
    """Create a CSV file with the necessary columns if it doesn't exist."""
    if not file_path.exists():
        with file_path.open('w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['config_index', 'indice', 'plan', 'provincia', 'localidad', 'especialidad', 'nombre', 'direccion', 'localidad_prestador', 'telefono', 'consultorio_digital', 'scraping_date'])

def save_to_csv(file_path: Path, results: List[Dict[str, str]]) -> None:
    """
    Append the results to a CSV file.
    """
    logger.debug("Attempting to append results to CSV", file_path=str(file_path), result_count=len(results))
    try:
        file_exists = file_path.exists()
        with file_path.open('a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['config_index', 'indice', 'plan', 'provincia', 'localidad', 'especialidad', 'nombre', 'direccion', 'localidad_prestador', 'telefono', 'consultorio_digital', 'scraping_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(results)
            logger.info("Successfully appended results to CSV", file_path=str(file_path), result_count=len(results))
    except Exception as e:
        logger.error("Error appending to CSV", error=str(e))
        if results:
            logger.debug("First result", result=results[0])
        else:
            logger.debug("No results to show")