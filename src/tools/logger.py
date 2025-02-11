import logging

logger = logging.getLogger("AlmaLinux AutoDebranding Tool")

if not logger.hasHandlers():
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
