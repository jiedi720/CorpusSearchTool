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
    try:
        from PySide6.QtWidgets import QApplication
        from gui.qt_CorpusSearchTool import CorpusSearchToolGUI
        
        # 创建应用程序
        app = QApplication(sys.argv)
        app.setApplicationName("字幕语料库检索工具")
        app.setOrganizationName("CorpusSearchTool")
        
        # 创建主窗口
        window = CorpusSearchToolGUI()
        window.show()
        
        # 运行应用程序
        sys.exit(app.exec())
    except ImportError as e:
        print(f"导入错误: {e}")
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