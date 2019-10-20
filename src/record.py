from pynput import keyboard
import time
import pyaudio
import wave
import sched
import sys

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
frames = []

def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (in_data, pyaudio.paContinue)

class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None
        self.wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        self.wf.setnchannels(CHANNELS)
        self.wf.setsampwidth(p.get_sample_size(FORMAT))
        self.wf.setframerate(RATE)
    def on_press(self, key):
        if key == keyboard.Key.space:
            self.key_pressed = True
        return True

    def on_release(self, key):
        if key == keyboard.Key.space:
            self.key_pressed = False
        return True


listener = MyListener()
listener.start()
started = False
stream = None

def recorder():
    global started, p, stream, frames, event

    if listener.key_pressed and not started:
        # Start the recording
        try:
            stream = p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK,
                             stream_callback = callback)
            print("Stream active:", stream.is_active())
            started = True
            print("start Stream")
            event = task.enter(0.1, 1, recorder, ())
        except:
            raise

    elif not listener.key_pressed and started:
        print("Stop recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        listener.wf.writeframes(b''.join(frames))
        listener.wf.close()
        print("You should have a wav file in the current directory")
        
    else: # Reschedule the recorder function in 100 ms.
        event = task.enter(0.1, 1, recorder, ())


print("Press and hold the spacebar to begin recording")
print("Release the spacebar key to end recording")
task = sched.scheduler(time.time, time.sleep)
event = task.enter(0.1, 1, recorder, ())
task.run()