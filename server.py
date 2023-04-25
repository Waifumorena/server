import socket
import threading
import os

# Dirección IP del servidor
HOST = '149.56.67.133'
# Puerto en el que se ejecutará el servidor
PORT = 3389

# Lista de clientes conectados al servidor
clientes = []


def manejar_cliente(cliente, direccion):
    print(f"Conexión establecida desde {direccion}")
    cliente.send("Bienvenido al chat!".encode())

    while True:
        try:
            mensaje = cliente.recv(1024).decode()
            if mensaje:
                if mensaje.startswith("/enviar"):
                    filename = mensaje.split()[1]
                    file_size = os.path.getsize(filename)
                    cliente.send(f"{filename} {file_size}".encode())
                    with open(filename, 'rb') as f:
                        while True:
                            data = f.read(1024)
                            if not data:
                                break
                            cliente.sendall(data)
                else:
                    mensaje_formateado = f"<{direccion[0]}> {mensaje}"
                    print(mensaje_formateado)
                    difundir_mensaje(mensaje_formateado, cliente)
            else:
                quitar_cliente(cliente)
                break
        except:
            quitar_cliente(cliente)
            break


def difundir_mensaje(mensaje, cliente):
    for c in clientes:
        if c != cliente:
            try:
                c.send(mensaje.encode())
            except:
                quitar_cliente(c)
        else:
            mensaje_formateado = f"<yo> {mensaje}"
            try:
                c.send(mensaje_formateado.encode())
            except:
                quitar_cliente(c)


def quitar_cliente(cliente):
    if cliente in clientes:
        clientes.remove(cliente)
        cliente.close()


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()

    print(f"Servidor escuchando en {HOST}:{PORT}...")

    while True:
        cliente, direccion = servidor.accept()
        clientes.append(cliente)
        cliente_thread = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
        cliente_thread.start()


if __name__ == '__main__':
    main()
