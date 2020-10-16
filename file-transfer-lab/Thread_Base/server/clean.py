#! /usr/bin/python3
import os

path = './Files/'
fileDirectory = os.listdir(path)
originFile = path + 'README.md'

for i in range(len(fileDirectory)):
    file = path + fileDirectory[i]
    if file != originFile:
        os.remove(file)
        print('Removing %s' %file)

fileDirectory = os.listdir(path)

if path+fileDirectory[0] == originFile and len(fileDirectory) == 1:
    print('success')
else:
    print('failed')


