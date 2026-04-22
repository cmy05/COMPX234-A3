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