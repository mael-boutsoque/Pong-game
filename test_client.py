import socket

# Configuration du client
HOST = '127.0.0.1'  # Remplacer par l'IP de la machine A
PORT = 5000             # Même port que le serveur

# Connexion au serveur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.sendall(b"Hello from client")

# Réception de la réponse
response = client_socket.recv(1024)
print("Réponse du serveur:", response.decode())

client_socket.close()
