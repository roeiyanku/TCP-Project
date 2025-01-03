import os


def get_input(isServer: bool):
    #https: // www.geeksforgeeks.org / python - list - files - in -a - directory /
    file_name = ""
    message = ""
    max_message_length = -1
    window_size = -1
    timeout = -1
    for fn in os.listdir():
        if fn.endswith(".txt"):
            file_name = fn
            break
    if file_name == "":
        #from input
        if isServer:
            max_message_length = input("what is the maximum message length? ")
        else:
            message = input("what is the message? ")
            window_size = input("what is the window size? ")
            timeout = input("what is the timeout? ")
    else:
        #from file
        file = open(file_name, "r")
        for line in file:
            if line.find("message:") == 0:
                message = line[len("message:"):]
            elif line.find("maximum_msg_size:") == 0:
                max_message_length = int(line[len("maximum_msg_size:"):])
            elif line.find("window_size:") == 0:
                window_size = int(line[len("window_size:"):])
            elif line.find("timeout:") == 0:
                timeout = int(line[len("timeout:"):])
            elif message != "":
                message += line
    if isServer:
        return {"max_message_length": int(max_message_length)}
    else:
        return {"message": message, "window_size": int(window_size), "timeout": int(timeout)}
