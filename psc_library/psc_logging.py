# psc_logging.py

"""
Centralize logging stuff

@Author: Filipe Santos
"""

import logging

class log_class:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        #console_handler = logging.StreamHandler()
        #console_handler.setFormatter(formatter)
        #self.logger.addHandler(console_handler)

        self.logger.info("#"*60)
        self.logger.setLevel(logging.INFO)
        self.logger.info("Logging level set to INFO.")
        self.logger.setLevel(logging.DEBUG)

    def set_level(self, level):
        if level == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif level == "INFO":
            self.logger.setLevel(logging.INFO)
        
        self.logger.info(f"Logging level set to {level}.")

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)

logger = log_class("utilXRT.log")

"""
def logging_init():
    #logging.basicConfig(filename='utilXRT.log', format='%(asctime)s : %(levelname)-8s : %(message)s', level=logging.DEBUG)
    logging.basicConfig(filename='utilXRT.log', format='%(asctime)s : %(levelname)-8s : %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("#"*60)
    logger.info("Logging level set to INFO.")

def log_level_set(level):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.getLevelName(level))
    logger.info(f"Logging level set to {level}.")
"""