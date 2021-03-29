import socket
import threading

host = '127.0.0.1'
port = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print('Server started...')

clients = []
nicknames = []

# функция рассылает всем пользователям сообщение, которое ей передаётся
def broadcast(message):
    for client in clients:
        client.send(message)

# функция принимает сообщения от клиента и рассылает другим юзерам
def handle(client,addr):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except WindowsError as er:
            print(f'Отключение с адресом {addr[0]}:{addr[1]}')
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left.'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# функция обрабатывает первое подключение пользователя
def receive():
    while True:
        try:
            client, addr = server.accept()
            print(f'Подключение с адресом {addr[0]}:{addr[1]}')

            client.send('@name'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            clients.append(client)
            broadcast(f'{nickname} присоединился!'.encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client,addr,))
            thread.start()
        except WindowsError as er:
            print(f'Отключение с адресом {addr[0]}:{addr[1]}')

receive()
