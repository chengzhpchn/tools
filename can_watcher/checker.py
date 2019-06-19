# -*- coding: utf-8 -*-
import canopen
import time

can0_nodes = {
    0x14 : "拉线编码器",
    0x01 : "A9",
    0x03 : "A9?",
    0x11 : "A9?",
    0x42 : "驱B",
    0x43 : "驱A"
}

can1_nodes = {
    0x01 : "A9",
    0x30 : "扩A",
    0x31 : "扩B"
}

def detect(chan):
    network = canopen.Network()

    network.connect(bustype='socketcan', channel=chan, bitrate=500000)
    try:
        network.scanner.search()

        time.sleep(1)
        #for node_id in network.scanner.nodes:
        #    print("Found node %d" % node_id)
        return network.scanner.nodes
    finally:
        network.disconnect()
        
if __name__ == "__main__":
    _can0_nodes = detect('can0')
    for node_id in _can0_nodes:
        node_name = can0_nodes.get(node_id, "未知设备")
        print( '检测到can0设备: id=0x%02x, name=%s' % (node_id, node_name) )
    print('='*32)
    _can1_nodes = detect('can1')
    for node_id in _can1_nodes:
        node_name = can1_nodes.get(node_id, "未知设备")
        print( '检测到can1设备: id=0x%02x, name=%s' % (node_id, node_name) )