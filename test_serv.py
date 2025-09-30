import socket
import json
import threading

class Server:
    def __init__(self) -> None:
        self.UDP_IP:str
        self.UDP_PORT:int

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.connection = False
    
    def connected(self)->bool:
        return self.connection
    
    def start(self,ip:str,port:int):
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        self.sock.listen(5)

        self.sock, self.UDP_PORT = self.sock.accept()
        print(f"connected ✅ sock = {self.sock} , port = {self.UDP_PORT}")
        self.connection = True
    
    def start_threaded(self, ip: str, port: int):
        thread = threading.Thread(target=self._start_static, args=(ip, port, self.sock, self._connection_done), daemon=True)
        thread.start()
    
    @staticmethod
    def _start_static(ip:str,port:int,sock:socket.socket,connection_done_func):
        sock.bind((ip,port))
        sock.listen(5)
        sock, UDP_PORT = sock.accept()
        connection_done_func(sock,UDP_PORT)
        
    def _connection_done(self,sock:socket.socket,port:int):
        self.sock = sock
        self.UDP_PORT = port
        print(f"connected ✅ sock = {self.sock} , port = {self.UDP_PORT}")
        self.connection = True
    
    def loop(self,data_send:bytes):
        #send
        self.sock.sendall(data_send)
        
        #receive
        msg:str = self.sock.recv(1024).decode()

        return msg
    
    def loopDic(self,dictionary:dict):
        #convert
        data = json.dumps(dictionary)
        data = data.encode()
        
        #send
        self.sock.sendall(data)
        
        #receive
        msg:str = self.sock.recv(1024).decode()
        data_received:dict = json.loads(msg)

        return data_received


if __name__ == "__main__":
    server = Server()
    server.start("0.0.0.0",5005)
    
    i=0
    while True:
        msg = f"serv {i}"
        receive = server.loop(msg.encode())
        print("send :",msg," receive :",receive)
        i += 1