

class Proto:
    def __init__(self, message: str, packet_number,timeout,ket_ack,max_message_length,max_message_length,window_size):

def getProtoFromTxt(text: str) -> Proto:
    message = None
    packet_number = -1
    timeout = -1
    packet_ack = -1
    max_message_length = -1
    window_size = -1
    lines = text.splitlines()
    for line in lines:
        if line.find("message:") == 0:
            message = line
        elif line.find("maximum_msg_size:") == 0:
            max_message_length = int(line[len("maximum_msg_size:"):])
        elif line.find("window_size:") == 0:
            window_size = int(line[len("window_size:"):])
        elif line.find("timeout:") == 0:
            timeout = int(line[len("timeout:"):])
        elif line.find("PACK_NUM:") == 0:
            packet_number = int(line[len("PACK_NUM:"):])
        elif line.find("ACK_PACK_NUM:") == 0:
            packet_ack = int(line[len("ACK_PACK_NUM:"):])
        elif message is not None:
            message += line
