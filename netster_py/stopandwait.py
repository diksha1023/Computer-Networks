from typing import BinaryIO
import socket
import pickle as pck

MAX_MSG_SIZE = 512
timeout = 0.06


def stopandwait_server(iface: str, port: int, fp: BinaryIO) -> None:
    get_iface = socket.getaddrinfo(iface, port, family=socket.AF_UNSPEC)[0]
    iface = str(get_iface[4][0])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((iface, port))
    server_socket.settimeout(timeout)

    recv_seqNum = 0
    print("Hello, I am a server")
    msg_hdr_server = [0, 0]  # ackn, seq_number

    while True:
        try:
            rcv_pckt, clientAddress = server_socket.recvfrom(1024)
        except socket.timeout:
            continue

        ackn, seqNum, msg = pck.loads(rcv_pckt)

        msg_hdr_server[0] = 1
        msg_hdr_server[1] = seqNum
        ack_send_back = pck.dumps(msg_hdr_server, pck.DEFAULT_PROTOCOL)

        if seqNum < recv_seqNum:
            # incorrect packet
            while True:
                try:
                    server_socket.sendto(ack_send_back, clientAddress)
                    break
                except socket.timeout:
                    continue
            continue

       # print("msg:", msg, " seqNum", seqNum, "\n")

        ### SEND ACK
        while True:
            try:
                server_socket.sendto(ack_send_back, clientAddress)
                break
            except socket.timeout:
                continue

        if not msg or len(msg) == 0:
            break
        fp.write(msg)
        fp.flush()
        recv_seqNum = 1 - recv_seqNum  ### recv_seqNum += 1

    fp.close()
    server_socket.close()


def stopandwait_client(host: str, port: int, fp: BinaryIO) -> None:
    get_host = socket.getaddrinfo(host, port, family=socket.AF_UNSPEC)[0]
    host = str(get_host[4][0])

    host_addr = (host, port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Hello, I am a client")

    client_socket.settimeout(timeout)

    client_seq_num = 0
    ack_num = 2
    flag_EOF = False
    open_file = open(fp.name, "rb")
    retrying = False

    while True:
        # ack_rcv_flag=False
        if not retrying:
            inp_data = open_file.read(MAX_MSG_SIZE) if not flag_EOF else b""
            msg_header = [ack_num, client_seq_num, inp_data]
            pck_send = pck.dumps(msg_header, protocol=pck.DEFAULT_PROTOCOL)

        retrying = True

        try:
            client_socket.sendto(pck_send, host_addr)
        except socket.timeout:
            continue

        # while not ack_rcv_flag:
        while True:
            try:
                res, addr = client_socket.recvfrom(1024)
            except socket.timeout:
                retrying = True
                break

            ackn, seqNum = pck.loads(res)
            if ackn == 1 and seqNum == client_seq_num:
                # ack_rcv_flag=True
                client_seq_num = 1 - client_seq_num
                retrying = False
                break

        if flag_EOF:
            break

        if inp_data == b"":
            flag_EOF = True

    fp.close()
    client_socket.close()



