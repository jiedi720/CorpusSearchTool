#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试韩语变体搜索历史保存功能
"""

import os
import sys
from function.search_engine_kor import search_engine_kor
from function.search_history_manager import SearchHistoryManager

# 创建测试文件
with open("test_kor_variant.txt", "w", encoding="utf-8") as f:
    f.write("나는 속았어요.\n")  # 속았어요 (过去式)
    f.write("너는 속지 않았어.\n")  # 속지 (否定)
    f.write("그는 속고 있는 거야.\n")  # 속고 (连接)

# 测试1：直接使用搜索引擎测试变体生成
print("=== 测试1：变体生成 ===")
search_record = search_engine_kor.search_korean_advanced("test_kor_variant.txt", "속다")
print(f"词典形: {search_record['lemma']}")
print(f"生成的变体列表: {search_record['target_variant_set']}")
print(f"实际命中变体: {search_record['actual_variant_set']}")

# 测试2：测试搜索历史保存
print("\n=== 测试2：搜索历史保存 ===")
history_manager = SearchHistoryManager(corpus_type="kor")

# 添加搜索记录，包含生成的变体列表
history_manager.add_record(
    keywords="속다",
    input_path="test_kor_variant.txt",
    case_sensitive=False,
    fuzzy_match=False,
    regex_enabled=False,
    result_count=3,
    keyword_type="规则动词 (Regular Verb)",
    lemma="속다",
    actual_variant_set=search_record['actual_variant_set'],
    target_variant_set=search_record['target_variant_set']
)

# 读取并检查搜索历史文件
print("\n=== 测试3：搜索历史内容检查 ===")
history_file_path = "search_history_kor.md"
if os.path.exists(history_file_path):
    with open(history_file_path, "r", encoding="utf-8") as f:
        history_content = f.read()
    
    print("搜索历史文件内容：")
    print(history_content)
    
    # 检查是否包含生成的变体列表
    if "**生成变体列表**:" in history_content:
        print("\n✓ 测试通过：搜索历史中包含生成的变体列表")
    else:
        print("\n✗ 测试失败：搜索历史中缺少生成的变体列表")
        sys.exit(1)
else:
    print("\n✗ 测试失败：搜索历史文件不存在")
    sys.exit(1)

# 清理测试文件
if os.path.exists("test_kor_variant.txt"):
    os.remove("test_kor_variant.txt")
    print("\n测试文件已清理")

print("\n=== 所有测试通过！ ===")
