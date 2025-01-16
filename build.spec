# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['edge_tts.constants'],  # edge-tts 需要的隐藏导入
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'tkinter', 'scipy', 'pandas', 'PIL',
        '_bz2', '_lzma', '_decimal', 'pywin32_system32',
        'unittest', 'pdb', 'difflib', 'doctest'
    ],
    collect_submodules=['edge_tts'],  # 只收集 edge_tts 相关模块
    collect_data=False,  # 减少收集的数据文件
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Edge TTS Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    optimize=2,  # 使用 Python 优化
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
) 