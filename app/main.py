import socket

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is running on port 4221...")

    connection, client_address = server_socket.accept()
    print(f"Connected by {client_address}")

    try:
        http_response = "HTTP/1.1 200 OK\r\n\r\n"
        
        connection.sendall(http_response.encode('utf-8'))
        print("Response sent to the client.")
    finally:
        connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()