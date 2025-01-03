import logging
import os


class Logger:
    """
    A singleton logger class that provides both console and file logging capabilities.

    This class implements the singleton pattern to ensure only one logger instance exists
    per name. It provides both console and file logging with different logging levels:
    - Console handler: INFO level
    - File handler: DEBUG level

    The log files are stored in a 'logs' directory with the name 'scraper.log'.
    """
    _instance = None

    def __new__(cls, name):
        """
        Create or return the singleton instance of the Logger class.

        This method implements the singleton pattern, ensuring only one Logger
        instance exists per name.

        Args:
            name (str): The name for the logger instance.

        Returns:
            Logger: The singleton instance of the Logger class.
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger(name)
        return cls._instance

    def _initialize_logger(self, name):
        """
        Initialize the logger with console and file handlers.

        Sets up both console and file handlers with appropriate log levels and formatters.
        Creates a 'logs' directory if it doesn't exist and configures the log file.

        Args:
            name (str): The name for the logger instance.

        Note:
            Console handler is set to INFO level
            File handler is set to DEBUG level
            Log format: '%(asctime)s - %(levelname)8s - %(message)s'
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Set root logger to DEBUG

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)8s - %(message)s')

        # Create console handler
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)  # Set console handler to INFO
        self.console_handler.setFormatter(formatter)
        self.logger.addHandler(self.console_handler)

        # Create file handler
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, "scraper.log")
        self.file_handler = logging.FileHandler(log_file, mode='w')
        self.file_handler.setLevel(logging.DEBUG)  # Set file handler to DEBUG
        self.file_handler.setFormatter(formatter)
        self.logger.addHandler(self.file_handler)
    # def __init__(self, name):
    #     """
    #     Initialize the logger with console and file handlers.
    #
    #     Args:
    #         name (str): The name of the logger instance.
    #     """
    #     self.logger = logging.getLogger(name)
    #     self.logger.setLevel(logging.DEBUG)  # Set root logger to DEBUG
    #     os.makedirs('logs', exist_ok=True)
    #     log_file = f"logs{os.sep}scraper.log"
    #
    #     # Create log formatter
    #     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #
    #     # Create console handler
    #     ch = logging.StreamHandler()
    #     ch.setLevel(logging.INFO)  # Set console handler to INFO
    #     ch.setFormatter(formatter)
    #     self.logger.addHandler(ch)
    #
    #     # Create file handler
    #     log_dir = os.path.dirname(log_file)
    #     if log_dir and not os.path.exists(log_dir):
    #         os.makedirs(log_dir)
    #     fh = logging.FileHandler(log_file, mode='w')
    #     fh.setLevel(logging.DEBUG)
    #     fh.setFormatter(formatter)
    #     self.logger.addHandler(fh)


    def debug(self, message):
        """
        Log a debug message.

        Args:
            message (str): The debug message to be logged.
        """
        self.logger.debug(message)

    def info(self, message):
        """
        Log an info message.

        Args:
            message (str): The info message to be logged.
        """
        self.logger.info(message)

    def warning(self, message):
        """
        Log a warning message.

        Args:
            message (str): The warning message to be logged.
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Log an error message.

        Args:
            message (str): The error message to be logged.
        """
        self.logger.error(message)

    def critical(self, message):
        """
        Log a critical message.

        Args:
            message (str): The critical message to be logged.
        """
        self.logger.critical(message)
