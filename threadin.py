import socket
import sys
import thread
import datetime
import threading
import Queue


def on_new_ts(data, addrs):
    print("got here in thread!")
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

        if amount_received < amount_expected:
            data = sock.recv(50)
            amount_received += len(data)
            print('received {!r}'.format(data))
            print("IM IN HERE BITCH with: ", data)
            return data

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
        print("recieved:", data)
        #    print("nothing received!")
        #elif s.recv(1024) != 0:
        #    print("fuck me")
        #else:
        if data:
            for addrs in ts_addrs:
                try:
                    locked.acquire()
                    print("thread running for folowing addr:", addrs)
                    #below i use a queue to access thread return value 


                    #t = Thread(target=lambda q, arg1: q.put(on_new_(arg1)), args=(que, 'world!'))
                    #thread = threading.Thread(target = on_new_ts,args = (data, addrs))
                    thread = threading.Thread(target =lambda q, arg1, arg2: q.put(on_new_ts(arg1, arg2)),args = (que, data, addrs))
                    print("thread starting")

                    thread.start()

                    thread.join()
                    print("thread joined\n")


                    locked.release()
                    #hostname = "ERROR"
                    hostInfo = que.get()
                    print("host info: ",hostInfo)
                    print("received from either TS server:", hostInfo)
                    connection.sendall(hostInfo)
                finally:
                        print("something went wrong!")


    finally:
        print("yerrr...")
    print("onto next")
    #how to gracefully close this?????
s.close()
