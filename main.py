import sys
import sounddevice as sd
import numpy as np
import subprocess
import time

# 音量觸發的閥值 (可調整)
THRESHOLD = 340

# 指定要播放的影片或音訊檔案
MEDIA_FILE = './dajiangdahaijiangdahai.mp4'  # 改成你的檔案名稱

# 追蹤最大的音量
highest_volume = 0.0
playing_media = False

# 頻率偵測函數
def detect_frequency(indata, samplerate):
    fft_data = np.abs(np.fft.rfft(indata[:, 0]))
    freq = np.fft.rfftfreq(len(indata), d=1./samplerate)
    peak_freq = freq[np.argmax(fft_data)]
    return peak_freq

# 偵測到聲音後的處理函數
def audio_callback(indata, frames, time, status):
    global highest_volume, playing_media

    if playing_media:
        return

    volume_norm = np.linalg.norm(indata) * 10

    # 更新最高音量紀錄
    if volume_norm > highest_volume:
        highest_volume = volume_norm

    samplerate = 44100  # 根據你的sounddevice設定的取樣率調整
    peak_freq = detect_frequency(indata, samplerate)

    print("\033[H\033[J", end='')
    print(f"目前音量: {volume_norm:6.2f}, 最高音量: {highest_volume:6.2f}")
    print(f"目前頻率: {peak_freq:8.2f} Hz")

    if volume_norm >= THRESHOLD and peak_freq > 100 and peak_freq < 150 and not playing_media:
        print(f"音量超過閥值 ({THRESHOLD})！目前音量: {volume_norm:.2f}, 頻率: {peak_freq:.2f} Hz，啟動大江大海江大海！")
        playing_media = True
        subprocess.Popen(['xdg-open', MEDIA_FILE]).wait()
        playing_media = False
        sys.exit(0)

# 主程式邏輯
if __name__ == "__main__":
    print("開始監聽麥克風... 音量閥值:", THRESHOLD)
    with sd.InputStream(callback=audio_callback):
        while True:
            time.sleep(1000)