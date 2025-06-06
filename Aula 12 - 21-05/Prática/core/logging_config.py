import logging

def setup_logging():
    logging.basicConfig(
        filename="marketplace.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )
