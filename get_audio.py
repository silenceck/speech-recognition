#!/usr/bin/python
# -*- coding: utf-8 -*-
import pyaudio
import wave
import time
input_filename = 'input.wav'
input_filepath = './'
in_path = input_filepath + input_filename

def get_audio(filepath):
    #prompt_information = str(input('是否开始录音?  (Y/N)\n'))
    #time.sleep(1)
    #if prompt_information == str('Y'):
    CHUNK = 256
    FORMAT = pyaudio.paInt16
    CHANNELS = 1                # 声道数
    RATE = 11025                # 采样率
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = filepath
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print('*'*10)
    frames = []
    for i in range(0, int(RATE / CHUNK *RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print('*'*10, '录音结束\n')
    stream.stop_stream()
    stream.close()
    p.terminate()
    print frames
    wf = wave.open(WAVE_OUTPUT_FILENAME,'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    '''
    elif prompt_information == str('N'):
        exit()
    else:
        print('无效输入,请重新选择')
        get_audio(filepath)
    '''
if __name__ == '__main__':
    get_audio(in_path)
