from typing import BinaryIO
import socket


def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:

    get_iface=socket.getaddrinfo(iface,port,family=socket.AF_UNSPEC)[0]
    iface = str(get_iface[4][0])

    if not use_udp:
        server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        server_socket.bind((iface, port))
        print("Hello, I am a server")
        server_socket.listen(5)
        cnt =0
        connSocket, clientAddr= server_socket.accept()
        print("Connection",cnt," from the client",str(clientAddr))
        print("got message from ",clientAddr)

        file_data= open(fp.name,"wb")
        while(True):
            res_file=connSocket.recv(256)
            if(res_file):
                file_data.write(res_file)
            else:
                break
        file_data.close()
        connSocket.close()
    
    else:
        server_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((iface, port))

        print("Hello, I am a server")
        res_file, clientAddress = server_socket.recvfrom(256)
        print("got message from",clientAddress)
        file_data= open(fp.name,"wb")

        if(res_file):
            file_data.write(res_file)
        file_data.close()
    server_socket.close()

def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:

    get_host=socket.getaddrinfo(host,port,family=socket.AF_UNSPEC)[0]
    host = str(get_host[4][0])

    host_addr=(host,port)
    if not use_udp:
        client_socket=socket.socket()
        client_socket.connect(host_addr)
        print("Hello, I am a client")
        open_file=open(fp.name,"rb")
        inp_file=open_file.read(256)
        while inp_file:
            client_socket.send(inp_file)
            inp_file=open_file.read(256)
        open_file.close()
    else:
        client_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Hello, I am a client")
        open_file=open(fp.name,"rb")
        inp_file=open_file.read(256)
        while inp_file:
            client_socket.sendto(inp_file, host_addr)
            inp_file=open_file.read(256)
        open_file.close()
    client_socket.close()



# from typing import BinaryIO
# import socket


# def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:

#     get_iface=socket.getaddrinfo(iface,port,family=socket.AF_UNSPEC)[0]
#     iface = str(get_iface[4][0])

#     if not use_udp:
#         server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
#         server_socket.bind((iface, port))
#         print("Hello, I am a server")
#         server_socket.listen(5)
#         cnt =0
#         connSocket, clientAddr= server_socket.accept()
#         print("Connection",cnt," from the client",str(clientAddr))
#         print("got message from ",clientAddr)

#         file_data= open(fp.name,"wb")
#         while(True):
#             res_file=connSocket.recv(256)
#             if(res_file):
#                 file_data.write(res_file)
#             else:
#                 break
#         file_data.close()
#         connSocket.close()
        
#     else:
#         server_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         server_socket.bind((iface, port))

#         print("Hello, I am a server")
#         res_file, clientAddress = server_socket.recvfrom(256)
#         print("got message from",clientAddress)
#         file_data= open(fp.name,"wb")
        
#         if(res_file):
#             file_data.write(res_file)
#         file_data.close()
#     server_socket.close()


# def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:

#     get_host=socket.getaddrinfo(host,port,family=socket.AF_UNSPEC)[0]
#     host = str(get_host[4][0])

#     host_addr=(host,port)
#     if not use_udp:
#         client_socket=socket.socket()
#         client_socket.connect(host_addr)
#         print("Hello, I am a client")
#         open_file=open(fp.name,"rb")
#         inp_file=open_file.read(256)
#         while inp_file:
#             client_socket.send(inp_file)
#             inp_file=open_file.read(256)
#         open_file.close()
#     else:
#         client_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         print("Hello, I am a client")
#         open_file=open(fp.name,"rb")
#         inp_file=open_file.read(256)
#         while inp_file:
#             client_socket.sendto(inp_file, host_addr)
#             inp_file=open_file.read(256)
#         open_file.close()
#     client_socket.close() 


