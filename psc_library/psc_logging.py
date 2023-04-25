# psc_logging.py

"""
Centralize logging stuff

@Author: Filipe Santos
"""

import logging
from psc_library.psc_txt_msgs import psc_msg

logging.basicConfig(filename='utilXRT.log', format='%(asctime)s : %(levelname)-8s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("#"*60)
logger.info(psc_msg("version1"))
logger.info(psc_msg("version2"))
logger.info("Logging level set to INFO.")
