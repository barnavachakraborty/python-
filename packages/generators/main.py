
import time
from functools import wraps
from logger import NewLogger

def my_logger(original_func):
    import logging
    @wraps(original_func)
    def wrapper(*args,**kwargs):
        logkeeper = NewLogger(
            __name__,
            f'{original_func.__name__}.log',
            level=logging.INFO,
            formatter='%(levelname)s:%(name)s,%(message)s',
        )
    return wrapper

