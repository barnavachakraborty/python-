import os
import sys 
import numpy as np
import numpy.typing as npt

class imgdata:
    def __init__(
        self,
        ip:str|None = None,
        newtags:list[str]|None = None,
        op:str|None = None,
        tester:str|None =None,
        pixels:npt.NDArray|None=None,
        height:int|None=None,
        width:int|None=None,
        maxval:int|None = None
        ):
        if ip is None :
            if (pixels is None or height is None or width is None or maxval is None):
                raise ValueError("No Value to process")
            self.__pixels = pixels
            self.__height = height
            self.__width = width
            self.__maxval = maxval
            self.__writeposs = False
            
        elif(ip is not None and pixels is None and height is None and width is None):
            self.__ip = ip
            self.valAgn()  
            if newtags or tester:
                self.addtags(ip,newtags,op,tester)
                self.uniquename()
            self.__writeposs = True
        elif pixels is None and (height is not None or width is not None or maxval is not None):
            raise Exception('No pixel to assign height or weight')    
        elif pixels is not None and (height is None or width is None or maxval is None):
             raise Exception("Pixel's height and width not given")
        elif ip is not None and newtags is None:
            raise Exception("Cant process ip without tags")
    def valAgn(self):
        if not os.path.exists(self.__ip):
            raise FileNotFoundError(f"{self.__ip} does not esist")
        else:
            self.__height,self.__width,self.__maxval = 0,0,0
            with open(self.__ip,"r") as f_ip:
                if f_ip.readline().strip() != 'P2':
                    raise Exception("Not a proper file...")
                pos = f_ip.tell()
                comment = f_ip.readline()
                if not comment.startswith('#'):
                    f_ip.seek(pos)                
                self.__width,self.__height = map(int,f_ip.readline().split())
                self.__maxval =int(f_ip.readline()) 
                data = list(map(int,f_ip.read().split()))
                self.__pixels = np.array(data,dtype=np.int32)
                if(self.__pixels.size != self.__height*self.__width):
                    raise ValueError("The pixel data does not match")  
        
    def addtags(self,ip,newtags,op,tester):
        if (not isinstance(newtags, list) 
            or not all(isinstance(t, str) for t in newtags)) and not (type(tester)==str):
            raise Exception("newtags must be a list of strings or tester must be provided")
        tester = f"@{tester}" if tester else ""

        path,filename = os.path.split(ip)
        print(path)
        base,ext = os.path.splitext(os.path.basename(filename))
        if not op:
            if '[' in base and ']' in base:
                start = base.index('[')
                end = base.index(']')
                name = base[:start]
                tags = base[start+1:end].split(',')
                for tag in newtags:
                    if tag not in tags:
                        tags.append(tag)
                self.__op = f"{path}/{name}[{','.join(tags)}]{ext}"
            else:
                self.__op = f"{path}/{base}[{','.join(newtags)}]{tester}{ext}"
        else:
            self.__op = f"{path}{base}{tester}{ext}"
       
    def uniquename(self):
        c = 0
        base,ext = os.path.splitext(self.__op)
        while True:
            if c == 0:
                candidate = f'{base}{ext}'
            else:
                candidate = f"{base}-{c}{ext}"
                
            if not os.path.exists(candidate):
                self.__op = candidate
                break
            c+=1
    @property
    def ip(self):
        if self.__writeposs:
            return self.__ip
        else:
            raise ValueError('No input file given')
    @property
    def op(self):
        if self.__writeposs:
            return self.__op
        else:
            raise ValueError('No input file given')
    @property
    def height(self):
        return self.__height
    @property
    def width(self):
        return self.__width
    @property
    def maxval(self):
        return self.__maxval
    @property
    def pixels(self):
        return self.__pixels
    
    @pixels.setter
    def pixels(self,newP:npt.NDArray[np.int32]):
        if newP.shape == self.__pixels.shape and newP.dtype == np.int32:
            self.__pixels = newP
        elif newP.shape != self.__pixels.shape:
            raise ValueError('Shape of the given image not equal to the one already there')
        elif newP.dtype != np.dtype(np.int32):
            raise ValueError('Datatype Mismatch')
        self.__pixels = newP
    @property
    def dataform(self)->"imgdata":
        return imgdata(
            pixels = self.pixels.copy(),
            height = self.height,
            width = self.width,
            maxval = self.maxval,
        )
    def __str__(self) -> str:
        return f"[ip: {self.ip}, op: {self.op}, height: {self.height}, \nwidth: {self.width}, maxval: {self.maxval}, pixels: {self.height*self.width}]"
    def writeOP(self, output:npt.NDArray)->None:
        if self.__writeposs :
            with open(self.op, "x") as f_op:
                print(f"{self.op} opened")

                f_op.write(f"P2\n{self.width} {self.height}\n{self.maxval}\n")

                for i in range(self.height):
                    for j in range(self.width):
                        f_op.write(f"{output[i*self.width + j]} ")
                    f_op.write("\n")
        else:
            raise ValueError("No ip")
    
