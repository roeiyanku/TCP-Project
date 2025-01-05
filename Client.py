import socket
from Common import *
import threading
import time


# https://www.geeksforgeeks.org/multithreading-python-set-1/
# ://www.geeksforgeeks.org/python-time-module/
# how in python to auto close socket when program finish
def receive_messages(sock: socket, dictionary: dict,):
    while dictionary["messages_acks"] < dictionary["messages_len"]:
        time_acks_new=""
        char=""
        while True:
            char=client_socket.recv(1).decode()
            if not char or char==":":
                break
            else:
                time_acks_new+=char
        time_acks_new=int(time_acks_new[len("ACK"):])
        #time_acks_new = int(client_socket.recv(1024).decode()[len("ACK"):]) + 1
        #print("rec")
        # if receive new higher acks ->reset time
        if time_acks_new >= dictionary["messages_acks"]:
            dictionary["time_start"] = time.time()
            dictionary["messages_acks"] = time_acks_new+1
            print(f"ACK{time_acks_new} received")


def send_messages(sock: socket, dictionary: dict,to_do_order_problem: bool):
    #for reseting => start_time=time.time()
    #for checking => if time.time()-start_time>=dictionary["timeout"]
    dictionary["time_start"] = time.time()
    #while dictionary["messages_sent"] < dictionary["messages_len"]:
    while dictionary["messages_acks"] < dictionary["messages_len"]:

        while dictionary["messages_sent"]>=dictionary["messages_len"] or dictionary["messages_sent"] - dictionary["messages_acks"] >= dictionary["window_size"]:
            #print(f"pass...last sent M{dictionary["messages_sent"]}, received ACK{dictionary["messages_acks"]}")


            time_passed=time.time() - dictionary["time_start"]
            if time_passed >= dictionary["timeout"]:
                dictionary["messages_sent"] = dictionary["messages_acks"]
                print(f"time reseted, send again from M{dictionary["messages_sent"]}")
                dictionary["time_start"] = time.time()
            print("overflowed window size")
            if dictionary["messages_acks"] >= dictionary["messages_len"]:
                break
            #time.sleep(0.1)
        if dictionary["messages_sent"] >= len(messages):
            continue

        # check_time
        #if so -> messages_sent=messages_acks and time.reset

        time_passed = time.time() - dictionary["time_start"]
        if (time_passed>0):
            p=1
        if time_passed >= dictionary["timeout"]:
            dictionary["messages_sent"] = dictionary["messages_acks"]
            print(f"time reseted, send again from M{dictionary["messages_sent"]}")
            dictionary["time_start"] = time.time()

        to_send = dictionary["messages_sent"]
        if to_do_order_problem:
            if to_send == 0:
                to_send = 1
            elif to_send == 1:
                to_send=0
                to_do_order_problem = False

        sock.sendall(f"M{to_send}:{messages[to_send]}".encode())
        print(f"M{to_send} sent\n")
        dictionary["messages_sent"] += 1


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 11111

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        #first_message = "Please provide The maximum size of a single message the server is willing to handle."
        first_message = "F"
        client_socket.sendall(first_message.encode())

        dictionary = get_input(isServer=False)
        dictionary["messages_sent"] = 0
        dictionary["messages_acks"] = 0
        dictionary["time_start"] = time.time()
        text_message = dictionary.get("message")
        window_size = dictionary.get("window_size")
        timeout = dictionary.get("timeout")
        response = client_socket.recv(1024)
        decoded_response = response.decode()

        dictionary["maximum_msg_size"] = int(decoded_response)

        size_of_message = len(text_message.encode('utf-8'))  # UTF-8 is the default encoding in python.
        num_messages = 0

        if size_of_message % dictionary["maximum_msg_size"] == 0:
            num_messages = size_of_message // dictionary["maximum_msg_size"]
        else:
            num_messages = size_of_message // dictionary["maximum_msg_size"] + 1

        messages = []

        start = 0
        for i in range(num_messages):
            end = start + dictionary["maximum_msg_size"]

            message = text_message[start:end]

            labeled_message = f"M{i}: {message}"
            messages.append(message)
            start = end
        print(messages)
        dictionary["messages_len"] = len(messages)
        t1 = threading.Thread(target=receive_messages, args=(client_socket, dictionary))
        t2 = threading.Thread(target=send_messages, args=(client_socket, dictionary,False))


        t1.start()
        t2.start()
        t1.join()
        t2.join()

