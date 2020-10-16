#! /usr/bin/python3

import os, socket, re, sys
sys.path.append('../lib')
import params
from framedSock import framedReceive, framedSend

# params
switchesVarDefaults = (
    (('-l', '--listentPort'), 'listenPort', 50001),
    (('-p', '--proxy'), 'proxy', False),
    (('-?', '--usage'), 'usage', False)
)

paramMap = params.parseParams(switchesVarDefaults)
listenPort, proxy, usage = paramMap['listenPort'], paramMap['proxy'], paramMap['usage']


# usage of params
if usage:
    params.usage()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', listenPort))
serverSocket.listen(5)

key = '-1'
while True:
    key = str(int(key) + 1)
    connection, address = serverSocket.accept()
    framedSend(connection, key.encode(), False)
    filename = ''
    content = ''

    if not os.fork():
        files = os.listdir('./Files')
        while True:
            data = framedReceive(connection, False)
            if not data: # file did not finsih writing to server
                if filename not in files and filename != None:
                    fileSource = './Files/' + filename
                    os.remove(fileSource)
                    print('Deleting File: %s' %filename)
                break
            data = data.decode()

            # unpack data from client
            payload = re.split(':', data)
            serverFiles = os.listdir('./Files')
            # update files in server
            if len(payload) == 1:
                key = payload[0]
                files = os.listdir('./Files')
                filename = None
                content = None
                framedSend(connection, key.encode(), False)
                print('Sending File Key...')
                print(files)
            else:
                key = payload[0]
                filename = payload[1]
                content = payload[2]

            # write file
            if filename not in files and filename is not None:
                fileDestination = './files/' + filename
                file = open(fileDestination, 'a')

                file.write(content)
                file.close()
                framedSend(connection, b'Sucess', False)
            else: # file was fond in server
                if filename:
                    print('%s found in server' %filename)
                    print('Not writing data...')
                    framedSend(connection, b'Error', False)
                    break
        sys.exit(0)
        connection.close()

