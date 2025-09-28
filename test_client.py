import socket
import json

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
    client = Client()
    client.start("localhost",5005)
    
    i=0
    while True:
        msg = f"serv {i}"
        receive = client.loop(msg.encode())
        print("send :",msg," receive :",receive)
        i+=1