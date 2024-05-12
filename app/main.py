import socket

HOST = 'localhost'
PORT = 4221

def send_http_response(connection, status_code, reason_phrase):
    """Send an HTTP response to the client."""
    response = f"HTTP/1.1 {status_code} {reason_phrase}\r\n\r\n"
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
            path = request_line.split(' ')[1]

            if path == '/':
                send_http_response(connection, 200, "OK")
            else:
                send_http_response(connection, 404, "Not Found")

        finally:
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()