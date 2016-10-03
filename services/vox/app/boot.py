import os
import time
from pocketsphinx import LiveSpeech, get_model_path, Decoder
import paho.mqtt.client as mqtt


path_lm = '/Users/andres/projects/turing/services/vox/app/detection_model/base.lm'
path_dict = '/Users/andres/projects/turing/services/vox/app/detection_model/base.dic'

model_path = get_model_path()

# speech = LiveSpeech(
#     verbose=False,
#     sampling_rate=16000,
#     buffer_size=1024,
#     no_search=False,
#     full_utt=False,
#     hmm=os.path.join(model_path, 'en-us'),
#     # lm=os.path.join(model_path, 'en-us.lm.bin'),
#     lm=path_lm,
#     # dic=os.path.join(model_path, 'cmudict-en-us.dict')
#     dic=path_dict,
# )
#
# for phrase in speech:
#     print('Phrase:')
#     print(phrase)
#     print(phrase.segments(detailed=False))
#
#
# # https://pypi.python.org/pypi/pocketsphinx





# base.list - provides sensitivity thresholds for continuous listening
# base.vocab - word/sentence list for uploading into language generator
# base.lm - language model file
# base.dic - word dictionary file that scopes pronunciation

_comm_client = mqtt.Client()

def _on_connect(client, userdata, flags, rc):
    print "New connection: " + str(rc)

    _comm_client.subscribe('system', 0)


def _on_message(client, userdata, msg):
    print 'GOT MESSAGE (qos=' + str(msg.qos) + ', topic=' + str(msg.topic) + '): ' + str(msg.payload)

    _face.blink()

def _on_publish(mosq, obj, mid):
    print 'mid: ' + str(mid)

def _on_subscribe(mosq, obj, mid, granted_qos):
    print 'Subscribed: ' + str(mid) + ' ' + str(granted_qos)

def _on_log(mosq, obj, level, string):
    print 'Log: ' + str(string)



_comm_client.on_message = _on_message
_comm_client.on_connect = _on_connect
_comm_client.on_publish = _on_publish
_comm_client.on_subscribe = _on_subscribe

try:
    _comm_client.connect('localhost', 1883, 60)
    print('Connected to centralstation')

except Exception, e:
    print('Couldn\'t connect to centralstation. Retrying in 1 second.')

    time.sleep(1)
    self._connect_to_comms()


import sys, os
import subprocess
from pocketsphinx import *
import pyaudio

modeldir = '/usr/local/share/pocketsphinx/model/'

# Create a decoder with certain model
config = Decoder.default_config()

# Directory containing acoustic model files
config.set_string('-hmm', os.path.join(modeldir, 'en-us/en-us'))
config.set_string('-dict', path_dict)
config.set_string('-kws', 'detection_model/base.list')
config.set_string('-logfn', '/dev/null')

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

# Process audio chunk by chunk. On keyword detected perform action and restart search
decoder = Decoder(config)
decoder.start_utt()

while True:
    buf = stream.read(1024)
    decoder.process_raw(buf, False, False)

    if decoder.hyp() != None:
        hypothesis = decoder.hyp()

        print ('Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", hypothesis.prob)

        decoder.end_utt()
        stream.stop_stream()

        _comm_client.loop()

        if str(hypothesis.hypstr).lower().strip() == 'swell':
            try:
                _comm_client.publish('vox', 'swell')
                output = subprocess.check_output('afplay audio/r2d2.wav', shell=True)

            except Exception:
                pass
        elif str(hypothesis.hypstr).lower().strip() == 'dolly':
            try:
                _comm_client.publish('vox', 'dolly')
                output = subprocess.check_output('afplay audio/bb8.mp3', shell=True)

            except Exception:
                pass
        else:
            print hypothesis.hypstr.lower()

        # print "restarting search"
        stream.start_stream()
        decoder.start_utt()
