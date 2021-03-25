import logging
import inspect

logger = logging.getLogger('root')
FORMAT = "[%(asctime)s] %(levelname)s %(filename)s:%(lineno)s - %(funcName)s(): %(message)s"
logging.basicConfig(filename=r"logs/log.txt",
                    format=FORMAT,
                    datefmt='%H:%M:%S')
logger.setLevel(logging.DEBUG)