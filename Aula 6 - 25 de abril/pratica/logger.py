



import logging

logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime) - %(lelename)s - %(messages)s",
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)