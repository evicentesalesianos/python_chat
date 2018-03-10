"""
Sencillo chat de terminal multiplataforma pensado para redes locales.
Escrito en Python 3.6.4
"""

import sys
import socket
import threading

exit = False

# Mensaje de ayuda cuando no se proporcionan dos argumentos.
def helpmsg(str):
    print(str)
    exit()

if len(sys.argv) != 3:
    helpmsg("Ayuda: "+sys.argv[0]+" IP puerto")

# Valida los parámetros y los pasa a variables.
try:
    socket.inet_pton(socket.AF_INET, sys.argv[1])
except(OSError):
    helpmsg("Error: dirección IP inválida.")

ip = sys.argv[1]

try:
    port = int(sys.argv[2])
except(ValueError):
    helpmsg("Error: El puerto debe ser un valor numérico entero.")

if port < 0 or port > 65535:
    helpmsg("Error: Puerto fuera del rango válido [0-65535].")

# Crea el socket TCP servidor e intenta conectar con el mismo.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, port))


"""valid = False
user = input("Nombre: ")
if len(user) > 0 and len(user) <= 256:
    valid = True
"""
print("!q : salir")

def serverthread():
    while not exit:
        try:
            msg = server.recv(2048).decode("utf-8")
            if msg == "!q":
                print(" - El servidor se ha desconectado -")
                stopandquit()
            else:
                print(msg)
        except:
            break

def stopandquit():
    exit = True
    server.close()
    sys.exit()

threading.Thread(target=serverthread).start()

while not exit:
    try:
        msg = input()
        if msg == "!q":
            exit = True
        server.send(msg.encode("utf-8"))
    except: #(KeyboardInterrupt, SystemExit):
        stopandquit()
