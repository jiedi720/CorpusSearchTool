# -*- mode: python ; coding: utf-8 -*-
import os

# 获取当前目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(SPEC))

# 图标文件的完整路径
ICON_PATH = os.path.join(current_dir, 'icons', 'CorpusSearchTool.png')

a = Analysis(
    ['CorpusSearchTool.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 包含整个目录以确保所有资源都被正确打包
        ('function', 'function'),
        ('gui', 'gui'),
        ('icons', 'icons'),
        # 添加配置文件到根目录，确保程序能在同级目录读取
        ('CorpusSearchTool.ini', '.'),
        # 添加kiwipiepy_model模型文件
        (r'C:\Users\jiedi\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\kiwipiepy_model', 'kiwipiepy_model'),
    ],
    hiddenimports=[
        # PySide6 相关的隐式导入
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        # 韩语形态分析相关依赖
        'kiwipiepy_model',
        'kiwipiepy',
        # 项目模块
        'function.config_manager',
        'function.document_parser',
        'function.file_drag_drop',
        'function.file_selector',
        'function.result_exporter',
        'function.result_processor',
        'function.search_engine_base',
        'function.search_engine_eng',
        'function.search_engine_kor',
        'function.search_history_manager',
        'function.subtitle_parser',
        'gui.font',
        'gui.qt_CorpusSearchTool',
        'gui.search_history_gui',
        'gui.search_result_table_gui',
        'gui.theme',
        'gui.ui_CorpusSearchTool',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的模块以减小体积
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        # 排除不需要的PySide6模块
        'PySide6.Qt3DAnimation',
        'PySide6.Qt3DCore',
        'PySide6.Qt3DExtras',
        'PySide6.Qt3DInput',
        'PySide6.Qt3DLogic',
        'PySide6.Qt3DRender',
        'PySide6.QtCharts',
        'PySide6.QtConcurrent',
        'PySide6.QtDataVisualization',
        'PySide6.QtDesigner',
        'PySide6.QtHelp',
        'PySide6.QtLocation',
        'PySide6.QtMultimedia',
        'PySide6.QtMultimediaWidgets',
        'PySide6.QtNetwork',
        'PySide6.QtNetworkAuth',
        'PySide6.QtNfc',
        'PySide6.QtOpenGL',
        'PySide6.QtOpenGLWidgets',
        'PySide6.QtPdf',
        'PySide6.QtPdfWidgets',
        'PySide6.QtPositioning',
        'PySide6.QtPrintSupport',
        'PySide6.QtQml',
        'PySide6.QtQuick',
        'PySide6.QtQuick3D',
        'PySide6.QtQuickControls2',
        'PySide6.QtQuickWidgets',
        'PySide6.QtRemoteObjects',
        'PySide6.QtScxml',
        'PySide6.QtSensors',
        'PySide6.QtSerialPort',
        'PySide6.QtSql',
        'PySide6.QtStateMachine',
        'PySide6.QtSvg',
        'PySide6.QtSvgWidgets',
        'PySide6.QtTest',
        'PySide6.QtTextToSpeech',
        'PySide6.QtUiTools',
        'PySide6.QtWebChannel',
        'PySide6.QtWebEngine',
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebEngineQuick',
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebSockets',
        'PySide6.QtXml',
        'PySide6.QtXmlPatterns',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CorpusSearchTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON_PATH,
)

coll = COLLECT(
    exe,                # 包含之前定义的 EXE 对象（主程序）
    a.binaries,         # 收集所有依赖的 DLL/动态库
    a.datas,            # 收集所有的资源文件（图片、配置等）
    strip=False,        # 是否移除符号表（通常选 False 以防报错）
    upx=True,           # 是否使用 UPX 压缩混淆
    upx_exclude=[],     # 排除不压缩的文件
    name='CorpusSearchTool',  # 最终生成的文件夹名称
)
