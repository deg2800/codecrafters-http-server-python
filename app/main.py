import socket
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="HTTP Server with directory argument.")
    parser.add_argument("--directory", required=True, help="Directory to serve files from.")
    return parser.parse_args()

def send_http_response(connection, status_code, reason_phrase, body=b'', content_type='application/octet-stream'):
    content_length = len(body)
    headers = (
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {content_length}\r\n"
    )
    response = f"HTTP/1.1 {status_code} {reason_phrase}\r\n{headers}\r\n"
    connection.sendall(response.encode('utf-8') + body)

def handle_request(connection, base_directory):
    request = connection.recv(1024).decode('utf-8')
    print("Received request:")
    print(request)

    request_line = request.split('\r\n')[0]
    method, path, _ = request_line.split()

    if path.startswith('/files/'):
        filename = path[7:]  # Extract the filename after '/files/'
        filepath = os.path.join(base_directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as file:
                file_data = file.read()
            send_http_response(connection, 200, "OK", body=file_data)
        else:
            send_http_response(connection, 404, "Not Found", body=b'', content_type='text/plain')
    else:
        send_http_response(connection, 404, "Not Found", body=b'', content_type='text/plain')

def main():
    args = parse_args()
    print(f"Server will serve files from {args.directory}")

    server_socket = socket.create_server(('localhost', 4221), reuse_port=True)
    print("Server is running on localhost:4221...")

    while True:
        connection, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        try:
            handle_request(connection, args.directory)
        finally:
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()
