#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试补充后的词性标签映射字典
"""

from function.search_engine_kor import KoreanSearchEngine


def test_pos_map_update():
    """测试补充后的词性标签映射"""
    print("=== 测试补充后的词性标签映射 ===")
    
    # 初始化搜索引擎
    engine = KoreanSearchEngine()
    
    # 测试文件路径
    file_path = "test/test_kor.txt"
    
    # 测试不同类型的关键词
    test_keywords = [
        "속아",  # 规则动词
        "사랑",  # 一般名词
        "아름다운",  # 不规则形容词
        "빠르게",  # 规则形容词
        "나",  # 代名词
        "하나",  # 数词
    ]
    
    for keyword in test_keywords:
        print(f"\n测试关键词: '{keyword}'")
        
        # 执行搜索
        search_record = engine.search_korean_advanced(file_path, keyword)
        
        print(f"  搜索结果数量: {search_record['result_count']}")
        print(f"  词典形: {search_record['lemma']}")
        print(f"  词性全称: {search_record['pos']}")
        
        # 检查是否使用了正确的全称标签
        if '动词' in search_record['pos'] or '形容词' in search_record['pos']:
            # 用言应该包含规则/不规则信息
            assert '规则' in search_record['pos'] or '不规则' in search_record['pos'], f"用言 '{keyword}' 的词性标签应包含规则/不规则信息"
        
        if '名词' in search_record['pos']:
            # 名词应该包含具体类型
            assert any(tag in search_record['pos'] for tag in ['一般', '专有', '依存', '数词', '代名词']), f"名词 '{keyword}' 的词性标签应包含具体类型"
    
    print("\n=== 测试完成！===\n")


if __name__ == "__main__":
    test_pos_map_update()
