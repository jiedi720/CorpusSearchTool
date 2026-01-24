#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试搜索结果中显示对应台词在原文件里的行号
"""

from function.search_engine_kor import KoreanSearchEngine
from function.result_processor import result_processor


def test_line_number_display():
    """测试搜索结果显示行号"""
    print("=== 测试搜索结果显示行号 ===")
    
    # 初始化搜索引擎
    engine = KoreanSearchEngine()
    
    # 测试文件路径
    file_path = "test/test_kor.txt"
    
    # 1. 测试韩语动词搜索
    print(f"\n1. 测试韩语动词搜索: 关键词='속아'")
    search_record = engine.search_korean_advanced(file_path, "속아")
    
    print(f"   搜索结果数量: {search_record['result_count']}")
    
    for i, result in enumerate(search_record['search_results']):
        print(f"   结果 {i+1}:")
        print(f"     内容: {result['content']}")
        print(f"     行号: {result['lineno']} (lineno字段)")
        print(f"     行号: {result['line_number']} (line_number字段)")
        assert result['lineno'] != '', f"结果 {i+1} 缺少行号信息"
    
    # 2. 测试韩语名词搜索
    print(f"\n2. 测试韩语名词搜索: 关键词='사랑'")
    search_record = engine.search_korean_advanced(file_path, "사랑")
    
    print(f"   搜索结果数量: {search_record['result_count']}")
    
    for i, result in enumerate(search_record['search_results']):
        print(f"   结果 {i+1}:")
        print(f"     内容: {result['content']}")
        print(f"     行号: {result['lineno']} (lineno字段)")
        print(f"     行号: {result['line_number']} (line_number字段)")
        assert result['lineno'] != '', f"结果 {i+1} 缺少行号信息"
    
    # 3. 测试结果处理器的格式化功能
    print(f"\n3. 测试结果处理器的格式化功能")
    if search_record['search_results']:
        formatted_results = result_processor.format_results_for_display(search_record['search_results'], 'document')
        
        for i, result in enumerate(formatted_results):
            filename, line_number, episode, time_axis, content, file_path = result
            print(f"   格式化结果 {i+1}:")
            print(f"     文件名: {filename}")
            print(f"     行号: {line_number}")
            print(f"     内容: {content}")
            assert line_number != '0', f"格式化结果 {i+1} 行号显示错误"
    
    print("\n=== 所有测试通过！行号显示正常 ===")
    
    return True


if __name__ == "__main__":
    test_line_number_display()
