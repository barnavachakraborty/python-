import logging


class NewLogger:
    def __init__(
        self,
        loggername:str,
        filename:str,
        handlerLevel:logging._Level|None=None,
        formatter:str|None=None,
        level:int = logging.ERROR,
    ) -> None:
        self.__logger = logging.getLogger(loggername)
        self.__level = level
        self.__logger.setLevel(level)
        self.__formatter = logging.Formatter(formatter)
        self.__fileHandler = logging.FileHandler(filename)
        if self.__formatter != None:
            self.__fileHandler.setFormatter(self.__formatter)      
        self.__logger.addHandler(self.__fileHandler)
    @property
    def logger(self):
        return self.__logger  
    def log(self,messege:str):
        self.logger.log(self.__level,messege)


            