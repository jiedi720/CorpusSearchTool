---
name: "spec-rewriter"
description: "根据参考.spec文件配置逻辑重写项目.spec文件，确保.exe文件显示图标并能读取同级配置文件。当用户需要生成或更新PyInstaller打包配置时调用。"
---

# Spec 文件重写工具

# Spec 文件重写工具

## 功能说明

本技能用于根据参考 .spec 文件的配置逻辑，重写项目的 .spec 文件，确保生成的可执行文件具有以下特性：

1. **图标显示**：在程序标题栏和任务栏正常显示应用图标
2. **配置文件读取**：程序运行后能准确识别并读取同级目录下的配置文件
3. **依赖管理**：正确收集所有必要的依赖文件和模块
4. **优化打包**：排除不必要的模块以减小可执行文件体积

## 使用场景

当您需要：
- 为新项目生成 .spec 文件配置
- 重新生成或更新现有项目的 .spec 文件
- 确保打包后的可执行文件能正确显示图标
- 确保打包后的程序能正确读取配置文件
- 优化打包过程和结果
- 为不同项目统一打包配置标准

## 实现原理

1. **参考 BOSCH_Toolbox.spec 配置逻辑**：
   - 使用 `os.path.dirname(os.path.abspath(SPEC))` 获取当前目录的绝对路径
   - 构建完整的图标文件路径，确保图标正确显示
   - 详细配置 `datas` 列表，包含所有必要的目录和文件
   - 精确配置 `hiddenimports`，包含所有隐式依赖
   - 合理配置 `excludes`，排除不需要的模块以减小体积

2. **项目适配**：
   - 自动识别项目结构和主入口文件
   - 包含项目特定的目录和模块（如 function、gui、icons 等）
   - 添加项目所需的隐式导入，确保所有模块正确加载
   - 配置正确的图标文件路径，确保程序标题栏和任务栏显示图标

3. **配置文件读取支持**：
   - 在 `datas` 列表中添加配置文件到根目录（如 `('CorpusSearchTool.ini', '.')`）
   - 确保打包后的程序能在同级目录读取配置文件
   - 提供配置文件包含的示例代码

4. **依赖管理**：
   - 自动收集所有必要的依赖文件和模块
   - 对特殊依赖（如 kiwipiepy 模型）进行单独处理
   - 使用 UPX 压缩可执行文件，减小体积
   - 对 DLL 文件进行合理处理，避免重复打包

## 示例用法

### 基本用法

当您需要为项目生成或更新 .spec 文件时，可使用本技能参考 BOSCH_Toolbox.spec 的配置逻辑生成新的配置文件。

### 参考 BOSCH_Toolbox.spec 配置示例

```python
# -*- mode: python ; coding: utf-8 -*-
import os

# 获取当前目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(SPEC))

# 图标文件的完整路径
ICON_PATH = os.path.join(current_dir, 'icons', 'app_icon.png')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 包含资源目录
        ('function', 'function'),
        ('gui', 'gui'),
        ('icons', 'icons'),
        # 添加配置文件到根目录
        ('config.ini', '.'),
    ],
    hiddenimports=[
        # PySide6 相关的隐式导入
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        # 项目模块
        'function.module1',
        'function.module2',
        'gui.main_gui',
    ],
    excludes=[
        # 排除不需要的模块以减小体积
        'tkinter',
        'matplotlib',
        'numpy',
        # 排除不需要的 PySide6 模块
        'PySide6.Qt3DAnimation',
        'PySide6.Qt3DExtras',
        # 更多排除模块...
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
    name='AppName',
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
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AppName',
)
```

### 自定义配置

1. **图标配置**：
   - 默认查找 `icons` 目录下的图标文件
   - 支持 `.ico` 和 `.png` 格式的图标文件
   - 可通过修改 `ICON_PATH` 变量自定义图标路径

2. **配置文件支持**：
   - 在 `datas` 列表中添加配置文件：`('config.ini', '.')`
   - 确保程序运行时能识别同级目录下的配置文件
   - 可根据项目需求添加多个配置文件

3. **依赖管理**：
   - 自动收集所有必要的依赖模块
   - 在 `hiddenimports` 中添加隐式依赖
   - 在 `excludes` 中排除不需要的模块以减小体积

4. **打包优化**：
   - 使用 UPX 压缩可执行文件
   - 合理配置 `COLLECT` 选项
   - 对特殊依赖（如语言模型）进行单独处理

## 注意事项

1. **图标文件准备**：
   - 运行本技能前，请确保项目中存在图标文件，默认路径为 `icons` 目录下
   - 支持 `.ico` 和 `.png` 格式的图标文件

2. **配置文件处理**：
   - 参考 BOSCH_Toolbox.spec 的配置方式，将配置文件添加到 `datas` 列表
   - 示例：`('config.ini', '.')` 确保配置文件被添加到根目录

3. **依赖管理**：
   - 确保在 `hiddenimports` 中添加所有必要的隐式依赖
   - 在 `excludes` 中排除不需要的模块以减小体积

4. **路径处理**：
   - 使用 `os.path.dirname(os.path.abspath(SPEC))` 获取当前目录路径
   - 避免使用硬编码路径，确保在不同环境下都能正确定位文件

5. **打包验证**：
   - 生成 .spec 文件后，运行 `pyinstaller your_app.spec` 进行打包
   - 测试生成的可执行文件是否能正确显示图标和读取配置文件

6. **自定义调整**：
   - 根据项目的具体需求，手动调整生成的 .spec 文件中的配置项
   - 对于特殊依赖（如语言模型、第三方库），可能需要额外配置

## 适配不同项目

本技能适用于以下类型的 Python 项目：
- GUI 应用程序（使用 tkinter、PyQt、PySide 等）
- 命令行工具
- 包含配置文件的应用程序
- 需要特定图标显示的应用程序

无论项目类型如何，本技能都能生成适合的 .spec 文件配置，确保打包过程顺利完成，生成的可执行文件能正常运行。
