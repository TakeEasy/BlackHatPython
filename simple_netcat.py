import sys
import socket
import getopt
import threading
import subprocess

# definition of some global variables

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    print "Sample Netcat Tool"
    print
    print "Usage: simple_netcat.py -t target_host -p port"
    print "-l --listen"
    print "-e --execute=file_to_run"
    print "-c --command"
    print "-u --upload=destination"
    print
    print
    print "Examples: "
    print "simple_netcat.py -t 192.168.0.1 -p 55555 -l -c"
    print "simple_netcat.py -t 192.168.0.1 -p 55555 -l -u=c:\\target.exe"
    print "simple_netcat.py -t 192.168.0.1 -p 55555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./simple_netcat.py -t 192.168.11.12 -p 135"
    sys.exit(0)


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:

            # wait data back
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            print response,

            # wait more input
            buffer = raw_input("")
            buffer += "\n"

            # send out
            client.send(buffer)

    except:
        print "[*] Exception! Exiting."
        client.close()


def server_loop():
    global target

    # if dosen't define any target ip will listen all ip
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):
    command = command.rstrip()

    # run command and return the result
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failde to execute command. \r\n"

    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    # upload file
    if len(upload_destination):
        # read all data and writ the target
        file_buffer = ""
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    # run command
    if len(execute):
        output = run_command(execute)

        client_socket.send(output)

    # if need a shell
    if command:
        client_socket.send("<SNC:#> ")
        while True:
            #client_socket.send("<SNC:#> ")

            # receive data until \n
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            response = run_command(cmd_buffer)
            response += "\n<SNC:#> "
            client_socket.send(response)


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and port > 0:
        # read data from stdin
        # will block key the CTRL-D to stop
        buffer = sys.stdin.read()

        # send data
        client_sender(buffer)

    # start listen prepare to upload file execute command
    # put a shell
    # base on argv
    if listen:
        server_loop()


main()
