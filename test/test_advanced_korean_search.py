#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试高级韩语搜索功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from function.search_engine_kor import KoreanSearchEngine

def test_advanced_korean_search():
    """测试高级韩语搜索功能"""
    print("测试高级韩语搜索功能...")
    
    # 创建测试文件
    test_file = "test_korean_advanced.md"
    content = """# Death's Game S01E01
[00:02:35] 이전 장면
[00:02:36] 현주 병원 갔잖아
[00:02:37] 다음 장면

# Death's Game S01E02
[00:05:12] 그는 집에 갔어요
[00:05:13] 그녀는 학교에 갔어
[00:05:14] 저는 도서관에 갔어요
"""
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    try:
        # 创建搜索引擎实例
        search_engine = KoreanSearchEngine()
        
        # 测试1：动词原形搜索
        print("\n测试1：动词原形 '가다' 搜索")
        result1 = search_engine.search_korean_advanced(test_file, "가다")
        print(f"  搜索记录: {result1}")
        print(f"  结果数量: {result1['result_count']}")
        print(f"  词典形: {result1['lemma']}")
        print(f"  实际命中变体: {result1['actual_variant_set']}")
        
        # 测试2：动词活用形搜索
        print("\n测试2：动词活用形 '갔잖아' 搜索")
        result2 = search_engine.search_korean_advanced(test_file, "갔잖아")
        print(f"  搜索记录: {result2}")
        print(f"  结果数量: {result2['result_count']}")
        print(f"  词典形: {result2['lemma']}")
        print(f"  实际命中变体: {result2['actual_variant_set']}")
        
        # 测试3：名词搜索
        print("\n测试3：名词 '병원' 搜索")
        result3 = search_engine.search_korean_advanced(test_file, "병원")
        print(f"  搜索记录: {result3}")
        print(f"  结果数量: {result3['result_count']}")
        print(f"  词典形: {result3['lemma']}")
        print(f"  实际命中变体: {result3['actual_variant_set']}")
        
        print("\n测试完成！")
        
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    test_advanced_korean_search()
    input("\n按回车键退出...")