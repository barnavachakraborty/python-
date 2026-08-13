import logging
import functools
import os
import inspect
from typing import Callable
import re
import inspect

def obj(funcname:str)->tuple:
    patternstr = re.compile(r"\s*(\w*)\w*")
    frame = inspect.currentframe().f_back.f_back      #type:ignore
    line = inspect.getframeinfo(frame).code_context[0]      #type:ignore      
    objname = patternstr.match(line)
    return (f"{funcname}{objname.group(1)}",frame)     #type:ignore

class loggingIn:
    def __init__(self, filename: str):
        base, ext = os.path.splitext(filename)
        if ext and ext != '.log':
            raise ValueError('extension mismatch')
        elif not ext:
            ext = '.log'
        self.filename = base + ext
        self.formats = {}
        self.messeges = []
        funcname,frame = obj('info')
        def dynamicinfo(msg):
            self.info(msg)
        frame.f_globals[funcname] = dynamicinfo
        

    def __call__(self, args:list):
        imageFile = args
        for i, image in enumerate(imageFile):
            if not os.path.exists(image):
                raise Exception('Image file{}: {} does not exist'.format(i, image))

        def decorator(originalFunction: Callable) -> Callable:
            def count(tag: str):
                try:
                    with open(self.filename, "r") as fp:
                        lines = fp.readlines()
                except FileNotFoundError:
                    return 0
                counter = 0
                for line in lines:
                    if tag in line:
                        counter += 1
                return counter

            @functools.wraps(originalFunction)
            def wrapper(*args, **kwargs):
                result = originalFunction(*args, **kwargs)
                filebase = os.path.splitext(os.path.basename(inspect.getfile(originalFunction)))[0]
                pyLogger = logging.getLogger(filebase)
                pyLogger.setLevel(logging.INFO)

                for image in imageFile:
                    tag = f"[Image: {os.path.basename(image)}, function: {originalFunction.__name__}]"
                    formatcount = count(tag)
                    self.formats[image] = tag + f"-{formatcount + 1}"
                    messege = '\n'.join(self.messeges)
                    formatter = logging.Formatter('%(asctime)s: %(name)s{}:\n%(message)s'.format(self.formats[image]))

                    if not pyLogger.handlers:
                        handler = logging.FileHandler(self.filename)
                        pyLogger.addHandler(handler)
                    pyLogger.handlers[0].setFormatter(formatter)
                    pyLogger.info(messege)

                self.messeges.clear()
                return result
            return wrapper
        return decorator

    def info(self, other:str):
        self.messeges.append(str(len(self.messeges) + 1) + '. ' + other)
        return self


# logger = loggingIn('postSegMerge.log')
# info = logger.info

# @logger('1_095.pgm', 'lena.pgm')
# def func():
#     info('Hello')
#     info('World')

# func()
