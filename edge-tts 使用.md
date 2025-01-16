调用 Edge 浏览器的文本朗读有关 API 实现 TTS，无需本地部署模型
https://github.com/rany2/edge-tts/

安装：
```batch
conda activate chat
pip install edge-tts
```
命令行使用：
```batch
# 参数列表
usage: edge-tts [-h] [-t TEXT] [-f FILE] [-v VOICE] [-l]
                [--rate RATE] [--volume VOLUME] [--pitch PITCH]
                [--words-in-cue WORDS_IN_CUE] [--write-media WRITE_MEDIA] 
                [--write-subtitles WRITE_SUBTITLES][--proxy PROXY]

# 保存成 mp3 格式，以及字幕文件
edge-tts --text "Hello, world!" --write-media hello.mp3 --write-subtitles hello.vtt

# 如果想直接播放刚刚生成的音频，需要安装命令行播放工具 mpv，mac 安装 brew install mpv
edge-playback --text "Hello, world!"

# 查看可用的声音角色列表，推荐 zh-CN-XiaoxiaoNeural 女性，声音好听，也有部分角色是方言
edge-tts --list-voices
```
Python 使用：
```python
import edge_tts
import asyncio

async def run_tts(text: str, output: str, voice: str ='zh-CN-XiaoxiaoNeural') -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output)

if __name__ == '__main__':
    asyncio.run(run_tts('你好, 我是您的朋友，我叫晓晓', 'edge-tts-output.mp3'))
```
Jupyter 使用：
```python
import edge_tts
import asyncio
import IPython

async def run_tts(text: str, output: str, voice: str ='zh-CN-XiaoxiaoNeural') -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output)

async def amain() -> None:
    await asyncio.gather(run_tts('你好, 我是您的朋友，我叫晓晓', 'edge-tts-output.mp3'))

await amain()

IPython.display.Audio('edge-tts-output.mp3')
```
调整音色：
```batch
edge-tts --rate=-50% --text "Hello, world!" --write-media hello_with_rate_lowered.mp3 --write-subtitles hello_with_rate_lowered.srt
edge-tts --volume=-50% --text "Hello, world!" --write-media hello_with_volume_lowered.mp3 --write-subtitles hello_with_volume_lowered.srt
edge-tts --pitch=-50Hz --text "Hello, world!" --write-media hello_with_pitch_lowered.mp3 --write-subtitles hello_with_pitch_lowered.srt
```
音色列表：

| 名称                           | 语言            | 地区  | 性别  |
| ---------------------------- | ------------- | --- | --- |
| zh-CN-XiaoxiaoNeural         | 汉语（简体中文） 普通话  | 中国  | 女性  |
| zh-CN-XiaoyiNeural           | 汉语（简体中文） 普通话  | 中国  | 女性  |
| zh-CN-YunjianNeural          | 汉语（简体中文） 普通话  | 中国  | 男性  |
| zh-CN-YunxiNeural            | 汉语（简体中文） 普通话  | 中国  | 男性  |
| zh-CN-YunxiaNeural           | 汉语（简体中文） 普通话  | 中国  | 男性  |
| zh-CN-YunyangNeural          | 汉语（简体中文） 普通话  | 中国  | 男性  |
| zh-CN-liaoning-XiaobeiNeural | 汉语（简体中文） 辽宁方言 | 中国  | 女性  |
| zh-CN-shaanxi-XiaoniNeural   | 汉语（简体中文） 陕西方言 | 中国  | 女性  |
| zh-HK-HiuGaaiNeural          | 汉语（繁体中文） 粤语   | 香港  | 女性  |
| zh-HK-HiuMaanNeural          | 汉语（繁体中文） 粤语   | 香港  | 女性  |
| zh-HK-WanLungNeural          | 汉语（繁体中文） 粤语   | 香港  | 男性  |
| zh-TW-HsiaoChenNeural        | 汉语（繁体中文）      | 台湾  | 女性  |
| zh-TW-HsiaoYuNeural          | 汉语（繁体中文）      | 台湾  | 女性  |
| zh-TW-YunJheNeural           | 汉语（繁体中文）      | 台湾  | 男性  |
