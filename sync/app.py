from restapi_server import app
from log.loggers import logger

if __name__ == "__main__": 
    logger.info("flask starting")
    app.run(debug=True, host='0.0.0.0', port=5000)
    