#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试韩语变体生成
"""

from function.search_engine_kor import search_engine_kor

# 测试 외롭다 的变体生成
word = "외롭다"
print(f"测试单词: {word}")

variants = search_engine_kor._generate_korean_variants(word)
print(f"生成的变体数量: {len(variants)}")
print("生成的变体:")
for i, variant in enumerate(variants):
    print(f"{i+1}. {variant}")

# 检查特定变体是否存在
target_variants = ["외로운", "외로울", "외로웠", "외로워"]
print("\n检查特定变体是否存在:")
for target in target_variants:
    if target in variants:
        print(f"✓ {target} 存在")
    else:
        print(f"✗ {target} 不存在")
