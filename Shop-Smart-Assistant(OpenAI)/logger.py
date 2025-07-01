import logging
from logging.handlers import RotatingFileHandler


def setup_logger(name, log_file="\app.log", level=logging.INFO):
    """
    Configure and return a logger with file and console handlers.
    
    Args:
        name (str): Name of the logger (typically __name__ of the calling module).
        log_file (str): Path to the log file.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
    
    Returns:
        logging.Logger: Configured logger instance.
    """

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding handlers if logger is already configure
    if logger.handlers:
        return logger
    
    # Create formatters
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler with rotation
    try:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Failed to configure file handler for logging: {e}")
        # Fallback to console-only logging
        logger.warning(f"File handler setup failed: {e}. Using console logging only")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info(f"Logger '{name}' configure with file handler ({log_file}) and console handler")
    return logger
