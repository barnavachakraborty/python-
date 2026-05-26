# from classdefinition import dyn
# import inspect

# hello = dyn('hello.log')
# infohello("hello")  #type:ignore

# world = dyn('world.log')
# infoworld("world")  #type:ignore

# frame = inspect.currentframe()
# print(frame.f_back) #type:ignore

text_to_search = r'''
abcdefghijklmnopqurtuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890

Ha HaHa

MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \ | ( )

coreyms.com

321-555-4321
123.555.1234
123*555*1234
800-555-1234
900-555-1234

Mr. Schafer
Mr Smith
Ms Davis
Mrs. Robinson
Mr. T
'''
import re

# pattern = re.compile(r"[^a-zA-Z\s]")
# matches = pattern.finditer(text_to_search)
# for match in matches:
#     print(match)
# pattern = re.compile(r'\d{3}.\d{3}.\d{3}')


# with open("sample.txt","r") as f:
#     contents = f.read()
#     matches = pattern.finditer(contents)
# for match in matches:
#     print(match)


urls = '''
https://www.google.com
http://coreyms.com
https://youtube.com
https://www.nasa.gov
'''
# pattern = re.compile(r'https?://(www\.)?(\w+)(\.\w+)')
# matches = pattern.finditer(urls)
# for match in matches:
#     print(match.group(2))

# import inspect

# def test():
#     """using inspect the very first time"""
#     frame = inspect.currentframe()
#     for name,val in inspect.getmembers(frame):
#         print(name," ",val)
# print(inspect.getdoc(test))
# inspectmodule = inspect.getmembers(inspect)
# for key,val in list(inspectmodule):
#     print(f"{key}: {val}")

from classdefinition import dyn

s1 = dyn('log.log')
infos1('Hello')