# TCP File Transfer with Threads
This section of the lab focuses on allowing multiple clients (each with their own thread), write files to our TCP server.
Features Include:
1. Work with and without a proxy
2. Supports multiple clients
3. Handle files with no data
4. Handle files that do not exist
5. Handle if either server or client disconnect

## How to Run
```bash
python3 Server.py
python3 Client.py -lf local_filename
```
```bash
python3 Server.py
python3 Client.py -lf local_filename -rf remote_filename
```
```bash
python3 Server.py
python3 Client.py -s ip_address:port_number of server -lf local_filename -rf remote_filename
```
#### Params
* -lf local file name, must be within the files directory
* -rf how the file will be named in the remote server (optional). By default the remote file name is the local file name
* -s specify the IP address and port number of sever
###
Note: Must run server first, otherwise client will not find port number

## Client:
1. Establish Connection to server
2. Get key to write file
3. Create a payload that will contain file data (key:filename:file_data)
4. Send all packets with frameSock.send
5. Check if local file name exists
6. Check if file has data to send
7. Update key if file transfer was successful 

## Server
1. Send a unique key to each client
2. Write data into file
3. Make sure that no more than 1 client is writing to a file
4. Update key once client has finished writing to file
5. Check if file already exists in server