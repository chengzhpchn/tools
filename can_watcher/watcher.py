import can

bus0 = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)
bus1 = can.interface.Bus(bustype='socketcan', channel='can1', bitrate=500000)

# or use an asynchronous notifier
notifier0 = can.Notifier(bus0, [ can.Logger("recorded_can0.asc")])
notifier1 = can.Notifier(bus1, [ can.Logger("recorded_can1.asc")])

import time
time.sleep(1000*10)

