from pathlib import Path
import yaml
from sync.log.loggers import logger


def load_config():
        configfile_path = Path("./configs/config.yaml")
        # configfile_path = Path(__file__).resolve().parents[2]  / "configs"/"config.yaml"
        try:
            with open(configfile_path, "r") as file:
                logger.info("File opened successfully!")
                config = yaml.safe_load(file)
        except Exception as e:
                logger.info(f"Error opening file: {e}")
        return config
    

    
