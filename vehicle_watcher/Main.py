# -*- coding: utf-8 -*-
'''
pyuic5 *.ui > xx.py
'''

import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import QApplication , QMainWindow
from PyQt5.QtCore import QObject
from MainFrame import *
import color
from qmqtt import MqttClient

HOST = "10.10.40.100"
PORT = 1883

class MyApp(Ui_MainWindow, QObject):
    debug_request_sig = QtCore.pyqtSignal(int, int)

    def debug_request(self):
        vn = self.vehicle_no.text()
        _class = self.comboBox_class.currentIndex()
        int_vn = int(vn[2:])
        self.debug_request_sig.emit(_class, int_vn)
        self.textBrowser.clear()

    def on_connect(self):
        self.client = MqttClient(self)
        self.client.stateChanged.connect(self.on_stateChanged)
        self.client.messageSignal.connect(self.on_messageSignal)
        self.debug_request_sig.connect(self.client.send_debug_request)

        self.client.hostname = self.mqtt_ip.text()
        self.client.port = int( self.mqtt_port.text() )
        self.client.connectToHost()

    def on_disconnect(self):
        self.client.disconnectFromHost()

    @QtCore.pyqtSlot(int)
    def on_stateChanged(self, state):
        if state == MqttClient.Connected:
            print('on_stateChanged', state)

            vn = self.vehicle_no.text()
            prefix = vn[:2]
            int_vn = int(vn[2:])

            self.client.subscribe("ZJ/Carrier/Debug/N%04d" % int_vn)

    @QtCore.pyqtSlot(int, int, str)
    def on_messageSignal(self, _type, _class, msg):
        try:
            #print("on_messageSignal", msg)
            #self.textBrowser.setHtml('<pre>' + color.parse_log_general(msg) + '</pre>')
            if _class == 0:
                self.textBrowser.setHtml(
                    '<body bgcolor="black"><pre style="color:white">' + color.parse_log_general(msg) + '</pre></body>')
            elif _class == 1:
                self.textBrowser.setHtml(
                    '<body bgcolor="black"><pre style="color:white">' + color.parse_log_motion(msg) + '</pre></body>')

        except ValueError:
            print("error: Not number")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = MyApp()
    ui.setupUi(mainWindow)

    ui.mqtt_ip.setText(HOST)
    ui.mqtt_port.setText(str(PORT))
    ui.vehicle_no.setText("VN0021")

    ui.comboBox_class.addItems(["log_general", "log_motion"])

    #line = 'script:ok,-9999, 0, 0,    -1; can:55555; lift:unkno, 0,0,   0,   0,   0,0,  0; basic:work,new,o,m; slam:ok; task:    97,  23#,   0,   0,   0,   0,   0,  23,  -1,n; motion:un, 0,3,   0, 0,0; route:m(),c(),b(),tc:0,0'
    #print('<body bgcolor="black"><pre style="color:white">' + color.parse_log_general(line) + '</pre></body>')

    #line = ' ,110472,-1174,-51,30400,103143,-44,-25,56698,6020,27000,4,18,18,300,100,15,0,-44,0,45235,56686,6039,270510,56688,5694,270515,0,12,5,0,2,1393,-36,online:12-14%,1,a:3,e:0,-1,auto ,'
    #print('<body bgcolor="black"><pre style="color:white">' + color.parse_log_motion(line) + '</pre></body>')

    mainWindow.show()  # 用来显示窗口

    ui.pushButton_connect.clicked.connect( ui.on_connect )
    ui.pushButton_disconnect.clicked.connect( ui.on_disconnect  )
    ui.pushButton_refresh.clicked.connect( ui.debug_request )

    app.exec_()
    print("exit ... ")

