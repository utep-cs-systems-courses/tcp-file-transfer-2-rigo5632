#! /bin/bash

cd ./../../client/
./Client.py -p -lf file.txt 
./Client.py -p -lf file2.txt 
./Client.py -p -lf file3.txt
./Client.py -p -lf file4.txt
./Client.py -p -lf file5.txt
./Client.py -p -lf file6.txt

./Client.py -p -lf file.txt 
./Client.py -p -lf file2.txt
./Client.py -p -lf file3.txt
./Client.py -p -lf file4.txt
./Client.py -p -lf file5.txt
./Client.py -p -lf file6.txt

cd ../..

if diff ./client/files/file.txt ./server/Files/file.txt; then
    echo "file.txt passed"
else
    echo "file.txt failed"
fi

if diff ./client/files/file2.txt ./server/Files/file2.txt; then
    echo "file2.txt passed"
else
    echo "file2.txt failed"
fi

if diff ./client/files/file3.txt ./server/Files/file3.txt; then
    echo "file3 passed"
else
    echo "file3 failed"
fi


