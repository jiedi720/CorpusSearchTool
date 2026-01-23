"""
全面测试搜索功能修复
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_original_issue():
    """测试原始问题是否已修复"""
    print("正在测试原始问题修复...")
    
    # 创建一个包含韩语内容的测试文件
    test_file = "test_original_issue.txt"
    test_content = """전들아 아직도 뻣뻣하네?
이 문장은 아직도 중요하다.
오늘도 날씨가 좋다.
그는 아직도 기다리고 있다.
이것은 키워드와 관련 없는 문장입니다."""
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        from function.search_engine import search_engine
        
        # 搜索"아직도"，应该只返回包含"아직도"的行
        results = search_engine.search_in_file(test_file, "아직도")
        
        print(f"搜索'아직도'的结果数量: {len(results)}")
        for i, result in enumerate(results, 1):
            content = result['content']
            print(f"  {i}. 行号: {result['line_number']}, 内容: {content}")
            
            # 验证每一行都包含关键词
            if "아직도" not in content:
                print(f"  错误：结果中不包含关键词 '아직도': {content}")
                return False
        
        # 验证没有返回不相关的行
        unrelated_found = False
        for result in results:
            content = result['content']
            if "전들아" in content and "아직도" not in content:
                print(f"  错误：返回了不相关的行: {content}")
                unrelated_found = True
        
        if not unrelated_found:
            print("✓ 原始问题已修复！")
            return True
        else:
            print("✗ 原始问题未完全修复")
            return False
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)


def test_korean_variants():
    """测试韩语变形匹配"""
    print("\n正在测试韩语变形匹配...")
    
    # 创建一个包含韩语变形的测试文件
    test_file = "test_korean_variants.txt"
    test_content = """나는 학교에 간다.
학교에 가지 않았다.
그는 가고 있다.
우리는 갈 것이다.
그녀는 가지 않는다.
모든 문장은 '가다'의 변형을 포함합니다."""
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        from function.search_engine import search_engine
        
        # 使用韩语变形匹配搜索"가다"
        results = search_engine.search_korean_english_variants(test_file, ["가다"])
        
        print(f"搜索'가다'变形的结果数量: {len(results)}")
        for i, result in enumerate(results, 1):
            content = result['content']
            print(f"  {i}. 行号: {result['line_number']}, 内容: {content}")
        
        # 验证是否找到了包含变形词的行
        expected_matches = ["가지 않았다", "가고 있다", "갈 것이다", "가지 않는다"]
        found_expected = 0
        
        for result in results:
            content = result['content']
            for expected in expected_matches:
                if expected in content:
                    found_expected += 1
                    break
        
        if found_expected > 0:
            print("✓ 韩语变形匹配功能正常工作!")
            return True
        else:
            print("✗ 韩语变形匹配功能可能有问题")
            return False
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)


def test_mixed_content():
    """测试混合内容搜索"""
    print("\n正在测试混合内容搜索...")
    
    # 创建一个包含韩语和无关内容的测试文件
    test_file = "test_mixed_content.txt"
    test_content = """전들아 아직도 뻣뻣하네?
이건 테스트 문장입니다.
아직도 그녀는 오지 않았다.
이 문장은 관련이 없습니다.
그는 아직도 기다리고 있다.
오늘 날씨가 좋다.
아직도 시간이 남았다."""
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        from function.search_engine import search_engine
        
        # 搜索"아직도"
        results = search_engine.search_in_file(test_file, "아직도")
        
        print(f"搜索'아직도'的结果数量: {len(results)}")
        for i, result in enumerate(results, 1):
            content = result['content']
            print(f"  {i}. 行号: {result['line_number']}, 内容: {content}")
            
            # 验证每一行都包含关键词
            if "아직도" not in content:
                print(f"  错误：结果中不包含关键词 '아직도': {content}")
                return False
        
        # 确认没有返回不相关的行
        for result in results:
            content = result['content']
            if content == "이건 테스트 문장입니다." or content == "이 문장은 관련이 없습니다." or content == "오늘 날씨가 좋다.":
                print(f"  错误：返回了不相关的行: {content}")
                return False
        
        print("✓ 混合内容搜索功能正常工作!")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == "__main__":
    print("字幕语料库检索工具 - 搜索功能修复全面测试")
    print("="*60)
    
    # 运行测试
    test1_ok = test_original_issue()
    test2_ok = test_korean_variants()
    test3_ok = test_mixed_content()
    
    print("\n" + "="*60)
    print("测试结果:")
    print(f"原始问题修复: {'✓ 正常' if test1_ok else '✗ 异常'}")
    print(f"韩语变形匹配: {'✓ 正常' if test2_ok else '✗ 异常'}")
    print(f"混合内容搜索: {'✓ 正常' if test3_ok else '✗ 异常'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有搜索功能修复测试通过!")
        print("原始问题'전들아 아직도 뻣뻣하네?'不应出现在'아직도'的搜索结果中，现已修复!")
    else:
        print("\n✗ 部分功能仍存在问题，请检查上述错误信息")
        
    input("\n按回车键退出...")