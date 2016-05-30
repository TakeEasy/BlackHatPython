import socket

target_host = "www.baidu.com"
target_port = 80

# Build a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the target
client.connect((target_host, target_port))

# Send some data
client.send("GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n")

# Receive some data
response = client.recv(4096)

print response
