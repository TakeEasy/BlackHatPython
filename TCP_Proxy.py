import sys
import socket
import threading
def server_loop(local_host,local_port,remote_host,remote_port,receive_first):

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind(local_host,local_port)
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host,local_port)
        print "[!!] Check for other listening sockets or correct premission."
        sys.exit()


    print "[*] Listening on %s:%d" % (local_host,local_port)

    server.listen(5)

    while True:
        client_socket,addr = server.accept()

        #print local connection imformation
        print "[==>] Receiced incoming connection from %s:%d" % (addr[0],addr[1])
        proxy_thread = threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first))
        proxy_thread.start()

def proxy_handler(client_socket,remote_host,remote_port,receive_first):

    #connect remote host

    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    remote_socket.connect((remote_host,remote_port))

    #if receice first:
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        #remote_buffer to response handler
        remote_buffer = response_handler(remote_buffer)

        #if we have data need to send local
        if len(remote_buffer):
            print "[<==] Sending %d bytes to localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)
    #read data from localhost and send to remotehost
