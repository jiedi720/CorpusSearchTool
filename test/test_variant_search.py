#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试韩语变体搜索功能
"""

from function.search_engine_kor import search_engine_kor

# 创建测试文件
with open("test_kor.txt", "w", encoding="utf-8") as f:
    f.write("나는 속았어요.\n")  # 속았어요 (过去式)
    f.write("너는 속지 않았어.\n")  # 속지 (否定)
    f.write("그는 속고 있는 거야.\n")  # 속고 (连接)
    f.write("우리는 속았을 거예요.\n")  # 속았을 (过去将来时)
    f.write("이렇게 속은 적이 없어요.\n")  # 속은 (过去分词)
    f.write("속음이 많아요.\n")  # 속음 (名词化)
    f.write("속기 좋아요.\n")  # 속기 (动词名词化)

# 测试搜索
try:
    print("=== 测试韩语变体搜索 ===")
    search_record = search_engine_kor.search_korean_advanced("test_kor.txt", "속다")
    
    print(f"原始关键词: {search_record['raw_keyword']}")
    print(f"词典形: {search_record['lemma']}")
    print(f"词性: {search_record['pos']}")
    print(f"目标变体集合: {search_record['target_variant_set']}")
    print(f"实际命中变体: {search_record['actual_variant_set']}")
    print(f"搜索结果数量: {search_record['result_count']}")
    
    # 输出所有结果
    print("\n=== 搜索结果 ===")
    for i, result in enumerate(search_record['search_results']):
        print(f"结果 {i+1}:")
        print(f"  内容: {result['content']}")
        print(f"  行号: {result['lineno']}")
        
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()

# 清理测试文件
import os
if os.path.exists("test_kor.txt"):
    os.remove("test_kor.txt")
    print("\n测试文件已清理")
