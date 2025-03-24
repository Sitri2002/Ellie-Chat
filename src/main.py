import stt
import chat
from threading import Thread

listener = stt.STT()
agent = chat.ChatAgent()

def listen():
    listener._recorder.record()
def speak():
    agent.run()

Thread(target= listen).start()
Thread(target= speak).start()