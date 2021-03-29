import socket
from PyQt5 import QtWidgets, QtCore
import mesageBox
import authorization
import chatWindow
import sys
from PyQt5.QtCore import QThread


nickname=""

class WorkerThread(QThread):# поток для асинхронного принятия сообщений
    def __init__(self):
        QThread.__init__(self)
    signal = QtCore.pyqtSignal(str)

    def run(self):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == '@name':
                    client.send(nickname.encode('utf-8'))
                else:
                    self.signal.emit(message)
            except:
                print('Ошибка в потоке')
                client.close()
                break

class ShowDialog(QtWidgets.QMainWindow,mesageBox.Ui_Dialog):# собственный MessageBox
    def __init__(self,textCapture,textMessage):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(textCapture)
        self.pushButton.clicked.connect(self.clickMethod)
        self.messageText.setText(textMessage)

    def clickMethod(self):
        self.close()

# окно регистрации
class AuthWindow(QtWidgets.QMainWindow, authorization.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_nickname)

    def get_nickname(self):
        global nickname
        nickname= self.lineEdit.text().strip()
        if nickname != '':
            self.chat_window = ChatWindow()
            self.chat_window.show()
            self.close()
        else:
            self.window = ShowDialog('Внимание', 'Никнейм не может быть пустым')
            self.window.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return:
            self.get_nickname()


# окно мессенджера
class ChatWindow(QtWidgets.QMainWindow,chatWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.sendMessage)
        self.start_thread()

    def start_thread(self):
        self.worker = WorkerThread()
        self.worker.start()
        self.worker.signal.connect(self.change_textedit)

    def change_textedit(self, val):
        self.textEdit.append(val)


    def sendMessage(self):
        message = self.lineEdit.text().strip()
        if message == '':
            pass
        else:
            client.send(f'{nickname} : {message}'.encode('utf-8'))
            self.lineEdit.clear()
            self.lineEdit.setFocus()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return:
            self.sendMessage()
# основная функция
def main():
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        app = QtWidgets.QApplication(sys.argv)
        try:
            client.connect(('localhost',5050))
            window = AuthWindow()
            window.show()
        except WindowsError:
            temp=ShowDialog('Внимание', 'Сервер не доступен')
            temp.show()
        sys.exit(app.exec())

if __name__ == '__main__':
    main()