import logging


class LogService:
    def __init__(self, log_file: str = "app.log"):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger(__name__)

    def info(self, msg: str, **kwargs):
        self.logger.info(f"{msg} | {kwargs}")

    def debug(self, msg: str, **kwargs):
        self.logger.debug(f"{msg} | {kwargs}")

    def error(self, msg: str, **kwargs):
        self.logger.error(f"{msg} | {kwargs}")

    def warning(self, msg: str, **kwargs):
        self.logger.warning(f"{msg} | {kwargs}")

    def critical(self, msg: str, **kwargs):
        self.logger.critical(f"{msg} | {kwargs}")


logger_service = LogService()
