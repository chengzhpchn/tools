# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainFrame.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 571, 541))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(600, 30, 54, 12))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(600, 100, 54, 12))
        self.label_3.setObjectName("label_3")
        self.mqtt_ip = QtWidgets.QLineEdit(self.centralwidget)
        self.mqtt_ip.setGeometry(QtCore.QRect(670, 20, 113, 20))
        self.mqtt_ip.setObjectName("mqtt_ip")
        self.comboBox_class = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_class.setGeometry(QtCore.QRect(600, 260, 101, 22))
        self.comboBox_class.setObjectName("comboBox_class")
        self.pushButton_refresh = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_refresh.setGeometry(QtCore.QRect(710, 260, 75, 23))
        self.pushButton_refresh.setObjectName("pushButton_refresh")
        self.pushButton_connect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connect.setGeometry(QtCore.QRect(600, 140, 75, 23))
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.pushButton_disconnect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_disconnect.setGeometry(QtCore.QRect(710, 140, 75, 23))
        self.pushButton_disconnect.setObjectName("pushButton_disconnect")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(590, 0, 201, 181))
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 61, 16))
        self.label_2.setObjectName("label_2")
        self.mqtt_port = QtWidgets.QLineEdit(self.groupBox)
        self.mqtt_port.setGeometry(QtCore.QRect(80, 60, 113, 20))
        self.mqtt_port.setObjectName("mqtt_port")
        self.vehicle_no = QtWidgets.QLineEdit(self.groupBox)
        self.vehicle_no.setGeometry(QtCore.QRect(80, 100, 113, 20))
        self.vehicle_no.setObjectName("vehicle_no")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(600, 240, 54, 12))
        self.label_4.setObjectName("label_4")
        self.groupBox.raise_()
        self.textBrowser.raise_()
        self.label.raise_()
        self.label_3.raise_()
        self.mqtt_ip.raise_()
        self.comboBox_class.raise_()
        self.pushButton_refresh.raise_()
        self.pushButton_connect.raise_()
        self.pushButton_disconnect.raise_()
        self.label_4.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "服务器IP"))
        self.label_3.setText(_translate("MainWindow", "小车车号"))
        self.pushButton_refresh.setText(_translate("MainWindow", "刷新"))
        self.pushButton_connect.setText(_translate("MainWindow", "连接"))
        self.pushButton_disconnect.setText(_translate("MainWindow", "断开"))
        self.groupBox.setTitle(_translate("MainWindow", "MQTT"))
        self.label_2.setText(_translate("MainWindow", "服务器端口"))
        self.label_4.setText(_translate("MainWindow", "日志类型："))
