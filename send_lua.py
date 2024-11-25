import sys
import socket
import struct
import os.path

def send_payload(ip, port, filepath, timeout=10):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
        
    try:
        with open(filepath, "rb") as f:
            data = f.read()
    except IOError as e:
        raise IOError(f"Failed to read file: {e}")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((ip, int(port)))
            
            # Send size (qword) + data
            size = struct.pack("<Q", len(data))
            sock.sendall(size + data)

            # Receive response
            response = []
            while True:
                try:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    response.append(chunk)
                except socket.timeout:
                    print("Warning: Socket timeout while receiving response")
                    break

            return b''.join(response).decode("latin-1")
                
    except socket.error as e:
        raise ConnectionError(f"Socket error: {e}")

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <ps-ip> <port> <filepath>")
        return 1

    try:
        ip, port, filepath = sys.argv[1:]
        response = send_payload(ip, port, filepath)
        print(response)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())