#!/usr/bin/env python3
import socket
import subprocess
import json
import os

SOCKET_PATH = "/var/run/servermonitor.sock"

if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind(SOCKET_PATH)
os.chmod(SOCKET_PATH, 0o666)  
sock.listen(5)

while True:
    conn, _ = sock.accept()
    data = conn.recv(1024).decode().strip()

    if not data:
        conn.close()
        continue

    if data.startswith("smart "):
        device = data.split()[1]

        try:
            if "nvme" in device:
                output = subprocess.check_output(
                    ["nvme", "smart-log", "-o", 'json', device],
                    text=True
                )
            else:
                output = subprocess.check_output(
                    ["smartctl", "-a", "-j", device],
                    text=True
                )
            conn.sendall(output.encode())
        except Exception as e:
            conn.sendall(str(e).encode())

    else:
        conn.sendall(b"Comando invalido")

    conn.close()
