import socket
import sys
import thread
import datetime


#get hosts and ports
lsListenPort = sys.argv[1]
ts1Hostname = sys.argv[2]
ts1ListenPort = sys.argv[3]
ts2Hostname = sys.argv[4]
ts2ListenPort = sys.argv[5]


#create socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("socket creation failed!")

#function for handling each other connections
def on_new_client(clientsocket,conn, addr, data):
    error = data + "Error:HOST NOT FOUND"
    while True:
        #add time out function
        data = conn.recv(1024)
        if data:
            clientsocket.sendall(data)
        else:
            clientsocket.sendall(data)

    conn.close()




lsName = socket.gethostname()
s.bind((lsListen, lsName))
s.listen(4)

locked = threading.Lock()


#
while true:
    clientsocket, addr = s.accept()
    #send message to both and see if theres a response
    print('Established connection with addr', addr)
    data = s.recv(250)
    print(data)

    while true:
        #forwards for each new connection
        locked.acquire()
        #print('Connected to: )
        conn, addr = s.accept()     # Establish connection with client.
        thread.start_new_thread(on_new_client,(clientsocket, conn,addr, data))

        # uses: ts1ListenPort, ts1Hostname
        #data locked (sent to two ts servers and one is sent back)


        retValue #what was returned from either
