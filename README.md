# Audio_to_pic
实现语音可视化的python程序。为复旦大学第二附属学校的AI课程设计，原作者洪善渊，作为复旦大学课程“计算思维与信息素养”的一部分。设计过程中使用智谱清言辅助。

## 如何使用
假设你已经下载了conda
1. 使用`cd`移动到目标目录
2. `git clone`这个repo
   ```
   $ git clone https://github.com/Alex-SY-Hong/Audio_to_pic
   $ cd Audio_to_pic
   ```
3. 克隆依赖
   ```
   $ conda env -f environment.yml
   ```
4. 直接运行python源文件
5. 如果需要单文件版本，命令行运行
   ```
   $ pyinstaller --onefile GUI-wave.py
   ```
   或者
   ```
   $ pyinstaller --onefile GUI-wave.py
   ```
