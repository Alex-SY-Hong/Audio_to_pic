import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
# from pyguiadapter.adapter import GUIAdapter
# from matplotlib.pyplot import savefig

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def record_audio():
    print("请按下回车键开始录音...")
    input()
    print("开始录音...")

    # 录音参数
    duration = 5  # 录音时长，单位秒
    fs = 44100  # 采样率

    # 录音
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  # 等待录音结束

    print("录音结束，请按下回车键结束程序...")
    input()

    return recording.flatten(), fs

def compute_fft(signal, fs):
    # 计算FFT
    n = len(signal)
    yf = np.fft.rfft(signal, n)
    xf = np.linspace(0.0, fs / 2, n // 2 + 1)

    return xf, yf

def plot_spectrum(xf, yf, filename):
    # 可视化20至20000Hz的频谱
    plt.figure(figsize=(14, 6))
    plt.plot(xf, 2.0/len(yf) * np.abs(yf[:len(xf)]))
    plt.xlim(20, 1074)
    plt.title('频谱图 (20Hz - 1074Hz)')
    plt.xlabel('频率 (Hz)')
    plt.ylabel('幅度')
    plt.grid()
    plt.show()
    plt.savefig(filename)


def main():
    # 录音
    recording, fs = record_audio()

    # FFT计算
    xf, yf = compute_fft(recording, fs)

    # 获取用户输入的文件名
    file = input("请输入保存图片的文件名")

    # 可视化频谱
    plot_spectrum(xf, yf, file)

if __name__ == "__main__":
    main()
