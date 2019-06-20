# -*- coding: utf-8 -*-
'''
pyuic5 *.ui > xx.py
'''
import paho.mqtt.client as mqtt
import protocol
import json
import traceback

import threading

import sys
from PyQt5.QtWidgets import QApplication , QMainWindow, QTableWidgetItem, QAbstractItemView
from mainwindow import *

HOST = "10.10.40.100"
PORT = 1883

CarrierCommonTopic = "ZJ/Carrier/Commom/"
SystemCommonTopic = "ZJ/System/Commom/"
CarrierStatus1Topic = "ZJ/Carrier/Status1/"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    assert (rc == 0)
    client.subscribe(CarrierCommonTopic + '+')
    client.subscribe(CarrierStatus1Topic + 'N0001')
    client.subscribe(SystemCommonTopic + '+')

table_dict = {} # class : index: int

def on_message(client, userdata, msg):
    print("Topic: " + msg.topic)
    global ui
    try:
        _type, _class, content = protocol.parse_header(msg.payload)
        #del ret['bytes']
        #print(json.dumps(ret, indent=4, sort_keys=True))
        index = table_dict.get(_class, None)
        if index == None:
            index = len(table_dict)
            table_dict[_class] = index
            ui.tableWidget.setRowCount(index + 1)
            datas = [msg.topic, '0x%02x' % _class, _type, ' '.join(['%02x' % i for i in content])]
            for i in range(4):
                newItem = QTableWidgetItem(datas[i])
                ui.tableWidget.setItem(index, i, newItem)
        else:
            newItem = QTableWidgetItem( ' '.join(['%02x' % i for i in content]) )
            ui.tableWidget.setItem(index, 3, newItem)


    except Exception:
        traceback.print_exc()


def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("zj-r", "68689168")
    client.connect(HOST, PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app = QApplication(sys.argv)，每一个pyqt程序必须创建一个application对象，
    #sys.argv是命令行参数，可以通过命令启动的时候传递参数。
    mainWindow = QMainWindow()
    #生成过一个实例（对象）, mainWindow是实例（对象）的名字，可以随便起。
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)

    ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    mainWindow.show()  # 用来显示窗口

    def helloword():
        for item in ui.tableWidget.selectedItems():
            print('helloword', item)
    ui.Button_connect.clicked.connect(helloword)

    ui.tableWidget.itemDoubleClicked.connect(helloword)

    t = threading.Thread(target=start_mqtt_client, name="mqtt")
    t.start()


    sys.exit(app.exec_())#exec_()方法的作用是“进入程序的主循环直到exit()被调
