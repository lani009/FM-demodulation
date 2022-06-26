from queue import Queue
from threading import Thread
from time import sleep
import time
import numpy as np
from rtlsdr import RtlSdr
from scipy import signal
import pyaudio

raw_sample_queue = Queue()
audio_queue = Queue()
sdr = RtlSdr()


F_station = int(95.9e6)  # 95.9 MHz   MBC 표준 FM
F_offset = 250000
Fc = F_station - F_offset
Fs = int(2.4e6)

f_bw = 200000
dec_rate = int(Fs / f_bw)
Fs_y = f_bw
d = Fs_y * 75e-6
x = np.exp(-1/d)
b = [1-x]
a = [1, -x]

audio_freq = 44100.0
dec_audio = int(Fs_y/audio_freq)
Fs_audio = Fs_y / dec_audio

duration = 1
fc1 = np.exp(-1.0j*2.0*np.pi * F_offset*np.arange(0, duration, 1/Fs))


p = pyaudio.PyAudio()


def main():
    sdr.set_sample_rate(Fs)
    sdr.set_center_freq(Fc)
    sdr.set_freq_correction(66)
    sdr.set_gain(33.8)
    t = Thread(target=sampling)
    t.start()
    time.sleep(2)
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=int(Fs_audio),
                    output=True,
                    stream_callback=hi,
                    frames_per_buffer=int(Fs_y / dec_audio))
    stream.start_stream()

    time.sleep(1000)


    # stream.stop_stream()
    # stream.close()

    # p.terminate()

def sampling():
    sdr.read_samples_async(sampling_cb, int(duration * Fs))

def sampling_cb(values, context):
    x1 = values
    fc1 = np.exp(-1.0j*2.0*np.pi * F_offset*np.arange(0, duration, 1/Fs))
    x2 = x1 * fc1

    
    x4 = signal.decimate(x2, dec_rate)
    
    y5 = x4[1:] * np.conj(x4[:-1])
    x5 = np.angle(y5)

    x6 = signal.lfilter(b, a, x5)

    x7 = signal.decimate(x6, dec_audio)

    x7 *= 5000

    audio_queue.put(x7.astype('int16').tobytes())

def hi(in_data, frame_count, time_info, flag):
    return (audio_queue.get(block=True), pyaudio.paContinue)

if __name__ == '__main__':
    main()
