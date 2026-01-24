#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试搜索历史使用具体词典型作为关键词类型
"""

from function.search_history_manager import SearchHistoryManager
from function.search_engine_kor import KoreanSearchEngine


def test_search_history_pos():
    """测试搜索历史使用具体词典型"""
    print("=== 测试搜索历史使用具体词典型 ===")
    
    # 初始化组件
    engine = KoreanSearchEngine()
    history_manager = SearchHistoryManager("kor")
    
    # 清空历史记录，方便测试
    history_manager.clear_history()
    print("已清空历史记录")
    
    # 测试文件路径
    file_path = "test/test_kor.txt"
    
    # 测试不同类型的关键词
    test_keywords = [
        "속아",  # 动词
        "사랑",  # 名词
        "빠르게",  # 形容词
    ]
    
    for keyword in test_keywords:
        print(f"\n1. 执行搜索: 关键词='{keyword}'")
        search_record = engine.search_korean_advanced(file_path, keyword)
        
        print(f"   搜索结果: {search_record['result_count']} 条匹配")
        print(f"   词典形: {search_record['lemma']}")
        print(f"   具体词典型: {search_record['pos']}")
        
        # 添加到历史记录
        history_manager.add_record(
            keywords=keyword,
            input_path=file_path,
            output_path="N/A",
            regex_enabled=False,
            result_count=search_record['result_count'],
            keyword_type=search_record['pos'],  # 使用具体词典型
            lemma=search_record['lemma'],
            actual_variant_set=search_record['actual_variant_set']
        )
        print(f"   已添加到搜索历史，关键词类型: {search_record['pos']}")
    
    # 读取并验证历史记录
    print("\n2. 查看搜索历史记录")
    import os
    if os.path.exists(history_manager.history_file):
        with open(history_manager.history_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n历史文件内容:")
        print("=" * 60)
        print(content)
        print("=" * 60)
        
        # 验证历史记录中使用了具体词典型
        for keyword in test_keywords:
            search_record = engine.search_korean_advanced(file_path, keyword)
            expected_pos = search_record['pos']
            assert expected_pos in content, f"历史记录中缺少具体词典型 '{expected_pos}'"
            print(f"✓ 验证成功: 历史记录中包含具体词典型 '{expected_pos}'")
    
    print("\n=== 测试完成！===\n")


if __name__ == "__main__":
    test_search_history_pos()
