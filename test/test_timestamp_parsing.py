"""
测试带时间戳的文本文件解析功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_timestamp_parsing():
    """测试时间戳解析功能"""
    print("正在测试时间戳解析功能...")
    
    # 创建一个测试文件
    test_file = "test_timestamp.txt"
    test_content = """[00:00:00] 开场白
[00:00:49] 这是第一个场景的对话
[00:01:32] 第二个场景开始
[00:02:15] 继续对话内容
[01:23:45] 结尾部分"""
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        # 测试解析
        from function.subtitle_parser import TimestampParser
        parser = TimestampParser()
        results = parser.parse(test_file)
        
        print(f"解析结果数量: {len(results)}")
        
        for i, result in enumerate(results, 1):
            print(f"  {i}. 时间轴: {result['time_axis']}, 内容: {result['content']}")
        
        # 测试搜索功能
        from function.search_engine_base import search_engine
        search_results = search_engine.search_in_file(test_file, "场景")
        
        print(f"\n搜索'场景'的结果数量: {len(search_results)}")
        for i, result in enumerate(search_results, 1):
            print(f"  {i}. 时间轴: {result.get('time_axis', 'N/A')}, 内容: {result['content']}")
        
        print("\n✓ 时间戳解析功能测试通过!")
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


def test_result_formatting():
    """测试结果格式化功能"""
    print("\n正在测试结果格式化功能...")
    
    try:
        from function.result_processor import result_processor
        
        # 模拟搜索结果，包含时间轴信息
        mock_results = [
            {
                'file_path': 'test.txt',
                'line_number': 2,
                'content': '这是第一个场景的对话 [00:00:49]',
                'time_axis': '[00:00:49]'
            },
            {
                'file_path': 'test.txt',
                'line_number': 3,
                'content': '第二个场景开始 [00:01:32]',
                'time_axis': '[00:01:32]'
            }
        ]
        
        formatted = result_processor.format_results_for_display(mock_results, 'subtitle')
        
        print("格式化结果:")
        for i, result in enumerate(formatted, 1):
            print(f"  {i}. {result}")
        
        print("\n✓ 结果格式化功能测试通过!")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 时间戳功能测试")
    print("="*50)
    
    # 运行测试
    test1_ok = test_timestamp_parsing()
    test2_ok = test_result_formatting()
    
    print("\n" + "="*50)
    print("测试结果:")
    print(f"时间戳解析: {'✓ 正常' if test1_ok else '✗ 异常'}")
    print(f"结果格式化: {'✓ 正常' if test2_ok else '✗ 异常'}")
    
    if test1_ok and test2_ok:
        print("\n✓ 所有时间戳相关功能测试通过!")
    else:
        print("\n✗ 部分功能存在问题，请检查上述错误信息")
        
    input("\n按回车键退出...")