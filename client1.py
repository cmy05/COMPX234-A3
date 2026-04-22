import socket
import sys

def send_request(sock: socket.socket, command: str) -> str:
     msg_len = len(command) + 3