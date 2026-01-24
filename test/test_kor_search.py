#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试韩语高级搜索功能
"""

from function.search_engine_kor import KoreanSearchEngine


def test_korean_advanced_search():
    """测试韩语高级搜索功能"""
    # 初始化搜索引擎
    engine = KoreanSearchEngine()
    print("初始化搜索引擎成功")
    
    # 测试动词变形匹配
    print("\n=== 测试1: 动词变形匹配（输入: 속아）===")
    result = engine.search_korean_advanced('test/test_kor.txt', '속아')
    print(f"原始关键词: {result['raw_keyword']}")
    print(f"词典形: {result['lemma']}")
    print(f"词性: {result['pos']}")
    print(f"实际变体: {result['actual_variant_set']}")
    print(f"结果数量: {result['result_count']}")
    
    # 测试名词匹配
    print("\n=== 测试2: 名词匹配（输入: 사랑）===")
    result2 = engine.search_korean_advanced('test/test_kor.txt', '사랑')
    print(f"原始关键词: {result2['raw_keyword']}")
    print(f"词典形: {result2['lemma']}")
    print(f"词性: {result2['pos']}")
    print(f"实际变体: {result2['actual_variant_set']}")
    print(f"结果数量: {result2['result_count']}")
    
    print("\n所有测试完成！")


if __name__ == "__main__":
    test_korean_advanced_search()
