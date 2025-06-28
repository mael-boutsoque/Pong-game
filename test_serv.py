import socket

# Configuration du serveur
HOST = '0.0.0.0'  # Écoute sur toutes les interfaces
PORT = 5000       # Port TCP à écouter

# Création et liaison du socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"En attente de connexion sur {HOST}:{PORT}...")

# Acceptation d'une connexion
conn, addr = server_socket.accept()
print(f"Connexion acceptée depuis {addr}")

# Boucle de réception / envoi
while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Reçu:", data.decode())
    conn.sendall(b"Message bien recu")

conn.close()
server_socket.close()
