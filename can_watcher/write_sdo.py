import struct, sys
from canopen.sdo import SdoClient
from canopen.sdo import constants as const
import canopen

def download_data(sc, index, subindex, data):
    size = len(data)
    command = const.REQUEST_DOWNLOAD | const.EXPEDITED | const.SIZE_SPECIFIED
    command |= (4 - size) << 2
    header = const.SDO_STRUCT.pack(command, index, subindex)

    response = sc.request_response(header + data)

    resp_cmd, Index, SubIndex, ErrCode = struct.unpack_from("<BHBL", response, 0)
    assert resp_cmd == 0x60
    assert Index == index
    assert SubIndex == subindex
    return ErrCode

object_dictionary_table = [
    #index, subindex, value
    (0x3000, 0, bytearray([0x20])),#Node Id: new node id, like 0x21 = 0x20 +1
                                   #Note: Result Value = Set Value + 0x01, Here we input the Set Value
    (0x3001, 0, bytearray([0x05])),#Baud Rate: 500K
    (0x3003, 1, bytearray([0x00])),#Auto Baud Detection: disable
    (0x6003, 0, bytearray([0xd0, 0x07, 0x00, 0x00])),#Preset value: 2000
    (0x6200, 0, bytearray([0x32, 0x00])),#Cyclic Timer: 50ms
    (0x1010, 1, bytearray("save")),#save
]


if __name__ == "__main__":
    network = canopen.Network()
    network.connect(bustype='socketcan', channel="can1", bitrate=500000)
    node_id = 0x20
    if len(sys.argv) > 1:
        node_id = int(sys.argv[1])
    sc = SdoClient(0x600 + node_id, 0x580 + node_id, None)
    sc.network = network
    sc.RESPONSE_TIMEOUT = 10
    network.subscribe(sc.tx_cobid, sc.on_response)

    for index, subindex, data in object_dictionary_table:
        ErrCode = download_data(sc, index, subindex, data)
        print "%x|%x -> %d" % (index, subindex, ErrCode)