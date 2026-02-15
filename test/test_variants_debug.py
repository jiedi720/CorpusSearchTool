#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试韩语变体生成（带调试信息）
"""

from function.search_engine_kor import search_engine_kor

# 测试 외롭다 的变体生成
word = "외롭다"
print(f"测试单词: {word}")

# 调试：分析单词的词性
analysis_result = search_engine_kor.kiwi.analyze(word)
print("\n分析结果:")
for token in analysis_result[0][0]:
    print(f"形态素: {token.form}, 词典形: {token.lemma}, 词性: {token.tag}")

# 去掉다得到词干
base = word[:-1]  # 去掉다
print(f"\n词干: {base}")

variants = search_engine_kor._generate_korean_variants(word)
print(f"\n生成的变体数量: {len(variants)}")
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

# 手动生成变音后的变体进行测试
print("\n手动生成变音后的变体:")
transformed_base = base[:-1] + '로'
print(f"变音后的词干: {transformed_base}")
transform_variants = [
    transformed_base + '은',  # 如 외로운
    transformed_base + '을',  # 如 외로울
    transformed_base + '웠',  # 如 외로웠
    transformed_base + '워',  # 如 외로워
]
for tv in transform_variants:
    print(f"手动生成: {tv}")
