import socket
import threading

bind_ip = "127.0.0.1"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))

server.listen(5)
print "[*] Listen on %s:%d" % (bind_ip, bind_port)


# Client handle thread function
def handle_client(client_socket):
    # Print message that receive from client
    request = client_socket.recv(1024)
    print "[*] Receive: %s" % request

    # Send back a message
    client_socket.send("ACK!")
    client_socket.close()


while True:
    client, addr = server.accept()
    print "[*] Accept connection from: %s:%d" % (addr[0], addr[1])

    # Hang on the thread and handle the data
    client_handle = threading.Thread(target=handle_client, args=(client,))
    client_handle.start()
