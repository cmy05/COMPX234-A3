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
     port = int(sys.argv[2])
     file_path = sys.argv[3]

     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
     sock.connect((host, port))

     try:  
        with open(file_path, "r", encoding="utf-8") as f:  
            lines = f.readlines() 
        
        for line in lines: 
            line = line.strip() 
            if not line:  
                continue
        
            if len(line) > 970:  
                print(f"{line}: 错误 - 长度超过限制")  
                continue

            parts = line.split(maxsplit=1)  
            if not parts:  
                continue 

            cmd = parts[0]
            if cmd == "PUT":  
                kv = parts[1].split(maxsplit=1)  
                if len(kv) < 2: 
                    print(f"{line}: 错误 - 格式无效")  
                    continue  
                key, val = kv  
                req = f"P {key} {val}"
            elif cmd == "READ":  
                key = parts[1]  
                req = f"R {key}"