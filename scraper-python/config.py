import yaml
import structlog

logger = structlog.get_logger()

def load_config(config_file: str) -> dict:
    """
    Load configuration from a YAML file using UTF-8 encoding.

    Args:
        config_file (str): Path to the YAML configuration file.

    Returns:
        Dict: Configuration dictionary.
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except UnicodeDecodeError:
        logger.error("Failed to decode config file with UTF-8 encoding. Trying with ISO-8859-1.")
        with open(config_file, 'r', encoding='iso-8859-1') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load configuration file: {str(e)}")
        raise