from random import *
filename='lotteworld.jpg'
filenamesplit = filename.split('.')

i = randint(1, 1000000)
c_filename = f'{filenamesplit[0]}_{i}.{filenamesplit[1]}'
print(c_filename)

