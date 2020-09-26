#! /usr/bin/python3
import os, socket, re, sys
sys.path.append('../../lib')
import params
sys.path.append('../../framed-echo')
from framedSock import framedReceive, framedSend


switchesVarDefaults = (
    (('-l', '--listentPort'), 'listenPort', 50001),
    (('-p', '--proxy'), 'proxy', False),
    (('-?', '--usage'), 'usage', False)
)

paramMap = params.parseParams(switchesVarDefaults)
listenPort, proxy, usage = paramMap['listenPort'], paramMap['proxy'], paramMap['usage']

if usage:
    params.usage()

files = {}
key = '0'
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', listenPort))
serverSocket.listen(1)

connection, address = serverSocket.accept()
connection.send(key.encode()) if not proxy else framedSend(connection, key.encode(), False)
filename = ''
content = ''
while True:
    data = connection.recv(1024).decode() if not proxy else framedReceive(connection, False)
    if not data:
        if filename not in files: 
            fileSource = './files/' + filename
            os.remove(fileSource)
            print('Deleting File: %s' %filename)
        break
    if proxy: data = data.decode()
    if data == 'exit': break

    payload = re.split(':', data)
    if len(payload) == 1:
        key = payload[0]
        files[filename] = -1
        filename = None
        content = None
        connection.send(key.encode()) if not proxy else framedSend(connection, key.encode(), False)
        print('Sending File Key...')
    else:
        print(payload)
        key = payload[0]
        filename = payload[1]
        content = payload[2]

    if filename not in files and filename is not None:
        fileDestination = './files/' + filename
        file = open(fileDestination, 'a')

        print('Writing to file %s' %filename)

        file.write(content)
        file.close()
    else:
        if filename:
            print('%s found in server' %filename)

connection.close()