import can

bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)

# iterate over received messages
#for msg in bus:
#    print("{X}: {}".format(msg.arbitration_id, msg.data))

# or use an asynchronous notifier
notifier = can.Notifier(bus, [ can.Logger("recorded.asc"), can.Printer()])

import time
time.sleep(1000*10)
