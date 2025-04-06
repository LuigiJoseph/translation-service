from python_services.sync.restapi_server import app
from python_services.sync.log.loggers import logger

if __name__ == "__main__": 
    logger.info("flask starting")
    app.run(host='0.0.0.0', port=5000)
    