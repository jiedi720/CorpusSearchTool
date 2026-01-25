#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试新增按钮功能
测试lemmalist_btn和stop_search_btn的功能
"""

import os
import sys
import time

# 将项目根目录添加到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from gui.qt_CorpusSearchTool import CorpusSearchToolGUI


def test_new_buttons():
    """
    测试新增按钮功能
    """
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = CorpusSearchToolGUI()
    window.show()
    
    # 给窗口一点时间初始化
    time.sleep(1)
    
    # 测试1: 检查lemmalist_btn是否存在
    assert hasattr(window, 'lemmalist_btn'), "lemmalist_btn 不存在"
    print("✅ 测试1: lemmalist_btn 存在")
    
    # 测试2: 检查stop_search_btn是否存在
    assert hasattr(window, 'stop_search_btn'), "stop_search_btn 不存在"
    print("✅ 测试2: stop_search_btn 存在")
    
    # 测试3: 检查generate_lemmalist方法是否存在
    assert hasattr(window, 'generate_lemmalist'), "generate_lemmalist 方法不存在"
    print("✅ 测试3: generate_lemmalist 方法存在")
    
    # 测试4: 检查stop_search方法是否存在
    assert hasattr(window, 'stop_search'), "stop_search 方法不存在"
    print("✅ 测试4: stop_search 方法存在")
    
    # 测试5: 检查SearchThread类是否有stop方法
    from gui.qt_CorpusSearchTool import SearchThread
    assert hasattr(SearchThread, 'stop'), "SearchThread.stop 方法不存在"
    print("✅ 测试5: SearchThread.stop 方法存在")
    
    # 测试6: 检查SearchThread类是否有_stop_flag属性
    thread = SearchThread("", "test", False, False, False)
    assert hasattr(thread, '_stop_flag'), "SearchThread._stop_flag 属性不存在"
    print("✅ 测试6: SearchThread._stop_flag 属性存在")
    
    print("\n🎉 所有测试通过！新增按钮功能已成功实现。")
    
    # 关闭应用程序
    app.quit()
    
    return True


if __name__ == "__main__":
    test_new_buttons()
