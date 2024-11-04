import time

import numpy as np

from gcadapter.gcadapter import GCAdapter, GCControllerStatus

try:
    adapter = GCAdapter()
    origin = adapter.get_origins()[0]
    origin_print = (
        origin.joystick_x - GCControllerStatus.STICK_DEFAULT_VALUE,
        origin.joystick_y - GCControllerStatus.STICK_DEFAULT_VALUE,
    )
    print(f"Origin: {origin_print}")
    adapter.start_polling()
except IOError as e:
    print(f"Failed to connect to GCAdapter: {e}")
    adapter.disconnect()
    exit(1)

ts = []
start = time.time()
while (now := time.time()) - start < 5:
    ts.append(now)
    try:
        status = adapter.get_status()[0]
        if not status.connected:
            continue
        print(
            f"sx: {(status.joystick_x - GCControllerStatus.STICK_DEFAULT_VALUE):4}, "
            f"sy: {(status.joystick_y - GCControllerStatus.STICK_DEFAULT_VALUE):4}",
            f"cx: {(status.c_stick_x - GCControllerStatus.STICK_DEFAULT_VALUE):4}, "
            f"cy: {(status.c_stick_y - GCControllerStatus.STICK_DEFAULT_VALUE):4}",
            end="\r",
            flush=True,
        )
    except IOError:
        continue

adapter.disconnect()

measured_freq = int(1 / np.mean(np.diff(ts)))
print(f"\nPoll rate: {measured_freq} Hz")
