import logging
import sys

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  
        logging.FileHandler("black-channel.log")      
    ]
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

