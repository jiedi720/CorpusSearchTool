#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
字幕语料库检索工具 - 主程序入口
作者: Assistant
描述: 这是一个基于Python的字幕语料库检索工具，可以搜索字幕文件中的特定词汇
"""

import os
import sys


def main():
    """主函数，启动应用程序"""
    # 导入主窗口，延迟导入以处理tkinterdnd2依赖
    try:
        from gui.main_window import MainWindow
        app = MainWindow()
        app.run()
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所有依赖包:")
        print("pip install -r requirements.txt")
        input("按回车键退出...")
        return 1
    except Exception as e:
        print(f"程序运行错误: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())