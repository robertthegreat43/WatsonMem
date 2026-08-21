import os

import matplotlib
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import torch
import torch.utils.data
import librosa

device = "cuda" if torch.cuda.is_available() else "cpu"

matplotlib.use("TkAgg")


class Audio:
    def __init__(self):
        self.filename = ""
        self.input_file = ""
        self.duration = 0.0

    def recording(self, duration):
        self.duration = duration

        freq = 44100
        seconds = duration

        print("recording")

        recording = sd.rec(
            int(seconds * freq),
            samplerate=freq,
            channels=1
        )

        sd.wait()

        write("output.wav", freq, recording)

        wv.write(
            "output.wav",
            recording,
            freq,
            sampwidth=2
        )

        wav_file = wv.read("output.wav")
        print(wav_file.data)

    def file_sound(self):
        sound_file = input("Enter the file name: ")

        filename = os.path.join(
            r"C:\Users\Robert\Documents\soundfile",
            sound_file
        )

        print(filename)

        try:
            with open(filename, "rb") as f:
                contents = f.read()

            contents_as_int = np.array(list(contents), dtype=np.uint8)

            print(contents_as_int)

            write("Recording.wav", 44100, contents_as_int)

            wv.write(
                "Recording.wav",
                contents_as_int,
                44100,
                sampwidth=1
            )

            wav_file = wv.read("Recording.wav")
            print(wav_file.data)

        except IOError as e:
            print("error could not read " + filename)
            print(e)


