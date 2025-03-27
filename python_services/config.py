from pathlib import Path
import yaml
import os

from python_services.sync.log.loggers import logger


def load_config():
        config_file = os.getenv("config_file", None)     
        if config_file:
                configfile_path = Path(config_file)
        else:
                configfile_path = Path(__file__).parent.parent / "configs/config.yaml"
 

        try:
            with open(configfile_path, "r") as file:
                logger.info("File opened successfully!")
                config = yaml.safe_load(file)
        except Exception as e:
                logger.info(f"Error opening file: {e}")
        return config
    

    
