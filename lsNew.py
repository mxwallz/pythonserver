import socket
import sys
import thread
import datetime

def on_new_ts(data, tsHost, tsPort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #talk to TS1
    server_address = (tsHost, tsPort)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
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

    finally:
        print('closing socket')
        sock.close()

#function for handling each other connections
def on_new_client(clientsocket, addr):
    error = data + "Error:HOST NOT FOUND"
    while True:
        #add time out function
        conn, addr = s.accept()     # Establish connection with client.
        print('Established connection with addr', addr)
        data = conn.recv(1024)
        thread.start_new_thread(on_new_ts, (data,ts1Hostname, ts1ListenPort))
        locked.release()
        print(data)
        if data:
            clientsocket.sendall(data)
        else:
            clientsocket.sendall(error)

    conn.close()


#get hosts and ports
lsListenPort = int(sys.argv[1])
ts1Hostname = sys.argv[2]
ts1ListenPort = int(sys.argv[3])
ts2Hostname = sys.argv[4]
ts2ListenPort = int(sys.argv[5])

#create socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("socket creation failed!")

lsName = socket.gethostname()
s.bind((lsName,lsListenPort))
s.listen(4)

locked = thread.allocate_lock()


while True:
    #forwards for each new connection
    #locked.acquire()
    #print('Connected to: )
    thread.start_new_thread(on_new_client,(s,))
    #locked.release()
        # uses: ts1ListenPort, ts1Hostname
        #data locked (sent to two ts servers and one is sent back)
    # Clean up the connection
print("Closing current connection")
connection.close()
