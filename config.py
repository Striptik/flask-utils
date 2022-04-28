import logging
import os

from dotenv import load_dotenv

load_dotenv()

LOGS_DISABLED = os.getenv("DISABLE_LOGS") == "true"

IS_LOCAL = os.getenv("ENVIRONMENT", "dev") == 'local'

logging.basicConfig(
    filename=os.getenv("SERVICE_LOG", "server.log"),
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s \
        pid:%(process)s module:%(module)s %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
)
