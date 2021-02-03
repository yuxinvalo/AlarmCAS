#!/usr/bin/python3
# Project:
# Author: syx10
# Time 2021/2/3:9:42
import socket
import sys
import re
import threading
import subprocess
import time

from PyQt5 import QtCore, QtWidgets
from alarmUI import AlarmUI


# Configurations
CONNECTED_SOCKET = {}
ALARM_STRING = 'LM'
PORT = 8899


class AlarmServer(QtWidgets.QWidget):
    _ping_signal = QtCore.pyqtSignal(bool, str)

    def __init__(self):
        super(AlarmServer, self).__init__()
        self.ui = AlarmUI()
        self.ui.setupUi(self)
        self.ui.startIP.editingFinished.connect(self.set_end_ip)
        self.ui.pingButton.clicked.connect(self.start_ping)
        self.ui.stopButton.clicked.connect(self.stop_checking)
        self._ping_signal.connect(self.set_ui)
        self.inspecting = False

    def set_end_ip(self):
        '''
        填写起始地址后，默认填写结束地址为xxx.xxx.xxx.255
        '''
        startip = self.ui.startIP.text()
        pattern = r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$)"
        m = re.match(pattern, startip)      # 检查IP地址是否合法
        if m:
            startip = startip.split('.')
            startip[3] = '255'
            endip = '.'.join(startip)
            self.ui.endIP.setText(endip)
        else:
            QtWidgets.QMessageBox.warning(self, "easyPing", "IP地址错误")
            self.ui.startIP.setFocus()
            self.ui.startIP.selectAll()

    def start_ping(self):
        '''
        启动多线程
        '''
        self.reset_ui()
        startip = self.ui.startIP.text().split('.')
        endip = self.ui.endIP.text().split('.')
        tmp_ip = startip
        self.inspecting = True
        pthread_list = []
        for i in range(int(startip[3]), int(endip[3]) + 1):
            tmp_ip[3] = str(i)
            ip = '.'.join(tmp_ip)
            pthread_list.append(threading.Thread(target=self.get_ping_result, args=(ip,)))
        for item in pthread_list:
            item.setDaemon(True)
            item.start()

    def get_ping_result(self, ip):
        global CONNECTED_SOCKET
        while self.inspecting:
            cmd_str = "ping {0} -n 1 -w 600".format(ip)
            DETACHED_PROCESS = 0x00000008   # 不创建cmd窗口
            try:
                subprocess.run(cmd_str, creationflags=DETACHED_PROCESS, check=True)  # 仅用于windows系统
            except subprocess.CalledProcessError as err:
                self._ping_signal.emit(False, ip)
            else:
                self._ping_signal.emit(True, ip)
                if ip in CONNECTED_SOCKET.keys():
                    try:
                        data = CONNECTED_SOCKET[ip].recv(512)
                        if data == ALARM_STRING:
                            print("GOT ALARM FROM " + str(ip))
                    except Exception as e:
                        print("EXCEPTION WHEN TRY TO CONNECT DEVICE: " + ip)
                else:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((ip, PORT))
                        CONNECTED_SOCKET[ip] = s
                        data = s.recv(13)
                        if data[0:2] == ALARM_STRING:
                            print("GOT ALARM FROM " + str(ip))
                    except Exception as e:
                        print("EXCEPTION WHEN TRY TO CONNECT DEVICE: " + ip)
            time.sleep(1)

    def stop_checking(self):
        self.inspecting = False

    def reset_ui(self):
        ''' 初始化窗口IP窗格为灰色背景 '''
        for item in self.ui.label_list:
            item.setStyleSheet("background-color: rgb(203, 203, 203);")

    def set_ui(self, result, ip):
        '''
        设置窗口颜色
            result：线程ping的结果
            ip：为对于的IP地址
        '''
        index = int(ip.split('.')[3])
        if result:
            self.ui.label_list[index].setStyleSheet("background-color: rgb(85, 170, 127);") # 设置背景为绿色
        else:
            self.ui.label_list[index].setStyleSheet("background-color: rgb(255, 142, 119);")    # 设置背景为红色


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    easy = AlarmServer()
    easy.show()
    sys.exit(app.exec_())