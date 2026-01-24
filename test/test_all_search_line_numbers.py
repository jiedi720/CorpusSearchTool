#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有搜索引擎的行号显示功能
"""

from function.search_engine_kor import KoreanSearchEngine
from function.search_engine_eng import EnglishSearchEngine
from function.search_engine_base import SearchEngineBase


def test_all_search_line_numbers():
    """测试所有搜索引擎的行号显示"""
    print("=== 测试所有搜索引擎的行号显示 ===")
    
    # 测试文件路径
    file_path = "test/test_kor.txt"
    
    # 初始化搜索引擎
    kor_engine = KoreanSearchEngine()
    eng_engine = EnglishSearchEngine()
    base_engine = SearchEngineBase()
    
    print("\n1. 测试韩语高级搜索")
    test_korean_advanced_search(kor_engine, file_path)
    
    print("\n2. 测试英语变形搜索")
    test_english_variants_search(eng_engine, file_path)
    
    print("\n3. 测试基础搜索功能")
    test_base_search(base_engine, file_path)
    
    print("\n4. 测试完全匹配搜索")
    test_exact_match_search(base_engine, file_path)
    
    print("\n=== 所有测试通过！所有搜索引擎都能正确显示行号 ===")


def test_korean_advanced_search(engine, file_path):
    """测试韩语高级搜索"""
    search_record = engine.search_korean_advanced(file_path, "속아")
    
    print(f"   搜索结果数量: {search_record['result_count']}")
    
    for i, result in enumerate(search_record['search_results']):
        line_num = result['lineno']
        print(f"   结果 {i+1}: 行号={line_num}")
        assert line_num != '', f"结果 {i+1} 缺少行号信息"


def test_english_variants_search(engine, file_path):
    """测试英语变形搜索"""
    results = engine.search_english_variants(file_path, ["love"])
    
    print(f"   搜索结果数量: {len(results)}")
    
    for i, result in enumerate(results):
        # 英语搜索可能没有匹配结果，所以我们只检查有结果时的行号
        if result:
            line_num = result.get('lineno', '') or result.get('line_number', '')
            print(f"   结果 {i+1}: 行号={line_num}")
            assert line_num != '', f"结果 {i+1} 缺少行号信息"


def test_base_search(engine, file_path):
    """测试基础搜索功能"""
    results = engine.search_in_file(file_path, ["사랑"])
    
    print(f"   搜索结果数量: {len(results)}")
    
    for i, result in enumerate(results):
        line_num = result.get('lineno', '') or result.get('line_number', '')
        print(f"   结果 {i+1}: 行号={line_num}")
        assert line_num != '', f"结果 {i+1} 缺少行号信息"


def test_exact_match_search(engine, file_path):
    """测试完全匹配搜索"""
    results = engine.search_exact_match(file_path, "사랑")
    
    print(f"   搜索结果数量: {len(results)}")
    
    for i, result in enumerate(results):
        line_num = result.get('lineno', '')
        print(f"   结果 {i+1}: 行号={line_num}")
        assert line_num != '', f"结果 {i+1} 缺少行号信息"


if __name__ == "__main__":
    test_all_search_line_numbers()
