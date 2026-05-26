import inspect
import re


class dyn:
    def __init__(self,file:str)->None:
        self.file = file
        pattern = re.compile(r"\s*(\w*)\s*=")
        frame = inspect.currentframe().f_back           #type:ignore
        filename = frame.f_code.co_filename             #type:ignore
        lineno = frame.f_lineno                         #type:ignore
        print(filename,lineno)
        with open(filename,"r") as f:
            lines = f.readlines()
        targetline = lines[lineno-1]
        obj = re.match(pattern,targetline)
        if obj:
            objname= obj.group(1)                       #type:ignore
            funcname = f'info{objname}'
            def dynamic(msg):
                self.info(msg)
            frame.f_globals[funcname] = dynamic         #type:ignore
    def info(self,msg):
        print(f'[INFO]:{msg}')