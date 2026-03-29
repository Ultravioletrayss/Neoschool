from utils import *



root_path='C:Users/ultra/Desktop/data/fishing/'
file_name='3ways.html_121816046000.txt'

l=file_opener(root_path,file_name)
print(l)
print("l的type为",type(l))

Redux=word_freq_redux(l)





