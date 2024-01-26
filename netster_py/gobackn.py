from typing import BinaryIO
import socket
import pickle as pck

timeout = 0.06

def gbn_server(iface:str, port:int, fp:BinaryIO) -> None:
    get_iface = socket.getaddrinfo(iface, port, family=socket.AF_UNSPEC)[0]
    iface = str(get_iface[4][0])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((iface, port))
    server_socket.settimeout(timeout)

    recv_seqNum = 0
    memory_buffer=bytearray()

    print("Hello, I am a server")
    msg_hdr_server = [0, 0]  # ackn, seq_number

    while True:
        try:
            rcv_pckt, clientAddress = server_socket.recvfrom(1024)
        except socket.timeout:
            continue

        seqNum, msg = pck.loads(rcv_pckt)

        if seqNum==recv_seqNum:
            if not msg or len(msg) == 0:
                msg_hdr_server[0] = 2
                msg_hdr_server[1] = recv_seqNum
                ack_send_back = pck.dumps(msg_hdr_server, pck.DEFAULT_PROTOCOL)
                server_socket.sendto(ack_send_back, clientAddress)
                break
            memory_buffer.extend(msg)
            recv_seqNum+=1
        
        msg_hdr_server[0] = 1
        msg_hdr_server[1] = recv_seqNum
        ack_send_back = pck.dumps(msg_hdr_server, pck.DEFAULT_PROTOCOL)
        server_socket.sendto(ack_send_back, clientAddress)
        
    fp.write(memory_buffer)
    fp.flush()
 

    fp.close()
    server_socket.close()


def gbn_client(host:str, port:int, fp:BinaryIO) -> None:
    get_host = socket.getaddrinfo(host, port, family=socket.AF_UNSPEC)[0]
    host = str(get_host[4][0])

    host_addr = (host, port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Hello, I am a client")

    client_seq_num = 0
    open_file = open(fp.name, "rb")
    retrying = False
    size_window=4
    start_window=0

    hdr_size=len(pck.dumps( [0,b""], pck.DEFAULT_PROTOCOL))
    MAX_DATA_SIZE=256-hdr_size

    inp_file_data=[]
    inp_file=open_file.read(MAX_DATA_SIZE)
    while inp_file:
        inp_file_data.append(inp_file)
        inp_file=open_file.read(MAX_DATA_SIZE)
    inp_file_data.append(b"")
    
    file_len=len(inp_file_data)
    
    while start_window<file_len:

        while client_seq_num<min(file_len,start_window+size_window):
            msg_header = [client_seq_num,inp_file_data[client_seq_num]]
            pck_send = pck.dumps(msg_header, protocol=pck.DEFAULT_PROTOCOL)
            client_socket.sendto(pck_send, host_addr)
            #print(f"packet with sequence No.:{client_seq_num}")
            client_seq_num+=1

        client_socket.settimeout(timeout)
        try:
            res, addr = client_socket.recvfrom(1024)
            ackn,rcv_seqNo = pck.loads(res)
            #print(f"received ack for seq no:{rcv_seqNo}")
            if ackn==2:
                break
            if rcv_seqNo>start_window:
                start_window = rcv_seqNo
            size_window= min(size_window+1,128)
        except socket.timeout:
            #print(f"timeout, resend from seq no:{start_window}")
            client_seq_num= start_window
            size_window = max(1,size_window//2)

    fp.close()
    client_socket.close()