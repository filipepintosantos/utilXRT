# psc_logging.py

"""
Centralize logging stuff

@Author: Filipe Santos
"""

import logging

logging.basicConfig(filename='utilXRT.log', format='%(asctime)s : %(levelname)-8s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("#"*60)
logger.info("Logging level set to INFO.")
