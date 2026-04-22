import socket
import sys

def send_request(sock: socket.socket, command: str) -> str:
     msg_len = len(command) + 3
     formatted_len = f"{msg_len:03d}"
     full_msg = (formatted_len + command).encode()

     sock.sendall(full_msg)

     resp_len_bytes = sock.recv(3)
     resp_len = int(resp_len_bytes.decode().strip())
     resp = sock.recv(resp_len - 3).decode().strip()
     return resp

def main():
     if len(sys.argv) != 4:  
        print("用法: python client.py <主机> <端口> <请求文件路径>")  
        return
     
     host = sys.argv[1]