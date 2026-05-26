# import logging
# class decoratorClass(object):
#     def __init__(self,function):
#         self.function = function
#         logging.basicConfig(
#             format='%(levelname)s:%(message)s',
#             filename=f'{function.__name__}.log',
#             level=logging.INFO            
#         )
                
#     def __call__(self,*args, **kwargs):
#         logging.info(f'Ran with args: {args}, kwargs: {kwargs}')
#         return self.function(*args,**kwargs)
    
    
# @decoratorClass
# def add(a,b):
#     logging.info(f'ADD: {a} + {b} = {a+b}')
#     return a+b

# add(4,5)
# def my_logger(originalFunction):
#     import logging
#     logging.basicConfig(
#         format='%(levelname)s:%(message)s',
#         filename=f'{originalFunction.__name__}.log',
#         level=logging.INFO            
#     )
    
#     def wrapper(*args,**kwargs):
#         logging.info(f'Ran with args: {args}, and kwargs: {kwargs}')
#         return originalFunction(*args,**kwargs)
#     return wrapper

# @my_logger
# def display():
#     print('Display function ran')


# @my_logger
# def display_info(name:str,age:int):
#     print(f'Name: {name}, Age: {age}')
    
# display()
# display_info('Barnava Kumar Chakraborty',20)

from functools import wraps

def mytimer(original_func):
    
    import time
    
    @wraps(original_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = original_func(*args,*kwargs)
        t2 = time.time()-t1
        print(f"{original_func.__name__} function ran for {t2} seconds giving a result {result}")
        return result
    return wrapper

def my_logger(original_func):
    import logging
    logging.basicConfig(
        format = '%(levelname)s:%(name)s:%(message)s',
        filename= f'{original_func.__name__}.log',
        level= logging.INFO
    )
    @wraps(original_func)
    def wrapper(*args,**kwargs):
        logging.info(f'Ran with args: {args} and kwargs: {kwargs}')
        return original_func(*args,**kwargs)
    return wrapper

import time

@my_logger
@mytimer
def display_info(name,age):
    time.sleep(1)
    print(f'display_info ran with arguments({name},{age})')
    
display_info('Tom',22)
    
 
   