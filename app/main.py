import socket
import os
import argparse
import re

# Constants
HOST = 'localhost'
PORT = 4221

def parse_args():
    parser = argparse.ArgumentParser(description="HTTP Server that can serve files, handle specific endpoints, accept file uploads, and support content encoding.")
    parser.add_argument("--directory", default=os.getcwd(), help="Directory to serve files from and save uploads to. Defaults to current working directory.")
    return parser.parse_args()

def send_http_response(connection, status_code, reason_phrase, body='', content_type='text/plain', content_encoding=None):
    if isinstance(body, str):
        body = body.encode('utf-8')  # Ensure the body is in bytes
    content_length = len(body)
    headers = [
        f"Content-Type: {content_type}",
        f"Content-Length: {content_length}"
    ]
    if content_encoding:
        headers.append(f"Content-Encoding: {content_encoding}")
    
    header_str = '\r\n'.join(headers)
    response = f"HTTP/1.1 {status_code} {reason_phrase}\r\n{header_str}\r\n\r\n{body.decode('utf-8')}"
    connection.sendall(response.encode('utf-8'))

def handle_request(connection, args):
    request = connection.recv(4096).decode('utf-8')
    print("Received request:")
    print(request)

    headers, body = request.split('\r\n\r\n', 1)
    request_line = headers.split('\r\n')[0]
    method, path, _ = request_line.split()
    accept_encoding = next((line.split(": ")[1] for line in headers.split('\r\n') if line.startswith("Accept-Encoding: ")), '')

    if path == '/':
        send_http_response(connection, 200, "OK")
    elif path == '/user-agent':
        user_agent = next((line.split(": ")[1] for line in headers.split('\r\n') if line.startswith("User-Agent: ")), "Unknown")
        send_http_response(connection, 200, "OK", body=user_agent)
    elif path.startswith('/echo/'):
        echo_str = path[6:]  # Extracts the string after '/echo/'
        if 'gzip' in accept_encoding:
            send_http_response(connection, 200, "OK", body=echo_str, content_type='text/plain', content_encoding='gzip')
        else:
            send_http_response(connection, 200, "OK", body=echo_str, content_type='text/plain')
    elif path.startswith('/files/') and method == 'GET':
        filename = path[7:]  # Extract the filename after '/files/'
        filepath = os.path.join(args.directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as file:
                file_data = file.read()
            send_http_response(connection, 200, "OK", body=file_data, content_type='application/octet-stream')
        else:
            send_http_response(connection, 404, "Not Found", content_type='text/plain')
    elif path.startswith('/files/') and method == 'POST':
        filename = path[7:]  # Extract the filename after '/files/'
        filepath = os.path.join(args.directory, filename)
        with open(filepath, 'wb') as file:
            file.write(body.encode('utf-8'))  # Write the binary data to file
        send_http_response(connection, 201, "Created")
    else:
        send_http_response(connection, 404, "Not Found")

def main():
    args = parse_args()
    print(f"Server will serve files from and save uploads to {args.directory}")

    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    print(f"Server is running on {HOST}:{PORT}...")

    while True:
        connection, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        try:
            handle_request(connection, args)
        finally:
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()
