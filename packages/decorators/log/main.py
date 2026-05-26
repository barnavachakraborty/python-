import logging
# import Info
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('sample.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.ERROR)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

logger.error('New Output')

num1 = 10
num2 = 0

logger.debug('ADD:\n{} + {} = {}'.format(num1,num2,num1 + num2))

logger.debug('SUB:\n{} - {} = {}'.format(num1,num2,num1 - num2))

logger.debug('MUL:\n{} * {} = {}'.format(num1,num2,num1 * num2))

def div(num1,num2):
    try:
        div = num1/num2
    except ZeroDivisionError:
        logger.exception('Tried to Divide by Zero')
    else:
        return div

logger.debug('DIV:\n{} / {} = {}'.format(num1,num2,div(num1,num2)))




