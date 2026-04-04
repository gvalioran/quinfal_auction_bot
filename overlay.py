# overlay_server.py
import sys
import socket
import threading
from PyQt5 import QtWidgets, QtGui, QtCore


class Overlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = "Фаза 1\n подойди к доске задач\n Доска задач не найдена"

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool |
            QtCore.Qt.WindowTransparentForInput
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        self.font = QtGui.QFont("Consolas", 14, QtGui.QFont.Bold)
        self.color = QtGui.QColor(0, 255, 0)

        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setFont(self.font)
        painter.setPen(self.color)
        rect = QtCore.QRect(50, 50, 800, 600)
        painter.drawText(rect, QtCore.Qt.AlignLeft | QtCore.Qt.TextWordWrap, self.text)
        #painter.drawText(50, 50, self.text)

    @QtCore.pyqtSlot(str)
    def update_text(self, new_text):
        self.text = new_text
        self.update()


def tcp_server(overlay: Overlay):
    """Простой TCP сервер, принимающий строки."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 5001))
    sock.listen(1)

    print("Overlay server listening on 127.0.0.1:5001")

    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024).decode("utf-8").strip()
        if data:
            overlay.update_text(data)
        conn.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    overlay = Overlay()
    # сервер в отдельном потоке
    threading.Thread(target=tcp_server, args=(overlay,), daemon=True).start()
    sys.exit(app.exec_())
