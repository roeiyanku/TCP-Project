import socket
from Common import *

def send_message():
    host = '127.0.0.1'
    port = 11111

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    first_message = "Please provide The maximum size of a single message the server is willing to handle."

    client_socket.send(first_message.encode())

    response = client_socket.recv(1024)
    decoded_response = response.decode()
    print(f"{decoded_response}")

    maximum_msg_size = int(decoded_response)

    # text_message = input("Text example to send back to server and chop into different messages")
    dictionary = get_input(isServer=False)
    text_message=dictionary.get("message")
    window_size=dictionary.get("window_size")
    timeout=dictionary.get("timeout")

    size_of_message = len(text_message.encode('utf-8'))  # UTF-8 is the default encoding in python.
    num_messages = 0

    if size_of_message % maximum_msg_size == 0:
        num_messages = size_of_message // maximum_msg_size
    else:
        num_messages = size_of_message // maximum_msg_size + 1

    messages = []


    for i in range(num_messages):
        start = 0
        end = start + maximum_msg_size

        message = text_message[start:end]

        labeled_message = f"M{i}: {message}"
        messages.append(labeled_message)
        start = end

    #window_size = int(input("Please enter sliding window size:"))

    messages_sent = 0
    acks_till_now = 0
    first_unACK_msg = 0


    while messages_sent < len(messages):

        # wait for acknowledgment then send:
        while messages_sent-acks_till_now >= window_size:
            acks_till_now = int(client_socket.recv(1024).decode()[len("ACK"):])+1  # Receive the

        client_socket.sendall(f"M{messages_sent}:{messages[messages_sent]}".encode())
        messages_sent+=1

            #reset timer
            last_unACK_msg +=1
            print("Acknowledgment received. Sending next message.")
            num_ack += 1
        else:
            print("No acknowledgment received. Waiting.")

        if acks_till_now == len(messages):
            client_socket.close()
            print("Message sent and connection closed.")

send_message()
