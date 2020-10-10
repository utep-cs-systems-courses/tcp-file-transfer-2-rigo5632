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
serverSocket.listen(5)

while True:
    connection, address = serverSocket.accept()
    framedSend(connection, key.encode(), False)
    filename = ''
    content = ''

    if not os.fork():
        while True:
            data = framedReceive(connection, False).decode()
            if not data:
                try:
                    if filename not in files: 
                        fileSource = './files/' + filename
                        os.remove(fileSource)
                        print('Deleting File: %s' %filename)
                except:
                    print('No filename')
                break
            if proxy: data = data.decode()
            if data == 'exit': break

            payload = re.split(':', data)
            if len(payload) == 1:
                key = payload[0]
                files[filename] = -1
                filename = None
                content = None
                framedSend(connection, key.encode(), False)
                print('Sending File Key...')
            else:
                key = payload[0]
                filename = payload[1]
                content = payload[2]

            if filename not in files and filename is not None:
                fileDestination = './files/' + filename
                file = open(fileDestination, 'a')

                print('Writing to %s' %filename)

                file.write(content)
                file.close()
            else:
                if filename:
                    print('%s found in server' %filename)
                    print('Not writing data...')
        connection.close()
