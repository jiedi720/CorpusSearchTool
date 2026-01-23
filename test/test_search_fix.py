"""
测试搜索功能修复
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_korean_search():
    """测试韩语搜索功能"""
    print("正在测试韩语搜索功能...")
    
    # 创建一个测试文件
    test_file = "test_korean.txt"
    test_content = """전들아 아직도 뻣뻣하네?
오늘 날씨가 좋네요.
그는 아직도 학교에 가지 않았다.
아직도 그 일을 기억하고 있어.
오늘도 좋은 하루입니다."""
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        # 测试搜索
        from function.search_engine import search_engine
        
        # 搜索"아직도"，应该只返回包含"아직도"的行
        results = search_engine.search_in_file(test_file, "아직도")
        
        print(f"搜索'아직도'的结果数量: {len(results)}")
        for i, result in enumerate(results, 1):
            print(f"  {i}. 行号: {result['line_number']}, 内容: {result['content']}")
        
        # 验证结果是否真的包含关键词
        for result in results:
            content = result['content']
            if "아직도" not in content:
                print(f"  错误：结果中不包含关键词 '아직도': {content}")
                return False
        
        print("✓ 韩语搜索功能测试通过!")
        
        # 测试韩语变形匹配
        print("\n测试韩语变形匹配...")
        variant_results = search_engine.search_korean_english_variants(test_file, ["하다"])
        
        print(f"搜索'하다'变形的结果数量: {len(variant_results)}")
        for i, result in enumerate(variant_results, 1):
            print(f"  {i}. 行号: {result['line_number']}, 内容: {result['content']}")
        
        print("✓ 韩语变形匹配测试通过!")
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


def test_search_accuracy():
    """测试搜索准确性"""
    print("\n正在测试搜索准确性...")
    
    # 创建一个测试文件
    test_file = "test_accuracy.txt"
    test_content = """전들아 아직도 뻣뻣하네?
이 문장은 키워드를 포함하지 않습니다.
아직도 그녀는 오지 않았다.
오늘도 날씨가 좋다.
그는 아직도 기다리고 있다."""
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        from function.search_engine import search_engine
        
        # 搜索"아직도"，应该只返回包含"아직도"的行
        results = search_engine.search_in_file(test_file, "아직도")
        
        print(f"搜索'아직도'的结果数量: {len(results)}")
        for i, result in enumerate(results, 1):
            content = result['content']
            print(f"  {i}. 内容: {content}")
            
            # 验证每一行都包含关键词
            if "아직도" not in content:
                print(f"  错误：结果中不包含关键词 '아직도': {content}")
                return False
        
        print("✓ 搜索准确性测试通过!")
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
    print("字幕语料库检索工具 - 搜索功能修复测试")
    print("="*50)
    
    # 运行测试
    test1_ok = test_korean_search()
    test2_ok = test_search_accuracy()
    
    print("\n" + "="*50)
    print("测试结果:")
    print(f"韩语搜索: {'✓ 正常' if test1_ok else '✗ 异常'}")
    print(f"搜索准确性: {'✓ 正常' if test2_ok else '✗ 异常'}")
    
    if test1_ok and test2_ok:
        print("\n✓ 所有搜索功能测试通过!")
    else:
        print("\n✗ 部分功能存在问题，请检查上述错误信息")
        
    input("\n按回车键退出...")