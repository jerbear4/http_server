import socket
import sys


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                while True:
                    data = conn.recv(1024)
                    # print('data:', data)
                    if len(data) < 1024:
                        break
                    print('sending response', file=log_buffer)
                    response = response_ok()
                    conn.sendall(response)
                    # print('received "{0}"'.format(data), file=log_buffer)
                    # if data:
                    #     print('sending data back to client', file=log_buffer)
                    #     response = response_ok()
                    #     conn.sendall(response)
                    # else:
                    #     msg = 'no more data from {0}:{1}'.format(*addr)
                    #     print(msg, log_buffer)
                    #     break
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return

def response_ok():
    """returns a basic HTTP response"""
    resp = []
    resp.append(b"HTTP/1.1 200 OK")
    resp.append(b"Content-Type: text/plain")
    resp.append(b"")
    resp.append(b"this is a pretty minimal respose")
    return b"\r\n".join(resp)


if __name__ == '__main__':
    server()
    sys.exit(0)