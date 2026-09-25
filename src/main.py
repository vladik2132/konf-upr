import os
import socket

while True:
    prompt = f"{os.getlogin()}@{socket.gethostname()}:~$ "
    line = input(prompt).strip()
    if not line:
        continue
    expanded_line = os.path.expanduser(line)
    parts = expanded_line.split()
    cmd = parts[0]
    args = parts[1:]
    if cmd == "exit":
        break
    elif cmd in ("ls", "cd"):
        print(f"Команда: {cmd}, Аргументы: {args}")
    else:
        print(f"Неизвестная команда: {cmd}")
