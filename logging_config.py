import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Create logs directory
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                os.path.join(log_dir, 'crab_ai.log'),
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
        ]
    )

    # Create and return application-specific logger
    return logging.getLogger("crab_ai")

# Global logger
logger = setup_logging()