#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 lemmalist_btn 变体表生成功能
"""

import sys
sys.path.insert(0, '.')
from PyQt5.QtWidgets import QApplication
# 必须先创建 QApplication
app = None
from gui.qt_CorpusSearchTool import CorpusSearchToolGUI

def test_lemmalist_generation():
    """测试变体表生成功能"""
    global app
    if app is None:
        app = QApplication(sys.argv)
    window = CorpusSearchToolGUI()
    
    # 测试1: 动词 이루다
    print("=" * 60)
    print("测试1: 动词 '이루다'")
    print("=" * 60)
    window.korean_keyword_edit.setText('이루다')
    window.generate_lemmalist()
    result1 = window.korean_lemmalist_display.text()
    print(result1)
    print()
    
    # 测试2: 动词 하다
    print("=" * 60)
    print("测试2: 动词 '하다'")
    print("=" * 60)
    window.korean_keyword_edit.setText('하다')
    window.generate_lemmalist()
    result2 = window.korean_lemmalist_display.text()
    print(result2)
    print()
    
    # 测试3: 动词 속다
    print("=" * 60)
    print("测试3: 动词 '속다'")
    print("=" * 60)
    window.korean_keyword_edit.setText('속다')
    window.generate_lemmalist()
    result3 = window.korean_lemmalist_display.text()
    print(result3)
    print()
    
    # 测试4: 复合动词 좋아하다
    print("=" * 60)
    print("测试4: 复合动词 '좋아하다'")
    print("=" * 60)
    window.korean_keyword_edit.setText('좋아하다')
    window.generate_lemmalist()
    result4 = window.korean_lemmalist_display.text()
    print(result4)
    print()
    
    # 测试5: 名词
    print("=" * 60)
    print("测试5: 名词 '사람'")
    print("=" * 60)
    window.korean_keyword_edit.setText('사람')
    window.generate_lemmalist()
    result5 = window.korean_lemmalist_display.text()
    print(result5)
    print()
    
    print("=" * 60)
    print("✅ 所有测试完成")
    print("=" * 60)

if __name__ == '__main__':
    test_lemmalist_generation()