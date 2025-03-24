from openai import OpenAI, OpenAIError
import os
from datetime import datetime, timedelta
import filter
import tts
import GPT_model as model

RESPOND_BUFFER = 3
NO_OUTPUT_BUFFER = 90
USER_RESPONDED_TO = True
AI_SPEAKING = False

class ChatAgent:
    def __init__(self):
        self._client = model.Model()
        self._tts = tts.Speech()
    
    def run(self):
        global USER_RESPONDED_TO
        global AI_SPEAKING
        last_spoken = datetime.now()
        while True:
            try:
                current_time = datetime.now()
                last_edit = datetime.fromtimestamp(os.path.getmtime('data/user_input.txt'))
                result = ""
                if current_time - last_edit > timedelta(seconds = RESPOND_BUFFER) and not USER_RESPONDED_TO:
                    AI_SPEAKING = True
                    result = self._client.respond(last_edit)
                    self._tts.edit_xml(result)
                    self._tts.speak()
                    USER_RESPONDED_TO = True
                    last_spoken = datetime.now()
                    AI_SPEAKING = False
                if current_time - last_spoken > timedelta(seconds = NO_OUTPUT_BUFFER):
                    AI_SPEAKING = True
                    result = self._client.respond(last_edit)
                    self._tts.edit_xml(result)
                    self._tts.speak()
                    last_spoken = datetime.now()
                    AI_SPEAKING = False
            except KeyboardInterrupt:
                break