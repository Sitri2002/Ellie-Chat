import faster_whisper as whisper
import torch
import warnings
import speech_recognition as sr
from queue import Queue
from datetime import datetime, timedelta
from time import sleep
import numpy as np
import os
import chat
import time
warnings.simplefilter(action='ignore', category=FutureWarning)

transcription = ['']

class STT:
    def __init__(self):
        self._transcriber = transcriber(model="large-v3")
        self._recorder = recorder(energy_threshold=1300, record_time= 1, cutoff_time= 2, transcribe_model=self._transcriber._model)
        print("Recording...")
        
class transcriber:
    def __init__(self, model):
        if (torch.cuda.is_available()):
            torch.cuda.init()
            device = "cuda"
            print("Using GPU for Whisper")
        else:
            device = "cpu"
            print("Using CPU for Whisper")
        self._model = whisper.WhisperModel(model, device = device, compute_type= "float16")

class recorder():
    def __init__(self, energy_threshold, record_time, cutoff_time, transcribe_model):
        self._recorder = sr.Recognizer()
        self._recorder.dynamic_energy_threshold = False
        self._recorder.energy_threshold = energy_threshold
        self._source = sr.Microphone(sample_rate=16000)
        self._audioThread = Queue()
        self._record_time = record_time
        self.phrase_time = None
        self._cutoff_time = cutoff_time
        self._model = transcribe_model
        with self._source:
            self._recorder.adjust_for_ambient_noise(self._source)

    def record_callback(self,_, audio:sr.AudioData) -> None:
        if chat.AI_SPEAKING:
            return
        data = audio.get_raw_data()
        self._audioThread.put(data)

    def record(self):
        log = open("data/user_input.txt", "w+", encoding='cp1252')
        self._recorder.listen_in_background(self._source, self.record_callback, self._record_time)
        while True:
            try:
                now = datetime.now()
                if not self._audioThread.empty():
                    phrase_complete = False
                    if self.phrase_time and now - self.phrase_time > timedelta(seconds=self._cutoff_time):
                        phrase_complete = True
                    self.phrase_time = now
                    audio_data = b''.join(self._audioThread.queue)
                    self._audioThread.queue.clear()
                    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                    segments, _ = self._model.transcribe(audio= audio_np, language= 'en', no_speech_threshold= 0.8)
                    text = ""
                    for segment in segments:
                        text += segment.text
                    # text = text.replace("Thank you.", "") # silence hallucination, bandaid fix, idk
                    if phrase_complete:
                        transcription.append(text)
                    else:
                        transcription[-1] = text
                    # os.system('cls' if os.name=='nt' else 'clear')
                    # for line in transcription:
                    #     print(line)
                    if os.stat("data/user_input.txt").st_size == 0:
                        log.seek(0)
                    log.write(transcription[-1])
                    log.write(" ")
                    log.flush()
                    chat.USER_RESPONDED_TO = False
                else:
                    sleep(0.05)
            except KeyboardInterrupt:
                break
        log.close()