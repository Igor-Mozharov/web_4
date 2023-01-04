import datetime
import os.path
import socket
import  json

def run_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            print('S_Server is running!')
            data, address = sock.recvfrom(1024)
            if not data:
                break
            result = {}
            response = ''
            try:
                with open('storage/data.json', 'rb') as file:
                    result = json.loads(file.read())
                    print('1')
                with open('storage/data.json', 'wb') as file:
                    value = json(data.decode('utf-8'))
                    key = str(datetime.datetime.now())
                    result[key] = value
                    file.write(json.dumps(result).encode())
                    print('2')
            except Exception as ex:
                response = str(ex)
            sock.sendto(response.encode(), address)
    except KeyboardInterrupt:
        sock.close()

def run_client(host, port, data = ''):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = json.dumps(data).encode()
    sock.sendto(data, (host, port))
    response, address = sock.recvfrom(1024)
    sock.close()
    return response
