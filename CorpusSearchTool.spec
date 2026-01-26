# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

# 获取当前目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(SPEC))

# 图标文件的完整路径
ICON_PATH = os.path.join(current_dir, 'icons', 'CorpusSearchTool.png')

# 动态查找kiwipiepy模型路径
kiwipiepy_model_path = None
try:
    import kiwipiepy
    # 获取kiwipiepy安装路径
    kiwipiepy_install_path = os.path.dirname(kiwipiepy.__file__)
    # kiwipiepy_model通常位于site-packages目录下
    kiwipiepy_model_parent = os.path.dirname(kiwipiepy_install_path)
    model_dir = os.path.join(kiwipiepy_model_parent, 'kiwipiepy_model')
    if os.path.exists(model_dir):
        kiwipiepy_model_path = model_dir
    else:
        # 如果上面的方法不行，尝试在site-packages的同级目录中查找
        site_packages_parent = os.path.dirname(kiwipiepy_model_parent)
        model_dir = os.path.join(site_packages_parent, 'kiwipiepy_model')
        if os.path.exists(model_dir):
            kiwipiepy_model_path = model_dir
        else:
            # 再尝试在kiwipiepy包内部查找
            internal_model_dir = os.path.join(kiwipiepy_install_path, 'models')
            if os.path.exists(internal_model_dir):
                kiwipiepy_model_path = internal_model_dir
except ImportError:
    print("Warning: kiwipiepy not found, skipping model inclusion")

# 构建datas列表
datas_list = [
    # 包含整个目录以确保所有资源都被正确打包
    ('function', 'function'),
    ('gui', 'gui'),
    ('icons', 'icons'),
    # 添加配置文件到根目录，确保程序能在同级目录读取
    ('CorpusSearchTool.ini', '.'),
]

# 如果找到了kiwipiepy模型路径，添加到datas列表
if kiwipiepy_model_path:
    datas_list.append((kiwipiepy_model_path, 'kiwipiepy_model'))

a = Analysis(
    ['CorpusSearchTool.py'],
    pathex=[],
    binaries=[],
    datas=datas_list,
    hiddenimports=[
        # PySide6 相关的隐式导入
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        # 韩语形态分析相关依赖
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
        # 排除PyQt5以避免Qt绑定冲突
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.QtMultimedia',
        'sip',
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
