import socket
import sys
import os
import mimetypes


def response_ok(body=b"this is a pretty minimal response", mimetype=b"text/plain"):
    """returns a basic HTTP response"""
    resp = []
    resp.append(b"HTTP/1.1 200 OK")
    resp.append(b"Content-Type: text/plain")
    resp.append(b"")
    resp.append(body)
    # resp.append(b"this is a pretty minimal response")
    return b"\r\n".join(resp)


def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp).encode('utf8')


def response_not_found():
    """returns a 404 Not Found response"""
    return b""


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    return uri


def resolve_uri(uri):
    """This method should return appropriate content and a mime type"""
    dir_root = os.getcwd()
    print('dir_root:', dir_root)
    print('uri:', uri)
    try:
        dir_list = os.listdir(dir_root + uri)
        file_names = "\r\n".join(dir_list)
        # file_names = join("\r\n").dir_list
        # for file in dir_list:
        #     mime = mimetypes.guess_type(file)
        print('dir_list:', dir_list)
        # print('files:', files)
    except FileNotFoundError:
        print("file not found")

    return file_names.encode('utf8'), b"text/plain"

    # return b"still broken", b"text/plain"


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
                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')
                    if len(data) < 1024:
                        break

                try:
                    uri = parse_request(request)
                except NotImplementedError:
                    response = response_method_not_allowed()
                else:
                    try:
                        content, mime_type = resolve_uri(uri)
                    except NameError:
                        response = response_not_found()
                    else:
                        response = response_ok(content, mime_type)

                print('sending response', file=log_buffer)
                conn.sendall(response)
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)