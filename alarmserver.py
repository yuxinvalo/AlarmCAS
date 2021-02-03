import socket
import sys
import time

from PyQt5 import QtWidgets, QtCore, QtMultimedia
from PyQt5.QtCore import QThread

PORT = 8899
DATA_SIZE = 12
BIND_ADDR = '192.168.124.3'


class AlarmServer(QtWidgets.QWidget):
    def __init__(self):
        super(AlarmServer, self).__init__()
        self.serverThread = WorkThread()
        self.serverThread._sk_signal.connect(self.server_rev_info)
        self.setup_ui()
        # self.setup_server()
        self.setup_alarm_sound()

    def setup_ui(self):
        # self.setMaximumSize(QtCore.QSize(860, 600))
        self.setMinimumSize(QtCore.QSize(860, 600))

        self.setWindowTitle("AlarmServer")
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(30)

        self.startButton = QtWidgets.QPushButton()
        self.startButton.setText("Start Listening")
        self.startButton.clicked.connect(self.start_listening)
        self.startButton.setEnabled(True)

        self.stopButton = QtWidgets.QPushButton()
        self.stopButton.setText("Stop Listening")
        self.stopButton.clicked.connect(self.stop_listening)
        self.stopButton.setEnabled(False)

        self.horizontalLayout.addWidget(self.startButton)
        self.horizontalLayout.addWidget(self.stopButton)

        self.textRecv = QtWidgets.QTextBrowser()
        # self.textRecv.append("")

        self.typeStrLable = QtWidgets.QLabel("CPU TYPE: ")
        self.typeLable = QtWidgets.QLabel("")
        self.eneryStrLabel = QtWidgets.QLabel("ENERY: ")
        self.eneryLabel = QtWidgets.QLabel("")
        self.alarmStrLabel = QtWidgets.QLabel("Alarm: ")
        self.alarmLabel = QtWidgets.QLabel("")
        self.horizontalLabelLayout = QtWidgets.QHBoxLayout()
        self.horizontalLabelLayout.setSpacing(30)
        self.horizontalLabelLayout.addWidget(self.typeStrLable)
        self.horizontalLabelLayout.addWidget(self.typeLable)
        self.horizontalLabelLayout.addWidget(self.eneryStrLabel)
        self.horizontalLabelLayout.addWidget(self.eneryLabel)
        self.horizontalLabelLayout.addWidget(self.alarmStrLabel)
        self.horizontalLabelLayout.addWidget(self.alarmLabel)

        self.mainLayout.addLayout(self.horizontalLayout)
        self.mainLayout.addWidget(self.textRecv)
        self.mainLayout.addLayout(self.horizontalLabelLayout)

    def setup_server(self):
        self.textRecv.append("Generated socket at: ")
        ip_port = (BIND_ADDR, PORT)
        sk = socket.socket()
        sk.bind(ip_port)
        self.textRecv.append(str(sk))
        sk.listen(5)
        self.serverThread.sk = sk

    def setup_alarm_sound(self):
        sound_file = './resource/alarm.wav'
        self.sound = QtMultimedia.QSoundEffect()
        self.sound.setSource(QtCore.QUrl.fromLocalFile(sound_file))
        self.sound.setLoopCount(1)
        self.sound.setVolume(100)

    def start_listening(self):
        self.setup_server()
        self.textRecv.append("Start listening")
        self.serverThread.listening = True
        self.serverThread.start()
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)

    def server_rev_info(self, info):
        if info == '' or len(info) < len(BIND_ADDR) + DATA_SIZE:
            return
        else:
            addr, info = info.split(",")
            self.textRecv.append("Recv alarm data from: " + addr + " with info: " + info)
            self.typeLable.setText(info[0:6])
            self.eneryLabel.setText(info[6:10])
            self.alarmLabel.setText(info[-1])
            isAlarm = int(info[-1])
            if isAlarm:
                self.sound.play()

    def stop_listening(self):
        self.textRecv.append("Stopping listening...")
        self.serverThread.stop()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)


class WorkThread(QThread):
    _sk_signal = QtCore.pyqtSignal(str)

    def __init__(self, socketServer=''):
        super(WorkThread, self).__init__()
        self.listening = False
        self.sk = socketServer

    def run(self):
        if self.sk == '':
            self.listening = False
            print("Work thread hasn't been initialized... ")
        while self.listening:
            try:
                conn, addr = self.sk.accept()
                data = conn.recv(DATA_SIZE)
                print("RECV ", end=": ")
                print(data)
                if len(data) == 0:
                    continue
                res = str(addr[0]) + "," + str(data, encoding="utf8")
                print(res)
                self._sk_signal.emit(res)
            except Exception as e:
                self._sk_signal.emit('')
                print("Exception while receiving data ..." + str(e))
                return
            time.sleep(0.05)
        print("Done... ")

    def stop(self):
        self.listening = False
        try:
            self.sk.close()
        except Exception as e:
            print("Close socket failed: " + str(e))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    v = AlarmServer()
    v.show()
    sys.exit(app.exec_())
