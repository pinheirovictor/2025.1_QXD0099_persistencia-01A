import logging

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
