import can

def init_cobid():
    ExIOBoard_A = [0x300 + 0xB * i + 0x30 for i in range(12)]
    ExIOBoard_B = [0x300 + 0xB * i + 0x31 for i in range(12)]
    LiftCtrlBoard = (0x492, 0x497, 0x498)
    MotionCtrlBoard = (0x1C3, 0x4C3, 0x3C3, 0x483, 0x484, 0x485, 0x486, 0x487, 0x488, 0x489, 0x491, 0x493, 0x494, 0x402)
    CurtisDriver = (0x20B, 0x203, 0x207, 0x213, 0x217)
    WireDrawEncoder = (0x1A0, )

    map = {
        "ExIOBoard_A" : ExIOBoard_A,
        "ExIOBoard_B": ExIOBoard_B,
        "LiftCtrlBoard" : LiftCtrlBoard,
        "MotionCtrlBoard" : MotionCtrlBoard,
        "CurtisDriver" : CurtisDriver,
        "WireDrawEncoder" : WireDrawEncoder
    }

    ret = {}
    for key in map:
        for v in map[key]:
            ret[v] = key
    return ret

cobid_map = init_cobid()
device_set = set([])

class AGVChecker(can.Printer):
    def on_message_received(self, msg):
        device = cobid_map.get(msg.arbitration_id, None)
        if device:
            if device not in device_set:
                print "%s active for cob_id: %x" % (device, msg.arbitration_id)
                device_set.add(device)



bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)

notifier = can.Notifier(bus, [ AGVChecker()])

import time
time.sleep(30)
notifier.stop()

print "detected devices:"
for device in device_set:
    print ' '*3, device

print 'waiting for exit......'
time.sleep(6)
