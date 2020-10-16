#! /usr/bin/python3

import os, socket, re, sys
sys.path.append('../lib')
import params
from encapFramedSock import EncapFramedSock
from threading import Thread, Lock

# params
switchesVarDefaults = (
    (('-l', '--listentPort'), 'listenPort', 50001),
    (('-p', '--proxy'), 'proxy', False),
    (('-?', '--usage'), 'usage', False)
)

paramMap = params.parseParams(switchesVarDefaults)
listenPort, proxy, usage = paramMap['listenPort'], paramMap['proxy'], paramMap['usage']

# display params usage
if usage: params.usage()

# listen on port 50001
listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenerSocket.bind(('', listenPort))
listenerSocket.listen(5)
print('listening...')

serverFiles = os.listdir('./Files/') # files that are in our server
inProgressFiles = {}  # keep track of working files
key = '-1' # client key, unique key for each client 
lock = Lock()

class Server(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.clientSocket, self.clientAddress = connection
        self.framedSocket = EncapFramedSock(connection)
    def run(self):
        global key, serverFiles, inProgressFiles, lock
        self.framedSocket.send(key.encode(), False) # send key to client

        filename = ''
        content = ''
        
        while True:
            data = self.framedSocket.receive(False)
            if not data: # unexpected client shutdown
                if filename in inProgressFiles.keys() and filename not in serverFiles:
                    file = './Files/' + filename
                    os.remove(file)
                    print('Deleting File: %s' %filename)
                return
            data = data.decode()
            payload = re.split(':', data) # get data from client (key:filename:data)
            if len(payload) == 1: # reset flags and add to server filename to sever list
                key = payload[0]
                if filename in inProgressFiles.keys():
                    lock.acquire()
                    del inProgressFiles[filename]
                    lock.release()
                serverFiles.append(filename)
                filename = None
                content = None
                print('Saving File Key...')

                print('Server Files: ', serverFiles)
                print('In Progress Files: ', inProgressFiles)
            else:
                key = payload[0]
                filename = payload[1]
                content = payload[2]

            if filename not in serverFiles and filename is not None: # new file
                if filename not in inProgressFiles.keys(): # add file to working directory
                    print('adding key')
                    lock.acquire()
                    inProgressFiles[filename] = key
                    lock.release()
                if filename in inProgressFiles.keys() and inProgressFiles[filename] == key: # handles multiple users writing to the same file
                    fileDestination = './Files/' + filename
                    file = open(fileDestination, 'a')
                    print('Writing to %s' %filename)

                    file.write(content)
                    file.close()
                else:
                    print('Writing to same file')
                    return
            else: # file already exists
                if filename is not None:
                    print('%s found in server' %filename)
                    print('Not writing data...')


while True:
    connection = listenerSocket.accept()
    lock.acquire()
    key = int(key) + 1
    key = str(key)
    lock.release()
    server = Server(connection)
    server.start()

