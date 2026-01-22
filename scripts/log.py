
import logging

def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s]: %(name)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
    )