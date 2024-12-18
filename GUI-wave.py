import tkinter as tk
from tkinter import simpledialog, Text, Frame, Label
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fs = 44100  # 采样率
channels = 2  # 声道数
is_recording = False  # 录音状态标志
audio_data = None  # 存储录音数据
is_readme_visible = False  # readme 文本框是否可见


# 红点闪烁频率
blink_frequency = 500  # 5 Hz 对应 200 ms 间隔

# 红点闪烁函数
def blink_dot():
    if is_recording:
        dot_label.config(bg="red")
        root.after(blink_frequency, unblink_dot)
    else:
        dot_label.config(bg="white")


def unblink_dot():
    if is_recording:
        dot_label.config(bg="white")
        root.after(blink_frequency, blink_dot)


#def check_audio_permission():
#    try:
#         # 尝试初始化一个短暂的录音来检查权限
#        sd.default.samplerate = 44100
#        sd.default.channels = 2
#        sd.rec(int(1), samplerate=sd.default.samplerate, channels=sd.default.channels, dtype='int16')
#        sd.wait()  # 等待录音完成
#        check_audio_label.config('')
#        # print("音频设备访问权限正常。")
#    except PermissionError as e:
#        check_audio_label.config(f"权限错误: {e}")
#       # print(f"权限错误: {e}")
#    except sd.PortAudioError as e:
#       check_audio_label.config(f"PortAudio错误: {e}")
#    except Exception as e:
#       check_audio_label.config(f"未知错误: {e}")

# 录音函数
def toggle_record():
    global is_recording, audio_data, fs, status_label

    filename = ''
    # 录音
    if not is_recording:
        is_recording = True

        #try:
        audio_data = sd.rec(int(fs * 5), samplerate=fs, channels=channels, dtype='int16')
        status_label.config(text="录音中")
        blink_dot()
        #except Exception as e:
        # status_label.config(text=f"出现错误:{str(e)}导致录音失败，请检查系统权限设置")
        #    is_recording = False
        #    dot_label.config(bg="white")

        #finally:
        #    pass
    else:
        sd.wait()  # 等待录音完成
        is_recording = False
        status_label.config(text="录音结束")
        dot_label.config(bg="white")

        # 弹出输入框让用户输入文件名
        filename = simpledialog.askstring("输入", "请输入文件名:")

    if filename:
        # 调用output函数
        output(audio_data.flatten(), fs, filename)

    # 重置状态
    status_label.config(text="未开始录音")
    dot_label.config(bg="white")

# 数据处理
def compute_fft(signal, f):
   # 计算FFT
     n = len(signal)
     yf = np.fft.rfft(signal, n)
     xf = np.linspace(0.0, f / 2, n // 2 + 1)
     return xf, yf


def plot_spectrum(xf, yf, filename):
    # 可视化频谱
    plt.figure(figsize=(14, 6))
    plt.plot(xf, 2.0 / len(yf) * np.abs(yf[:len(xf)]))
    plt.xlim(20, 1074)
    plt.title('“' + filename + '”的可视化')
    plt.xlabel('频率 (Hz)')
    plt.ylabel('强度')
    plt.grid()
    plt.savefig(filename)
    plt.show()


def output(signal, f, filename):
    xf, yf = compute_fft(signal, f)
    plot_spectrum(xf, yf, filename)


def toggle_readme():
    global is_readme_visible

    if not is_readme_visible:
        readme_text.pack(pady = 10)
        is_readme_visible = True
    else:
        readme_text.pack_forget()
        is_readme_visible = False


# 创建主窗口
root = tk.Tk()
root.title("声音可视化")
root.geometry('600x300')


# 创建一个框架用于放置录音按钮
button_frame = Frame(root)
button_frame.pack(side=tk.LEFT, padx=10)

# 创建按钮并绑定点击事件
record_button = tk.Button(root, text="开始/停止录音", command=toggle_record)
record_button.pack(pady=20)

# 创建状态标签
status_label = tk.Label(root, text="未开始录音")
status_label.pack(pady=10)


# 创建红点标签
dot_label = tk.Label(root, width=2, height=1, bg="white")
dot_label.pack(pady=10)


# 创建一个框架用于放置README文本
readme_frame = Frame(root)
readme_frame.pack(side=tk.RIGHT, padx=10)


# 创建README文本小部件
readme_text = Text(root, height=10, width=50)
readme_text.insert('end', "本程序的作用是将语音可视化。\
\n 请点击“录音/停止录音”按钮开始录音，再次点击停止录音。\
结束后会弹出一个输入框，请输入文件名，程序会保存可视化的结果。\
\n 技术说明：本程序的原理是对声音信号进行FFT运算，从而把信号从\
时域转换到频域，然后截断C6以上的高音绘制出信号的频谱图。\
所以如果高声尖叫或者唱歌，可能效果不佳。" )
readme_text.pack_forget()  # 初始状态隐藏文本小部件


# 创建README按钮并绑定点击事件
readme_button = tk.Button(root, text="使用说明", command=toggle_readme)
readme_button.pack(pady=20)


# 创建一个检查权限的小组件
# check_audio_label = Label(root, height=1, width=50, text='')
# check_audio_label.pack(pady = 10)
# check_audio_permission()


# 运行主循环
root.mainloop()
