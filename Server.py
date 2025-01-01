import socket
from Common import *

def get_params_from_file():
    file=open("values.txt","r")
    fileStr=file.read(1024)


def startServerGal():
    host = '127.0.0.1'
    port = 11111
    segments={}
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)


    print(f"Server is listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"connection established with {addr}")

    message = conn.recv(1024).decode()
    settings = get_input(isServer=False)
    maximum_msg_size = settings.get("max_message_length")
    response = f"{maximum_msg_size}"
    conn.send(response.encode())

    # while server is open:

    ack = 0
    while True:
        whole_segment = conn.recv(1024).decode()
        start_of_message=whole_segment.find(":")+1
        segmant_num=whole_segment[1:start_of_message]
        segment=whole_segment[start_of_message:]

        segments[segmant_num]=segment
        if segmant_num==ack+1:
            ack+=1
        else:
            while ack in segments.keys():
                ack+=1
            ack-=1
        conn.sendall(f"ACK{ack}".encode())


    print("Connection closed.")

def start_server():
    host = '127.0.0.1'
    port = 11111

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server is listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"connection established with {addr}")

    message = conn.recv(1024).decode()

    maximum_msg_size = input()
    response = f"{maximum_msg_size}"
    conn.send(response.encode())

    #while server is open:
    ack = 0
    message = conn.recv(1024).decode()

    if message == f"M{ack}":
        response = f"ACK{ack}"
        conn.send(response.encode())
        ack += 1

    else:
        response = f"ACK{ack}"
        conn.send(response.encode())


    print("Connection closed.")


startServerGal()

#max_message_size=20
