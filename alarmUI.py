from PyQt5 import QtCore, QtWidgets, QtGui


class AlarmUI(object):
    def setupUi(self, alarmFrame):
        alarmFrame.setObjectName("AlarmUI")
        # MyPing.setWindowIcon(QtGui.QIcon("ping.ico"))
        # MyPing.resize(660, 385)
        alarmFrame.setMaximumSize(QtCore.QSize(660, 425))
        alarmFrame.setMinimumSize(QtCore.QSize(660, 425))
        self.groupBox = QtWidgets.QGroupBox(alarmFrame)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 470, 50))
        self.groupBox.setObjectName("groupBox")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(10, 20, 441, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startIP = QtWidgets.QLineEdit(self.widget)
        self.startIP.setText("192.168.0.0")
        self.startIP.selectAll()
        self.startIP.setObjectName("startIP")
        self.horizontalLayout.addWidget(self.startIP)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.endIP = QtWidgets.QLineEdit(self.widget)
        self.endIP.setObjectName("endIP")
        self.horizontalLayout.addWidget(self.endIP)
        self.pingButton = QtWidgets.QPushButton(self.widget)
        self.pingButton.setObjectName("pingButton")
        self.stopButton = QtWidgets.QPushButton(self.widget)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.pingButton)
        self.horizontalLayout.addWidget(self.stopButton)
        self.widget1 = QtWidgets.QWidget(alarmFrame)
        self.widget1.setGeometry(QtCore.QRect(10, 70, 630, 345))
        self.widget1.setObjectName("widget1")
        self.gridlayout = QtWidgets.QGridLayout(self.widget1)
        self.gridlayout.setContentsMargins(0, 0, 0, 0)
        self.gridlayout.setObjectName("gridlayout")
        self.gridlayout.setSpacing(7)

        self.label_list = []
        list_index = 0
        for i in range(1, 17):
            for j in range(1, 17):
                label = QtWidgets.QLabel(self.widget1)
                label.setMinimumSize(QtCore.QSize(32, 15))
                label.setStyleSheet("background-color: rgb(203, 203, 203);")
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setText(QtCore.QCoreApplication.translate("Alarm", str(list_index)))
                self.label_list.append(label)
                self.gridlayout.addWidget(label, i-1, j-1, 1, 1)
                list_index += 1
        self.retranslateUi(alarmFrame)
        QtCore.QMetaObject.connectSlotsByName(alarmFrame)

    def retranslateUi(self, AlarmFrame):
        _translate = QtCore.QCoreApplication.translate
        AlarmFrame.setWindowTitle(_translate("AlarmFrame", "AlarmUI"))
        self.groupBox.setTitle(_translate("AlarmFrame", "Set IP Range"))
        self.label_2.setText(_translate("AlarmFrame", "——"))
        self.pingButton.setText(_translate("AlarmFrame", "Ping"))
        self.stopButton.setText(_translate("AlarmFrame", "Stop"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    alarmFrame = QtWidgets.QWidget()
    ui = AlarmUI()
    ui.setupUi(alarmFrame)
    alarmFrame.show()
    sys.exit(app.exec_())