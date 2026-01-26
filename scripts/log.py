
import logging


def setup_logger():
    logging.basicConfig(
        level=logging.ERROR,
        format='[%(levelname)s]: %(name)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
    )
