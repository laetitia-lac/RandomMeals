import logging

# create logger
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)
logger = logging.getLogger('random_meals_logger')
logger.propagate = False

# create file handler
file_handler = logging.FileHandler('logs/random_meals.log')
file_handler.setLevel(logging.DEBUG)

# create formatter and add it to file handler
log_formatter = logging.Formatter(log_format)
file_handler.setFormatter(log_formatter)

# add file handler to the logger
logger.addHandler(file_handler)