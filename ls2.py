import socket
import sys
import thread
import datetime
import threading
import Queue
import select


def on_new_ts(data, addrs):
    tsHost, tsPort = addrs
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #talk to TS1
    server_address = (tsHost, tsPort)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    #add waiting f
    try:
        message = data
        print('sending {!r}'.format(message))
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        sock.setblocking(0)
        ready = select.select([sock], [], [], 5)
        if(ready[0]):
            data = sock.recv(50)
            response = data[:].decode("utf-8")
            que.put(response)
        else:
            print("Server Timeout")
            que.put(data + " - ERROR:HOST NOT FOUND")

    finally:
        print('closing socket')
        sock.close()


que = Queue.Queue()
# start with creating socket for client connection
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket created!")
except socket.error as err:
    print("socket creation failed!")
lsListenPort = int(sys.argv[1])
ts1Hostname = sys.argv[2]
ts1ListenPort = int(sys.argv[3])
ts2Hostname = sys.argv[4]
ts2ListenPort = int(sys.argv[5])
lsName = socket.gethostname()

locked = thread.allocate_lock() #initialize lock object
ts_addrs = ((ts1Hostname, ts1ListenPort),(ts2Hostname,ts2ListenPort))
s.bind((lsName,lsListenPort))
s.listen(4)
print("listening for incoming connections at port:", lsName, lsListenPort)
connection, address = s.accept()
print('connection from', address)
while True:
    #ip, port = str(address[0]), str(address[1])
    #print("Connected with " + ip + ":" + port) #connect with client
    try:
        data = connection.recv(250)
        response = data[:].decode("utf-8")
        if(len(response)<2):
            s.close()
            break
        if response:
            for addrs in ts_addrs:
                try:
                    locked.acquire()
                    print("thread running for folowing addr:", addrs)
                    #below i use a queue to access thread return value


                    #t = Thread(target=lambda q, arg1: q.put(on_new_(arg1)), args=(que, 'world!'))
                    #thread = threading.Thread(target = on_new_ts,args = (data, addrs))
                    print("DATA: " + response)
                    thread = threading.Thread(target = (on_new_ts(response, addrs)))
                    print("thread starting")

                    thread.start()

                    thread.join()
                    print("thread joined")


                    locked.release()
                    #hostname = "ERROR"
                finally:
                    print("TS checked\n")

            while(not que.empty()):
                hostInfo = que.get()
                if("ERROR:HOST NOT FOUND" not in hostInfo):
                    print("Host Found: " + hostInfo)
                    connection.sendall(hostInfo)
                    que.queue.clear()
                elif(que.empty() and "ERROR:HOST NOT FOUND" in hostInfo):
                    connection.sendall(hostInfo)

    finally:
        print("TS Search Concluded\n")
    #how to gracefully close this?????
