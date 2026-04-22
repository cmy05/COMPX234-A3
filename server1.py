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