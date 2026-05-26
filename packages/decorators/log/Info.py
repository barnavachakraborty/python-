import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('Employee.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Info:
    def __init__(self,first:str,last:str,instance:str):
        self.first = first
        self.last = last
        self.instance = instance
        logger.info('Information of {}: Name - {}; Email - {}'.format(self.instance,self.fullname,self.email))
        
    @property
    def fullname(self):
        return '{} {}'.format(self.first,self.last)
    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first,self.last)
        
engineer = Info("Barnava","Chakraborty","engineer")
driver = Info("Ramesh","Gotti","deiver")
doctor = Info("Debojyoti","Chakraborty","doctor")
plumber = Info("Purushottom","Seal","plumber")
        