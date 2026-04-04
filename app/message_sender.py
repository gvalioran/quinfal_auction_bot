import socket

def send_text(msg: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 5001))
    sock.send(msg.encode("utf-8"))
    sock.close()





