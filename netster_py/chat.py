
import socket
import os
import threading
import sys

def chat_server(iface:str, port:int, use_udp:bool) -> None:
    
    get_iface=socket.getaddrinfo(iface,port,family=socket.AF_UNSPEC)[0]
    iface = str(get_iface[4][0])
    if not use_udp:
        server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        server_socket.bind((iface, port))
        print("Hello, I am a server")
        server_socket.listen() #optional for udp, queue - no. of connections that can wait in the queue
        cnt =0
        while True:
            thread_stp=False
            connSocket, clientAddr= server_socket.accept()
            print("Connection",cnt," from the client",str(clientAddr))
            #msg = connSocket.recv(2048)
            print("got message from ",clientAddr)
            
            #msg=msg.decode()
            #connSocket.send(msg.encode('utf-8'))
            thread=threading.Thread(target=clients_multithread,args=(connSocket,clientAddr))
            thread.start()
            cnt+=1
    else:
        server_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((iface, port))
    
        print("Hello, I am a server")
        while True:
            msg, clientAddress = server_socket.recvfrom(2048)
            print("got message from",clientAddress)
            msg=msg.decode('utf-8').strip()
            #min_n=min(255,len(msg))
            #msg=msg[:min_n]

            if(msg =="hello"):
                server_socket.sendto("world\n".encode('utf-8'), clientAddress)
            elif(msg=="goodbye"):
                server_socket.sendto("farewell\n".encode('utf-8'), clientAddress)
            elif(msg=="exit"):
                server_socket.sendto("ok\n".encode('utf-8'), clientAddress)
                break
            else:
                server_socket.sendto(msg.encode('utf-8'), clientAddress)

    server_socket.close()

def chat_client(host:str, port:int, use_udp:bool) -> None:

    get_host=socket.getaddrinfo(host,port,family=socket.AF_UNSPEC)[0]
    host = str(get_host[4][0])
    #ai_family, ai_socktype, ai_proto, ai_canonname, ai_addr= socket.getaddrinfo
    
    host_addr=(host,port)
    if not use_udp:
        client_socket=socket.socket()
        client_socket.connect(host_addr)
        print("Hello, I am a client")
        while True:
            msg=input()
            #min_n=min(255,len(msg))
            #msg=msg[:min_n]
            client_socket.send(msg.encode('utf-8'))
            response=client_socket.recv(2048)
            res=response.decode('utf-8').strip()
            #print("check: ", res,"msg_o :", msg_t,"\n")
            print(res)
            if(res=="farewell"):
                break
            elif(msg=="exit" and res=="ok"):
                #print("exit: ",res)
                break
    else:
        client_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Hello, I am a client")
        while True:
            msg=input()
            #min_n=min(255,len(msg))
            #msg=msg[:min_n]
            client_socket.sendto(msg.encode('utf-8'),host_addr)
            response, addr=client_socket.recvfrom(1024)
            res=response.decode('utf-8').strip()
            print(res)
            if(res=="farewell"):
                break
            if(msg=='exit' and res =="ok"):
                break
    client_socket.close()

def clients_multithread(conn,clientAddr) -> None:
    while conn:
        res=conn.recv(256).decode('utf-8').strip()
        print("got message from ",clientAddr)
        #min_n=min(255,len(data))
        #data=data[:min_n]
        if(res=='goodbye'):
            #send_resp='farewell'
            conn.send("farewell\n".encode('utf-8'))
            break
        elif(res=='hello'):
            #send_resp="world"
            conn.send("world".encode('utf-8'))
        elif(res=='exit'):
            #send_resp='ok'
            conn.send("ok".encode('utf-8'))
            conn.close()
            os._exit(1)
            #sys.exit(0)
        else:
            #send_resp=data
            conn.send(res.encode('utf-8'))
