#! /usr/bin/python3

import os, socket, re

files = {}

def checkDictionary(filename):
    if filename in files: return True
    files[filename] = 1
    return True
    
def addNewFile(data):
    print(data)
    payload = re.split(':', data)
    print(payload)
    #filename = payload[0]
    #content = payload[1:]
    #print(content)
    #checkDictionary(filename)
    
    #file = open(filename, 'w')

    #for data in content:
        #file.write(data)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 50001))
serverSocket.listen(1)

connection, Address = serverSocket.accept()

while True:
    data = connection.recv(1024).decode()
    if not data: break
    print(data)
    addNewFile(data)
connection.close()
    
    
