#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试搜索历史记录管理器
"""

from function.search_history_manager import SearchHistoryManager

# 创建搜索历史记录管理器实例
history_manager = SearchHistoryManager(corpus_type="kor")

# 添加测试记录，不使用正则表达式
history_manager.add_record(
    keywords="속다",
    input_path="test_path",
    output_path="",
    case_sensitive=False,
    fuzzy_match=False,
    regex_enabled=False,
    result_count=1,
    keyword_type="规则动词 (Regular Verb)",
    lemma="속다",
    actual_variant_set=["속"]
)

# 添加测试记录，使用正则表达式
history_manager.add_record(
    keywords="test.*",
    input_path="test_path",
    output_path="",
    case_sensitive=False,
    fuzzy_match=False,
    regex_enabled=True,
    result_count=2,
    keyword_type="",
    lemma="",
    actual_variant_set=[]
)

print("测试完成！请查看 search_history_kor.md 文件")
