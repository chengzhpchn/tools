# -*- coding: utf-8 -*-
'''
pyuic5 *.ui > xx.py
'''
import paho.mqtt.client as mqtt
import protocol
import json, base64
import traceback

import sys
from PyQt5.QtWidgets import QApplication , QMainWindow, QTableWidgetItem, QAbstractItemView
from mainwindow import *

HOST = "10.10.40.100"
PORT = 1883
USER = "zj-r"
PASSWORD = "68689168"

CarrierCommonTopic = "ZJ/Carrier/Commom/"
SystemCommonTopic = "ZJ/System/Commom/"
CarrierStatus1Topic = "ZJ/Carrier/Status1/"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    assert (rc == 0)
    #client.subscribe(CarrierCommonTopic + '+')
    #client.subscribe(CarrierStatus1Topic + '+')#'N0001')
    #client.subscribe(SystemCommonTopic + '+')

    global ui
    vn = ui.vehicle_no.text()
    prefix = vn[:2]
    int_vn = int(vn[2:])

    for cb in [ui.CB_carrier_common,
                ui.CB_carrier_session,
                ui.CB_system_common,
                ui.CB_carrier_status1,
                ui.CB_system_lastwill,
                ui.CB_system_session,
                ui.CB_system_status,
                ui.CB_carrier_status1_2,
                ui.CB_carrier_lastwill]:
        if cb.isChecked():
            topic = cb.text()
            if "%" in topic:
                topic = topic % int_vn
            if "XX" in topic:
                topic = topic.replace("XX", prefix)
            client.subscribe(topic)


table_dict = {} # (type, class) : index: int

def on_message(client, userdata, msg):
    #print("Topic: " + msg.topic)
    global ui
    try:
        _type, _class, content = protocol.parse_header(msg.payload)

        index = table_dict.get((_type, _class), None)
        if index == None:
            index = len(table_dict)
            table_dict[(_type, _class)] = index
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

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
def start_mqtt_client():
    global client
    client.loop_stop()

    global ui

    # clear the table content
    ui.tableWidget.setRowCount(0)
    table_dict.clear()

    client.username_pw_set(ui.user.text(), ui.password.text())
    client.connect(ui.broker_ipaddr.text(), int(ui.broker_port.text()), 60)
    client.loop_start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)

    ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    ui.broker_ipaddr.setText(HOST)
    ui.broker_port.setText(str(PORT))
    ui.user.setText(USER)
    ui.password.setText(PASSWORD)

    mainWindow.show()  # 用来显示窗口

    ui.Button_connect.clicked.connect(start_mqtt_client)
    def view_content():
        item = ui.tableWidget.selectedItems()[0]
        index = item.row()

        ui.tableWidget.item(index, 0)

        topic = ui.tableWidget.item(index, 0).text()
        _type = ui.tableWidget.item(index, 2).text()
        _class = ui.tableWidget.item(index, 1).text()
        content = topic = ui.tableWidget.item(index, 3).text()

        content = content.replace(' ', '').upper()
        print(content)

        bytes = base64.b16decode(  content )
        func_name, ret = protocol.parse_content(_type, int(_class, 16), bytes)
        del ret['bytes']
        for key in ret:
            value = ret[key]
            if type(value) == type(b""):
                ret[key] = value.decode()
        print('='*8, func_name, '='*8)
        print(json.dumps(ret, indent=4, sort_keys=True))

    ui.tableWidget.itemDoubleClicked.connect(view_content)

    '''ui.tableWidget.setRowCount(1)
    datas = ["1", "0x90", "request", "06 00 44 4D 30 30 30 30 31 32 0C 00"]
    for i in range(4):
        newItem = QTableWidgetItem(datas[i])
        ui.tableWidget.setItem(0, i, newItem)'''

    app.exec_()
    client.loop_start()
