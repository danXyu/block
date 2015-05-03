## Library Imports
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import commands
import sys
import time

## MonkeyRunner Device Creation and Run
device = MonkeyRunner.waitForConnection(10)
device.press('KEYCODE_DPAD_LEFT')
