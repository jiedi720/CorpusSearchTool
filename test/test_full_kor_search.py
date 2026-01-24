#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整测试韩语高级搜索功能，包括搜索历史保存
"""

from function.search_engine_kor import KoreanSearchEngine
from function.search_history_manager import SearchHistoryManager


def test_full_korean_search():
    """测试完整的韩语搜索流程"""
    # 初始化搜索引擎和历史管理器
    print("=== 初始化组件 ===")
    engine = KoreanSearchEngine()
    history_manager = SearchHistoryManager("kor")
    print("组件初始化成功")
    
    # 测试1：基础动词搜索
    print("\n=== 测试1: 基础动词搜索 ===")
    raw_keyword = "속아"
    file_path = "test/test_kor.txt"
    
    result = engine.search_korean_advanced(file_path, raw_keyword)
    print(f"搜索完成！关键词: {raw_keyword}")
    print(f"词典形: {result['lemma']}")
    print(f"词性: {result['pos']}")
    print(f"实际变体: {result['actual_variant_set']}")
    print(f"结果数量: {result['result_count']}")
    
    # 添加到历史记录
    history_manager.add_record(
        keywords=raw_keyword,
        input_path=file_path,
        output_path="N/A",
        regex_enabled=False,
        result_count=result['result_count'],
        keyword_type="动词/形容词"
    )
    print("已添加到搜索历史")
    
    # 测试2：名词搜索
    print("\n=== 测试2: 名词搜索 ===")
    raw_keyword = "사랑"
    
    result = engine.search_korean_advanced(file_path, raw_keyword)
    print(f"搜索完成！关键词: {raw_keyword}")
    print(f"词典形: {result['lemma']}")
    print(f"词性: {result['pos']}")
    print(f"实际变体: {result['actual_variant_set']}")
    print(f"结果数量: {result['result_count']}")
    
    # 添加到历史记录
    history_manager.add_record(
        keywords=raw_keyword,
        input_path=file_path,
        output_path="N/A",
        regex_enabled=False,
        result_count=result['result_count'],
        keyword_type="名词/副词"
    )
    print("已添加到搜索历史")
    
    # 查看生成的历史文件
    print("\n=== 查看生成的搜索历史文件 ===")
    import os
    if os.path.exists(history_manager.history_file):
        with open(history_manager.history_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n历史文件 '{history_manager.history_file}' 内容:")
        print("=" * 50)
        print(content)
        print("=" * 50)
    else:
        print(f"历史文件 '{history_manager.history_file}' 未生成")
    
    print("\n=== 测试完成！===\n")


if __name__ == "__main__":
    test_full_korean_search()
