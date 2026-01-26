#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试词性标签显示为全称
"""

from function.search_engine_kor import KoreanSearchEngine


def test_pos_fullname():
    """测试词性标签显示为全称"""
    print("=== 测试词性标签显示为全称 ===")
    
    # 初始化搜索引擎
    engine = KoreanSearchEngine()
    
    # 测试文件路径
    file_path = "test/test_kor.txt"
    
    # 测试不同类型的关键词
    test_keywords = [
        "속아",  # 动词
        "사랑",  # 名词
        "아름다운",  # 形容词
        "빠르게",  # 副词
    ]
    
    for keyword in test_keywords:
        print(f"\n测试关键词: '{keyword}'")
        
        # 执行搜索
        search_record = engine.search_korean_advanced(file_path, keyword)
        
        print(f"  搜索结果数量: {search_record['result_count']}")
        print(f"  词典形: {search_record['lemma']}")
        print(f"  词性全称: {search_record['pos']}")
        if 'original_pos' in search_record:
            print(f"  词性缩写: {search_record['original_pos']}")
        
        # 验证词性是否为全称
        pos = search_record['pos']
        if pos in ['VV', 'VA', 'NNG', 'NNP', 'MAG', 'VX']:
            print(f"  错误: 词性仍为缩写 '{pos}'")
        else:
            print(f"  ✅ 正确: 词性为全称 '{pos}'")
        
    print("\n=== 测试完成！===\n")


if __name__ == "__main__":
    test_pos_fullname()
