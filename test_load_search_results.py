#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试加载搜索结果功能
"""

import os
import sys
import tempfile
from bs4 import BeautifulSoup

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.qt_CorpusSearchTool import CorpusSearchToolGUI
from function.search_history_manager import search_history_manager

def test_load_search_results():
    """
    测试加载搜索结果功能
    """
    # 创建临时HTML文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>搜索结果</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        h1 { color: #333; text-align: center; }
        .search-info { margin-bottom: 20px; padding: 15px; background-color: white; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; background-color: white; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f2f2f2; font-weight: bold; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        tr:hover { background-color: #e8f4f8; }
        .highlight { background-color: #ffff99; }
    </style>
</head>
<body>
    <h1>搜索结果</h1>
    
    <div class="search-info">
        <p>搜索关键词: 테스트</p>
        <p>搜索路径: E:\语料库\韩语</p>
        <p>搜索时间: 2024-01-26 22:31:00</p>
        <p id="lemma_text">[规则动词 (Regular Verb)]：테스트하다</p>
        <p id="lemmalist_text">生成变体列表: 테스트하다, 테스트하고, 테스트해, 테스트했, 테스트해요, 테스트하세요; 实际命中变体: 테스트하다, 테스트해요</p>
        <p>结果数量: 2</p>
    </div>
    
    <table>
        <tr>
            <th>集数</th>
            <th>时间轴</th>
            <th>对应台词</th>
            <th>行号</th>
            <th>文件名</th>
            <th>文件路径</th>
        </tr>
        <tr>
            <td>第1集</td>
            <td>00:01:23</td>
            <td>테스트 문장 1</td>
            <td>10</td>
            <td>test1.md</td>
            <td>E:\语料库\韩语\test1.md</td>
        </tr>
        <tr>
            <td>第2集</td>
            <td>00:02:45</td>
            <td>테스트 문장 2</td>
            <td>20</td>
            <td>test2.md</td>
            <td>E:\语料库\韩语\test2.md</td>
        </tr>
    </table>
</body>
</html>
        ''')
        temp_file_path = f.name
    
    try:
        # 初始化搜索历史管理器
        search_history_manager.set_corpus_type('kor')
        
        # 清空历史记录
        search_history_manager.clear_history()
        
        # 创建GUI实例（模拟）
        from PySide6.QtWidgets import QApplication
        app = QApplication([])
        gui = CorpusSearchToolGUI()
        
        # 测试加载搜索结果
        gui.load_search_results_from_html(temp_file_path)
        
        # 检查历史记录是否被添加
        history = search_history_manager.get_recent_records(10)
        print(f"历史记录数量: {len(history)}")
        
        # 检查历史记录内容
        for record in history:
            print(f"关键词: {record.get('keywords')}")
            print(f"结果数量: {record.get('result_count')}")
            print(f"HTML路径: {record.get('html_path')}")
            print(f"词典形: {record.get('lemma')}")
            print(f"生成变体列表: {record.get('target_variant_set')}")
            print(f"实际命中变体: {record.get('actual_variant_set')}")
            print("---")
        
        # 再次加载相同的HTML文件，检查是否不会重复添加
        gui.load_search_results_from_html(temp_file_path)
        
        # 检查历史记录数量是否没有增加
        history_after_second_load = search_history_manager.get_recent_records(10)
        print(f"第二次加载后的历史记录数量: {len(history_after_second_load)}")
        
        if len(history_after_second_load) == len(history):
            print("✓ 测试通过：重复加载同一文件不会重复添加历史记录")
        else:
            print("✗ 测试失败：重复加载同一文件会重复添加历史记录")
        
    finally:
        # 清理临时文件
        os.unlink(temp_file_path)
        
        # 关闭应用程序
        app.quit()

if __name__ == "__main__":
    test_load_search_results()
