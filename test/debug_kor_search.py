#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试韩语搜索功能
"""

from function.search_engine_kor import KoreanSearchEngine


def debug_korean_search():
    """调试韩语搜索功能"""
    # 初始化搜索引擎
    engine = KoreanSearchEngine()
    print("初始化搜索引擎成功")
    
    # 测试动词变形匹配
    print("\n=== 调试: 动词变形匹配（输入: 속아）===")
    
    # 手动解析文件，查看解析结果
    from pathlib import Path
    from function.document_parser import parse_document_file
    
    file_path = 'test/test_kor.txt'
    try:
        parsed_data = parse_document_file(file_path)
        print(f"解析成功！共 {len(parsed_data)} 条数据")
        for i, item in enumerate(parsed_data):
            print(f"\n第 {i+1} 条数据:")
            print(f"  content: {item.get('content', '')}")
            print(f"  episode: {item.get('episode', '')}")
            print(f"  time_axis: {item.get('time_axis', '')}")
    except Exception as e:
        print(f"解析失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试单个句子的分析
    print("\n=== 测试句子分析 ===")
    test_sentence = "그가 나를 속였어."
    try:
        analyzed = engine.kiwi.analyze(test_sentence)
        print(f"句子 '{test_sentence}' 的分析结果:")
        for analysis_result in analyzed:
            for token in analysis_result[0]:
                print(f"  - {token.form} ({token.tag}), 词典形={token.lemma}")
    except Exception as e:
        print(f"分析失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 运行搜索
    print("\n=== 运行搜索 ===")
    result = engine.search_korean_advanced(file_path, '속아')
    print(f"搜索记录: {result}")


if __name__ == "__main__":
    debug_korean_search()
