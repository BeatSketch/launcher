from util.ipc.decode import BeatSketchInstanceDataDecoder


com = BeatSketchInstanceDataDecoder()

while True:
    print(com.get_data())
