# encoding: utf-8
import paho.mqtt.client as mqtt
import protocol
import json

HOST = "10.10.40.100"
PORT = 1883

CarrierCommonTopic = "ZJ/Carrier/Commom/"
SystemCommonTopic = "ZJ/System/Commom/"
CarrierStatus1Topic = "ZJ/Carrier/Status1/"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    assert (rc == 0)
    client.subscribe(CarrierCommonTopic + '+')
    client.subscribe(CarrierStatus1Topic + 'N0031')
    client.subscribe(SystemCommonTopic + '+')


def on_message(client, userdata, msg):
    print("Topic: " + msg.topic)
    ret = protocol.parse_payload(msg.payload)
    print(json.dumps(ret, indent=3))


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("zj-r", "68689168")
    client.connect(HOST, PORT, 60)
    client.loop_forever()