# Edge TTS GUI

基于 [edge-tts](https://github.com/rany2/edge-tts) 的 Python GUI 工具，提供简单易用的文本转语音界面。

## 功能特点

- 📝 简洁的图形界面
- 🎤 支持多种中文语音（大陆、香港、台湾）
- ⚙️ 可调节语速和音调
- 📌 窗口置顶功能
- ⌨️ 快捷键支持（Enter发送，Shift+Enter换行）

## 使用方式

### 直接运行（推荐）
1. 从 [Releases](https://github.com/TJJ120635/edge-tts-gui/releases) 下载最新版本
2. 解压后双击运行 `edge-tts-gui.exe`

### 从源码运行
1. 克隆仓库
```bash
git clone https://github.com/TJJ120635/edge-tts-gui.git
cd edge-tts-gui
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行程序
```bash
python main.py
```

### 手动构建
```bash
# 安装打包工具
pip install pyinstaller

# 构建程序
pyinstaller build.spec --clean
```

## 参数说明

### 语音设置
- Voice: 选择语音音色
  - CN - Xiaoxiao (小晓)：标准女声
  - CN - Yunxi (云溪)：标准男声
  - 等更多音色...
- Speed: 语速调节范围 -100% ~ +100%
- Pitch: 音调调节范围 -50Hz ~ +50Hz

### 快捷键
- Enter: 发送文本
- Shift + Enter: 换行
- Stay on Top: 窗口置顶开关

## 依赖版本

主要依赖包版本要求：
```
edge-tts >= 6.1.5
PyQt6 >= 6.4.0
sounddevice >= 0.4.6
numpy >= 1.23.0
pydub >= 0.25.1
```

## 已知问题

- 首次运行可能需要联网下载语音模型
- 部分系统可能需要安装额外的音频解码器

## 贡献代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

4. **创建首个 Release**

项目推送完成后，可以创建一个 Release：

- 在 GitHub 仓库页面点击 "Releases"
- 点击 "Create a new release"
- 标签版本填写：`v1.0.0`
- 标题可以写：`Edge TTS GUI Initial Release`
- 描述中可以写：
  ```
  首个版本发布，包含以下功能：
  - 支持多种中文语音（大陆、香港、台湾）
  - 可调节语速和音调
  - 窗口置顶功能
  - 快捷键支持
  ```
- 如果有编译好的 exe 文件，可以添加为 release 附件

5. **更新 README 中的链接**

确保 README.md 中的链接都指向你的仓库：

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件