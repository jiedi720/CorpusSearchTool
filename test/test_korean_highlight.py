"""
测试韩语搜索结果高亮功能
验证词干形式（如 이루）能否被正确高亮
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from function.search_engine_kor import KoreanSearchEngine
from function.subtitle_parser import parse_subtitle_file
from function.document_parser import parse_document_file


def test_korean_highlight():
    """测试韩语搜索的高亮功能"""

    # 创建测试数据
    test_content = """
    这个故事开始于很久以前。
    人们开始이루어梦想。
    很多人想要이뤄目标。
    他们努力이루었다自己的理想。
    这就是이루的意义。
    """

    # 创建临时测试文件
    test_file = "test_highlight_kor.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)

    print("=== 测试韩语搜索高亮功能 ===\n")

    # 测试搜索动词原形
    keyword = "이루다"
    print(f"搜索关键词: {keyword}")

    # 创建搜索引擎实例
    engine = KoreanSearchEngine()

    # 执行搜索
    search_record = engine.search_korean_advanced(test_file, keyword)

    # 输出搜索结果
    print(f"\n词典形 (lemma): {search_record['lemma']}")
    print(f"词性: {search_record['pos']}")
    print(f"\n目标变体集合 (target_variant_set):")
    for variant in search_record['target_variant_set']:
        print(f"  - {variant}")

    print(f"\n实际匹配的变体 (actual_variant_set):")
    for variant in search_record['actual_variant_set']:
        print(f"  - {variant}")

    print(f"\n所有匹配的词 (matched_terms_set):")
    if 'matched_terms_set' in search_record:
        for term in search_record['matched_terms_set']:
            print(f"  - {term}")
    else:
        print("  (未找到 matched_terms_set 字段)")

    print(f"\n搜索结果数量: {search_record['result_count']}")
    print("\n搜索结果:")
    for i, result in enumerate(search_record['search_results'], 1):
        print(f"\n{i}. 文件: {result['file_path']}")
        print(f"   行号: {result['lineno']}")
        print(f"   内容: {result['content']}")
        print(f"   匹配关键词: {result['matched_keyword']}")

    # 验证词干形式是否在 matched_terms_set 中
    if 'matched_terms_set' in search_record:
        stem = "이루"  # 词干形式
        if stem in search_record['matched_terms_set']:
            print(f"\n✓ 成功：词干形式 '{stem}' 已包含在 matched_terms_set 中")
        else:
            print(f"\n✗ 失败：词干形式 '{stem}' 未包含在 matched_terms_set 中")
    else:
        print("\n✗ 失败：matched_terms_set 字段不存在")

    # 清理测试文件
    try:
        os.remove(test_file)
        print(f"\n已清理测试文件: {test_file}")
    except:
        pass


if __name__ == "__main__":
    test_korean_highlight()
