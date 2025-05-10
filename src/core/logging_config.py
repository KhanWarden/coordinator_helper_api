import logging
import sys

LOG_FORMAT = (
    "[%(asctime)s] [%(levelname)s] "
    "[%(name)s:%(filename)s:%(lineno)d] - %(message)s"
)

logging.basicConfig(
    level=logging.WARNING,
    format=LOG_FORMAT,
    stream=sys.stdout,
)
