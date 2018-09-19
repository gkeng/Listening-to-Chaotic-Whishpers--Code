import socket 


def server(ip, port, nb_client_max=5):
    """
    Serveur socket pour transférer fichier depuis le serveur SIA
    :param ip:
    :param port:
    :param nb_client_max:
    :return:
    """
    server_socket = socket.socket()
    server_socket.bind((ip, port))
    server_socket.listen(nb_client_max)
    while True:
        client_socket, addr = server_socket.accept()
        with open('text_data/0000_2015-01-01/reuters/0000_0.txt', 'rb') as f:
            client_socket.sendfile(f, 0)
        client_socket.close()

if __name__ == '__main__':
    server('172.17.0.13', 22, 5)
