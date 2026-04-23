import ipc

instance = ipc.BeatSketchInstance()
instance.await_launch()
instance.write("MSG")
print("STDOUT", instance.read())
instance.write("Hello")
print("STDOUT", instance.read())
instance.write("WORLD")
print("STDOUT", instance.read())

instance = None

import time
time.sleep(2)
