## Library Imports
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import commands
import sys
import time

## MonkeyRunner Device Creation
device = MonkeyRunner.waitForConnection(10)

