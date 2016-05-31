import socket

target_host = "127.0.0.1"
target_port = 9999

# Build a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the target
client.connect((target_host, target_port))

# Send some data
client.send("Biu~biu~biu~!!")

# Receive some data
response = client.recv(4096)

print response
