#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试搜索历史记录中包含系统判定的词典形和实际命中的变体形式列表
"""

from function.search_history_manager import SearchHistoryManager
from function.search_engine_kor import KoreanSearchEngine


def test_search_history_with_lemma():
    """测试搜索历史记录包含词典形和实际变体"""
    print("=== 测试搜索历史记录包含词典形和实际变体 ===")
    
    # 初始化组件
    engine = KoreanSearchEngine()
    history_manager = SearchHistoryManager("kor")
    
    # 清空历史记录，方便测试
    history_manager.clear_history()
    print("已清空历史记录")
    
    # 执行韩语搜索
    file_path = "test/test_kor.txt"
    raw_keyword = "속아"
    
    print(f"\n1. 执行搜索: 关键词='{raw_keyword}'")
    search_record = engine.search_korean_advanced(file_path, raw_keyword)
    
    print(f"   搜索结果: {search_record['result_count']} 条匹配")
    print(f"   词典形: {search_record['lemma']}")
    print(f"   实际变体: {search_record['actual_variant_set']}")
    
    # 添加到历史记录
    history_manager.add_record(
        keywords=raw_keyword,
        input_path=file_path,
        output_path="N/A",
        regex_enabled=False,
        result_count=search_record['result_count'],
        keyword_type="动词/形容词",
        lemma=search_record['lemma'],
        actual_variant_set=search_record['actual_variant_set']
    )
    print("   已添加到搜索历史")
    
    # 执行另一次搜索
    raw_keyword = "사랑"
    print(f"\n2. 执行搜索: 关键词='{raw_keyword}'")
    search_record = engine.search_korean_advanced(file_path, raw_keyword)
    
    print(f"   搜索结果: {search_record['result_count']} 条匹配")
    print(f"   词典形: {search_record['lemma']}")
    print(f"   实际变体: {search_record['actual_variant_set']}")
    
    # 添加到历史记录
    history_manager.add_record(
        keywords=raw_keyword,
        input_path=file_path,
        output_path="N/A",
        regex_enabled=False,
        result_count=search_record['result_count'],
        keyword_type="名词/副词",
        lemma=search_record['lemma'],
        actual_variant_set=search_record['actual_variant_set']
    )
    print("   已添加到搜索历史")
    
    # 查看历史记录
    print("\n3. 查看生成的搜索历史文件")
    import os
    if os.path.exists(history_manager.history_file):
        with open(history_manager.history_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n历史文件 '{history_manager.history_file}' 内容:")
        print("=" * 60)
        print(content)
        print("=" * 60)
        
        # 验证历史记录中包含词典形和实际变体
        assert "**词典形**: " in content, "历史记录中缺少词典形信息"
        assert "**实际命中变体**: " in content, "历史记录中缺少实际命中变体信息"
        print("\n✓ 验证通过: 搜索历史记录中包含词典形和实际命中变体信息")
    else:
        print(f"错误: 历史文件 '{history_manager.history_file}' 未生成")
        return False
    
    print("\n=== 测试完成！===")
    return True


if __name__ == "__main__":
    test_search_history_with_lemma()
