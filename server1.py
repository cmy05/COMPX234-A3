import socket  
import threading  
import time  
from typing import Dict 

class TupleSpace:
    def __init__(self):  
        self.tuples: Dict[str, str] = {}  
        self.lock = threading.Lock()  

        self.total_connections = 0  
        self.total_ops = 0  
        self.read_ops = 0  
        self.get_ops = 0  
        self.put_ops = 0  
        self.error_ops = 0

    def put(self, key: str, value: str) -> int: 
        with self.lock:  
            self.total_ops += 1  
            self.put_ops += 1  
            if key in self.tuples:  
                self.error_ops += 1  
                return 1  
            self.tuples[key] = value  
            return 0 
    def read(self, key: str) -> str | None: 
        with self.lock:  
            self.total_ops += 1  
            self.read_ops += 1  
            if key not in self.tuples: 
                self.error_ops += 1 
                return None  
            return self.tuples.get(key)
    def get(self, key: str) -> str | None:  
        with self.lock:  
            self.total_ops += 1  
            self.get_ops += 1  
            if key not in self.tuples:  
                self.error_ops += 1  
                return None 
            return self.tuples.pop(key) 
        
    def stats_printer(tuple_space: TupleSpace):
        while True:  
         time.sleep(10)  
         with tuple_space.lock: 
             total = len(tuple_space.tuples)
             if total == 0:  
                avg_tup = avg_key = avg_val = 0.0  
             else:  
                avg_tup = sum(len(k)+len(v) for k,v in tuple_space.tuples.items()) / total  
                avg_key = sum(len(k) for k in tuple_space.tuples.keys()) / total  
                avg_val = sum(len(v) for v in tuple_space.tuples.values()) / total

             print("\n====== SERVER STATS (10s) ======")  # 打印统计信息分隔线
             print(f"Tuples: {total}")  # 打印当前元组数量
             print(f"Avg tuple: {avg_tup:.2f}  Avg key: {avg_key:.2f}  Avg val: {avg_val:.2f}")  # 打印平均大小
             print(f"Connections: {tuple_space.total_connections}")  # 打印总连接数
             print(f"Ops: total={tuple_space.total_ops} READ={tuple_space.read_ops} GET={tuple_space.get_ops} PUT={tuple_space.put_ops} ERR={tuple_space.error_ops}")  # 打印操作统计
             print("================================\n")  

    def handle_client(client_socket, tuple_space):
        try:  
            with client_socket:  
               tuple_space.total_connections += 1 
               while True: 
                len_head = client_socket.recv(3)  
                if not len_head:  
                    break  
                msg_len = int(len_head.decode().strip()) 
                msg = client_socket.recv(msg_len - 3).decode().strip()  
                parts = msg.split() 
                if not parts:  
                    continue  

                op = parts[0]  
                resp = ""

                if op == "R":  
                    key = parts[1]  
                    val = tuple_space.read(key)  
                    resp = f"OK ({key}, {val}) read" if val else f"ERR {key} does not exist"  
                    key = parts[1]  
                    val = tuple_space.get(key)  
                    resp = f"OK ({key}, {val}) removed" if val else f"ERR {key} does not exist"  
                elif op == "P":  
                    key = parts[1]  
                    val = " ".join(parts[2:]) if len(parts)>=3 else ""  
                    ret = tuple_space.put(key, val)  
                    resp = f"OK ({key}, {val}) added" if ret == 0 else f"ERR {key} already exists"
                else:  
                    resp = "ERR invalid command"

                full = resp  
                rlen = len(full) + 3 
                send = f"{rlen:03d}{full}".encode()
                client_socket.sendall(send)
        except:  
         pass 
    def main():
         import sys
         if len(sys.argv) != 2: 
          print("Usage: python server.py <port> (50000-59999)") 
          return
         port = int(sys.argv[1])
         