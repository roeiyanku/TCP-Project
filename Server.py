import socket
from Common import *


def get_params_from_file():
    file = open("values.txt", "r")
    fileStr = file.read(1024)


def start_server():
    host = '127.0.0.1'
    port = 11111
    segments = {}
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server is listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"connection established with {addr}")

    message = conn.recv(1024).decode()
    settings = get_input(isServer=True)
    maximum_msg_size = settings.get("max_message_length")
    response = f"{maximum_msg_size}"
    conn.send(response.encode())

    # while server is open:

    ack = 0

    while True:
        whole_segment = conn.recv(1024).decode()
        if not whole_segment:
            #print("end")
            break
        start_of_message = int(whole_segment.find(":")) + 1
        #print(start_of_message)
        segment_num = int(whole_segment[1:start_of_message - 1])
        segment = whole_segment[start_of_message:]
        print(f"segment num: {segment_num}")
        segments[segment_num] = segment
        #ack=0
        if segment_num == ack:
            while ack in segments.keys():
                print(f"found seg{ack}")
                ack += 1
            #ack -= 1
            conn.sendall(f"ACK{ack-1}".encode())
            print(f"Sent ACK{ack-1} for segment {segment_num}")
            
            

    #conn.close()
    print("Connection closed.")
    str_result = ""
    #print(segments)
    for i in range(ack):
        print(i)
        str_result = str_result+segments[i]
    print(str_result)


start_server()
