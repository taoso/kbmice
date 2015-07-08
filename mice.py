# -*- encoding: utf-8 -*-

from evdev import InputDevice, ecodes, UInput
import uinput

ui = uinput.Device([
    uinput.BTN_LEFT,
    uinput.BTN_RIGHT,
    uinput.REL_X,
    uinput.REL_Y,
])

dev_path = '/dev/input/by-path/pci-0000:00:1d.0-usb-0:1.5.1:1.0-event-kbd'
dev = InputDevice(dev_path)

is_open = False
d = 5
for event in dev.read_loop():
    if event.code == ecodes.KEY_LEFTSHIFT:
        is_open = event.value > 0

    if event.code == ecodes.KEY_LEFTCTRL:
        if event.value == 1:
            d = 10
        else:
            d = 5

    if not is_open:
        continue

    if event.code == ecodes.KEY_PAGEDOWN:
        ui.emit(uinput.BTN_LEFT, event.value > 0)
    elif event.code == ecodes.KEY_END:
        ui.emit(uinput.BTN_RIGHT, event.value > 0)

    x, y = 0, 0
    if event.code == ecodes.KEY_UP:
        y = -d
    elif event.code == ecodes.KEY_DOWN:
        y = d
    elif event.code == ecodes.KEY_RIGHT:
        x = d
    elif event.code == ecodes.KEY_LEFT:
        x = -d

    if x != 0:
        ui.emit(uinput.REL_X, x)
    elif y != 0:
        ui.emit(uinput.REL_Y, y)
