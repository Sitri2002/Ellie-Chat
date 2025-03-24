import os
import azure.cognitiveservices.speech as speechsdk
import xml.etree.ElementTree as ET 
import time

class Speech:
    def __init__(self):
        # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
        speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        self._speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        self._tree = ET.parse('data/ssml.xml')
        self._root = self._tree.getroot()
    def speak(self):
        xml_file_read = open("data/ssml.xml", "r+")
        speech_synthesis_result = self._speech_synthesizer.speak_ssml_async(xml_file_read.read()).get()
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(self._root[0][1].text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
        xml_file_read.close()
    def edit_xml(self, sentence):
        self._root[0][1].text = sentence
        self._tree.write("data/ssml.xml")