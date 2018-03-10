"""
Sencillo chat de terminal multiplataforma pensado para redes locales.
Escrito en Python 3.6.4
"""

import sys
import socket
import threading

# Mensaje de ayuda cuando no se proporcionan dos argumentos.
def helpmsg(str):
    print(str)
    exit()

if len(sys.argv) != 3:
    helpmsg("Ayuda: "+sys.argv[0]+" IP puerto")

# Pasa los parámetros a variables y valida el puerto.
ip = str(sys.argv[1])

try:
    port = int(sys.argv[2])
except(ValueError):
    helpmsg("Error: El puerto debe ser un valor numérico entero.")

if port < 0 or port > 65535:
    helpmsg("Error: Puerto fuera del rango válido [0-65535].")

# Crea el socket TCP servidor y establece los parámetros.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Escucha del socket servidor en la IP y el puerto.
try:
    server.bind((ip, port))
except(socket.gaierror):
    helpmsg("Error: dirección IP inválida.")
except(OSError):
    helpmsg("Error: Puerto ya en uso.")

server.listen(100) # Hasta 100 clientes simultáneos. Editar si es necesario.

# Array de sockets de clientes y variable de salida.
clients = []
exit = False

# Función de eliminación de cliente del array.
def remove(conn):
    if conn in clients:
        clients.remove(conn)

# Función de envío de mensajes a todos los clientes.
def broadcast(msg, conn):
    for c in clients:
        #if c != conn:
        try:
            c.send(msg.encode("utf-8"))
        except:
            c.close()
            remove(c)

# Hilos de clientes.
def clientthread(conn, addr):
    conn.send((" - Conectado a "+ip+" -").encode("utf-8"))
    while not exit:
        try:
            msg = conn.recv(2048).decode("utf-8")
            if msg == "!q":
                msg_send = " - "+addr[0]+" se ha desconectado -"
            else:
                msg_send = "["+addr[0]+"]: "+msg
            print(msg_send)
            broadcast(msg_send, conn)
        except:
            remove(conn)
            break

# Hilo del servidor.
def serverthread():
    while not exit:
        try:
            conn, addr = server.accept()
            clients.append(conn)
            print(" - "+addr[0]+" se ha conectado -")
            threading.Thread(target=clientthread, args=(conn, addr)).start()
        except:
            break

# Empieza el hilo servidor.
threading.Thread(target=serverthread).start()

# Ayuda al inicio.
print("Servidor en escucha, !q : salir")

# Bucle principal. Espera entrada y envía mensajes del servidor.
while not exit:
    try:
        msg = input()
        if msg == "!q":
            broadcast("!q", None)
            exit = True
            for c in clients:
                c.close()
                clients.remove(c)
            server.close()
        else:
            broadcast("[Servidor]: "+msg, None)
    except: #(KeyboardInterrupt, SystemExit):
        exit = True
        server.close()
        exit()
