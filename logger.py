import logging
import inspect
"""
TODO: extended logging e.g. info vs error
      add severity
"""

logger = logging.getLogger('root')
FORMAT = "[%(asctime)s] %(levelname)s %(filename)s:%(lineno)s - %(funcName)s(): %(message)s"
logging.basicConfig(filename=r"logs/log.txt",
                    format=FORMAT,
                    datefmt='%H:%M:%S')
logger.setLevel(logging.DEBUG)