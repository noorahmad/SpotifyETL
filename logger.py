import logging
import inspect

logger = logging.getLogger('root')
FORMAT = "[%(asctime)s] %(filename)s:%(lineno)s - %(funcName)20s(): %(message)s"
logging.basicConfig(filename=r"logs/log.txt",
                    format=FORMAT,
                    datefmt='%H:%M:%S')
logger.setLevel(logging.DEBUG)