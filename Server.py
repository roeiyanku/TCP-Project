import socket
from Common import *


def get_params_from_file():
    file = open("values.txt", "r")
    fileStr = file.read(1024)


def start_server(to_do_timeout_problem: bool):
    host = '127.0.0.1'
    port = 11111
    segments = {}
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server is listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"connection established with {addr}")

    message = conn.recv(1).decode()
    settings = get_input(isServer=True)
    maximum_msg_size = settings.get("max_message_length")
    response = f"{maximum_msg_size}"
    conn.send(response.encode())

    # while server is open:

    acks = 0
    stop=False
    while True:
        #whole_segment = conn.recv(1024).decode()
        start_of_message=""
        segment=""
        first=conn.recv(1).decode()
        if not first:
            conn.close()
            break
        while True:
            received = conn.recv(1).decode()

            if received==":":
                break
            else:
                start_of_message += received
        segment_num=int(start_of_message)
        segment=conn.recv(maximum_msg_size).decode()


        print(f"segment num: {segment_num}")
        if to_do_timeout_problem and segment_num==2:
            to_do_timeout_problem=False
            continue

        segments[segment_num] = segment
        #ack=0
        while acks in segments.keys():
            print(f"found seg{acks}")
            acks += 1
        #ack -= 1
        if acks>0:
            conn.sendall(f"ACK{acks-1}:".encode())
            print(f"Sent ACK{acks-1} for segment {segment_num}")
            
            

    conn.close()
    print("Connection closed.")
    str_result = ""
    #print(segments)
    for i in range(acks):
        print(i)
        str_result = str_result+segments[i]
    print(str_result)

start_server(to_do_timeout_problem=False)
