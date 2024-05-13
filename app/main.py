import socket

# Constants
HOST = 'localhost'
PORT = 4221

def send_http_response(connection, status_code, reason_phrase, body='', content_type='text/plain'):
    """Send an HTTP response to the client."""
    body_bytes = body.encode('utf-8')
    content_length = len(body_bytes)
    headers = (
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {content_length}\r\n"
    )
    response = f"HTTP/1.1 {status_code} {reason_phrase}\r\n{headers}\r\n{body}"
    connection.sendall(response.encode('utf-8'))

def main():
    print("Server is starting...")

    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    print(f"Server is running on {HOST}:{PORT}...")

    while True:
        connection, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        try:
            request = connection.recv(1024).decode('utf-8')
            print("Received request:")
            print(request)

            request_line = request.split('\r\n')[0]
            method, path, _ = request_line.split()

            if path == '/':
                send_http_response(connection, 200, "OK")
            elif path.startswith('/echo/'):
                echo_str = path[6:]
                send_http_response(connection, 200, "OK", body=echo_str)
            else:
                send_http_response(connection, 404, "Not Found")

        finally:
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()
