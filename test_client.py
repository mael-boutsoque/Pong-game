import socket
import json
import threading

class Client:
    def __init__(self) -> None:
        self.UDP_IP = str
        self.UDP_PORT = int

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = False
    
    def connected(self)->bool:
        return self.connection
    
    def start(self,ip:str,port:int):
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.sock.connect((self.UDP_IP,self.UDP_PORT))
        
        print("connected ✅")
        self.connection = True
    
    def start_threaded(self, ip: str, port: int):
        thread = threading.Thread(target=self._start_static, args=(ip, port, self.sock, self._connection_done), daemon=True)
        thread.start()
    
    @staticmethod
    def _start_static(ip:str,port:int,sock:socket.socket,connection_done_func):
        succes = False
        while not succes:
            try:
                sock.connect((ip,port))
                succes = True
            except:
                pass
        connection_done_func(sock)
        
    def _connection_done(self,sock:socket.socket):
        self.sock = sock
        print("connected ✅")
        self.connection = True
    
    def loop(self,data_send:bytes):
        #send
        self.sock.sendall(data_send)
        
        #receive
        msg:str = self.sock.recv(1024).decode()

        return msg

    def loopDic(self,dictionary:dict):
        if not self.connected() :
            raise Exception("Not connected")
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
    client = Client()
    client.start("localhost",5005)
    
    i=0
    while True:
        msg = f"serv {i}"
        receive = client.loop(msg.encode())
        print("send :",msg," receive :",receive)
        i+=1