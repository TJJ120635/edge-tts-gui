import sys
import asyncio
import sounddevice as sd
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QComboBox, QSpinBox, QCheckBox, QTextEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QEvent
import edge_tts
from io import BytesIO
from pydub import AudioSegment
import threading

class TTSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edge TTS Tool")
        self.setFixedSize(380, 200)  # 进一步减小窗口高度
        
        # 主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)  # 移除垂直间距
        layout.setContentsMargins(2, 2, 2, 2)  # 最小化边距
        
        # 设置面板
        settings_group = QGroupBox("Voice Settings")
        settings_layout = QGridLayout()
        settings_layout.setSpacing(1)  # 最小化网格间距
        
        # 语音选择
        settings_layout.addWidget(QLabel("Voice:"), 0, 0)
        self.voice_combo = QComboBox()
        self.voice_combo.setFixedHeight(20)
        settings_layout.addWidget(self.voice_combo, 0, 1)
        
        # 语速调节
        settings_layout.addWidget(QLabel("Speed (-100% ~ +100%):"), 1, 0)
        self.speed_spin = QSpinBox()
        self.speed_spin.setRange(-100, 100)
        self.speed_spin.setValue(0)
        self.speed_spin.setSingleStep(10)
        self.speed_spin.setFixedHeight(20)
        settings_layout.addWidget(self.speed_spin, 1, 1)
        
        # 音调调节
        settings_layout.addWidget(QLabel("Pitch (-50Hz ~ +50Hz):"), 2, 0)
        self.pitch_spin = QSpinBox()
        self.pitch_spin.setRange(-50, 50)
        self.pitch_spin.setValue(0)
        self.pitch_spin.setSingleStep(5)
        self.pitch_spin.setFixedHeight(20)
        settings_layout.addWidget(self.pitch_spin, 2, 1)
        
        # 窗口置顶控制
        self.stay_on_top = QCheckBox("Stay on Top")
        self.stay_on_top.setChecked(True)
        self.stay_on_top.stateChanged.connect(self.toggle_stay_on_top)
        settings_layout.addWidget(self.stay_on_top, 3, 0, 1, 2)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # 文本输入区
        self.text_edit = QTextEdit()
        self.text_edit.setFixedHeight(40)
        self.text_edit.installEventFilter(self)
        # 设置预设文本
        self.text_edit.setText("大家好啊，我是电棍，今天来点大家想看的东西。")
        layout.addWidget(self.text_edit)
        
        # 发送按钮
        self.send_button = QPushButton("Send (Enter)")
        self.send_button.setFixedHeight(20)
        self.send_button.clicked.connect(self.speak_text)
        layout.addWidget(self.send_button)
        
        # 初始化加载语音列表
        self.init_voices()
        
        # 创建事件循环
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
    def init_voices(self):
        """同步方式初始化语音列表"""
        async def load():
            voices = await edge_tts.VoicesManager.create()
            
            # 筛选中文语音并按地区排序
            zh_voices = []
            for voice in voices.voices:
                if voice['ShortName'].startswith('zh-'):
                    zh_voices.append(voice)
            
            # 按照 zh-CN, zh-HK, zh-TW 排序
            def sort_key(voice):
                locale = voice['ShortName'].split('-')[1]
                order = {'CN': 0, 'HK': 1, 'TW': 2}
                return (order.get(locale, 99), voice['ShortName'])
            
            zh_voices.sort(key=sort_key)
            
            # 添加到下拉列表，使用简短显示文本
            default_voice = None
            for voice in zh_voices:
                # 提取关键信息并格式化显示文本
                short_name = voice['ShortName']
                region = short_name.split('-')[1]  # 提取 CN/HK/TW
                name = short_name.split('-')[-1].replace('Neural', '')  # 移除 Neural 后缀
                chinese_name = voice['FriendlyName'].split()[0]  # 提取中文名的第一个词
                
                display_text = f"{region} - {name} ({chinese_name})"  # 例如: "CN - Xiaoxiao (小晓)"
                self.voice_combo.addItem(display_text, short_name)  # userData存储完整ShortName
                
                if short_name == 'zh-CN-XiaoxiaoNeural':
                    default_voice = self.voice_combo.count() - 1
            
            if default_voice is not None:
                self.voice_combo.setCurrentIndex(default_voice)
                
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(load())
        loop.close()
        
    def toggle_stay_on_top(self, state):
        """切换窗口置顶状态，使用更安全的方式"""
        try:
            # 保存当前窗口状态
            geometry = self.geometry()
            pos = self.pos()
            
            # 切换窗口标志
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, 
                             state == Qt.CheckState.Checked.value)
            
            # 恢复窗口位置和大小
            self.setGeometry(geometry)
            self.move(pos)
            
            # 重新显示窗口
            self.show()
        except Exception as e:
            print(f"Error toggling stay on top: {str(e)}")
            QMessageBox.warning(self, "Error", "Failed to toggle window state")
            # 恢复复选框状态
            self.stay_on_top.setChecked(not self.stay_on_top.isChecked())
    
    def get_voice_params(self):
        """获取当前语音参数"""
        speed = self.speed_spin.value()
        pitch = self.pitch_spin.value()
        voice = self.voice_combo.currentData()  # 使用存储的完整ShortName
        return {
            'voice': voice,
            'rate': f"{'+' if speed >= 0 else ''}{speed}%",  # 确保正数有+号
            'pitch': f"{'+' if pitch >= 0 else ''}{pitch}Hz"
        }
    
    async def generate_audio(self, text):
        """生成语音音频"""
        try:
            params = self.get_voice_params()
            print(f"TTS params: {params}")  # 打印参数信息
            
            communicator = edge_tts.Communicate(text, **params)
            audio_data = []
            
            async for chunk in communicator.stream():
                if chunk["type"] == "audio":
                    audio_data.append(chunk["data"])
            
            result = b"".join(audio_data)
            print(f"Generated audio size: {len(result)} bytes")  # 打印音频大小
            return result
            
        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            QMessageBox.warning(self, "Error", f"Failed to generate audio: {str(e)}")
            return None
    
    def play_audio(self, audio_data):
        """播放音频"""
        try:
            # 将 MP3 字节数据转换为 AudioSegment
            audio_segment = AudioSegment.from_mp3(BytesIO(audio_data))
            
            # 转换为numpy数组
            samples = np.array(audio_segment.get_array_of_samples())
            
            # 打印调试信息
            print(f"Audio format: {audio_segment.channels} channels, {audio_segment.frame_rate} Hz")
            print(f"Audio duration: {len(audio_segment)} ms")
            print(f"Samples shape: {samples.shape}")
            
            # 播放音频
            sd.play(samples, audio_segment.frame_rate)
            sd.wait()
            
        except Exception as e:
            print(f"Error playing audio: {str(e)}")
            QMessageBox.warning(self, "Error", f"Failed to play audio: {str(e)}")
    
    def speak_text(self):
        """处理文本到语音的转换和播放"""
        text = self.text_edit.toPlainText()
        if not text:
            return
            
        async def process_audio():
            audio_data = await self.generate_audio(text)
            if audio_data:
                self.play_audio(audio_data)
        
        # 使用已存在的事件循环而不是创建新的
        future = asyncio.run_coroutine_threadsafe(process_audio(), self.loop)
        try:
            future.result()  # 等待结果
            self.text_edit.clear()
        except Exception as e:
            print(f"Error in speak_text: {str(e)}")
            QMessageBox.warning(self, "Error", f"Failed to process audio: {str(e)}")

    def eventFilter(self, obj, event):
        """事件过滤器，用于处理文本框的Enter键事件"""
        if obj is self.text_edit and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return:
                # Shift+Enter 输入换行，普通 Enter 发送
                if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                    return False
                self.speak_text()
                return True
        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        """窗口关闭时清理事件循环"""
        self.loop.close()
        super().closeEvent(event)

def main():
    # 预加载一些模块
    import asyncio
    import edge_tts
    
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')  # 使用 Fusion 样式，启动更快
    
    window = TTSWindow()
    # 使用窗口标志来禁用帮助按钮
    # window.setWindowFlags(window.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    
    # 创建事件循环线程
    def run_event_loop():
        window.loop.run_forever()
    
    thread = threading.Thread(target=run_event_loop, daemon=True)
    thread.start()
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()