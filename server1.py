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