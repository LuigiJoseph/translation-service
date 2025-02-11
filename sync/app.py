from restapi_server import app,api
from log.loggers import logger

# logger = get_logger(__name__)



if __name__ == "__main__": 
    logger.info("Starting flask")
    app.run(debug=True, host='0.0.0.0', port=5000)