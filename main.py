from threading import  Thread
from server import run
from socket_server import run_server

if __name__ == '__main__':
    thread_server = Thread(target=run)
    thread_socket = Thread(target=run_server, args=('0.0.0.0', 5000))
    thread_server.start()
    thread_socket.start()