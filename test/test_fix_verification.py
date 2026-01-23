"""
测试修复后的功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_episode_detection():
    """测试集数检测功能"""
    print("正在测试集数检测功能...")
    
    # 创建一个包含集数信息的测试文件
    test_file = "test_episode.txt"
    test_content = """第1集：开场
这是第一句台词
主角登场
第2集：发展
剧情继续
第3集：结尾
最终台词"""
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        # 测试解析
        from function.document_parser import TxtParser
        parser = TxtParser()
        results = parser.parse(test_file)
        
        print(f"解析结果数量: {len(results)}")
        
        for i, result in enumerate(results, 1):
            print(f"  {i}. 行号: {result['line_number']}, 集数: {result['episode']}, 内容: {result['content']}")
        
        # 验证集数是否正确识别
        episodes_found = set()
        for result in results:
            if result['episode'] != '未知集数':
                episodes_found.add(result['episode'])
        
        if len(episodes_found) > 0:
            print(f"✓ 集数检测功能正常工作，找到集数: {episodes_found}")
            return True
        else:
            print("✗ 集数检测功能可能有问题")
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


def test_search_with_episodes():
    """测试带集数信息的搜索"""
    print("\n正在测试带集数信息的搜索...")
    
    # 创建一个包含集数信息的测试文件
    test_file = "test_search_episodes.txt"
    test_content = """第1集：开场
这是第一句台词
主角登场
第2集：发展
剧情继续
台词内容
第3集：结尾
最终台词"""
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        from function.search_engine import search_engine
        
        # 搜索"台词"
        results = search_engine.search_in_file(test_file, "台词")
        
        print(f"搜索'台词'的结果数量: {len(results)}")
        for i, result in enumerate(results, 1):
            print(f"  {i}. 行号: {result['line_number']}, 集数: {result.get('episode', '未知集数')}, 内容: {result['content']}")
        
        # 验证结果是否包含集数信息
        episodes_present = all('episode' in result for result in results)
        
        if episodes_present and len(results) > 0:
            print("✓ 带集数信息的搜索功能正常工作!")
            return True
        else:
            print("✗ 带集数信息的搜索功能可能有问题")
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


def test_result_formatting():
    """测试结果格式化功能"""
    print("\n正在测试结果格式化功能...")
    
    try:
        from function.result_processor import result_processor
        
        # 模拟搜索结果，包含集数信息
        mock_results = [
            {
                'file_path': 'test.txt',
                'line_number': 2,
                'content': '这是第一个场景的对话',
                'time_axis': '[00:00:49]',
                'episode': '第1集'
            },
            {
                'file_path': 'test.txt',
                'line_number': 3,
                'content': '第二个场景开始',
                'time_axis': '[00:01:32]',
                'episode': '第2集'
            },
            {
                'file_path': 'test_doc.txt',
                'line_number': 1,
                'content': '文档内容',
                'episode': '第3集'
            }
        ]
        
        # 测试字幕格式
        formatted_subtitle = result_processor.format_results_for_display(mock_results[:2], 'subtitle')
        print("字幕格式化结果:")
        for i, result in enumerate(formatted_subtitle, 1):
            print(f"  {i}. {result}")
        
        # 测试文档格式
        formatted_document = result_processor.format_results_for_display(mock_results[2:], 'document')
        print("文档格式化结果:")
        for i, result in enumerate(formatted_document, 1):
            print(f"  {i}. {result}")
        
        print("✓ 结果格式化功能正常工作!")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 功能修复测试")
    print("="*50)
    
    # 运行测试
    test1_ok = test_episode_detection()
    test2_ok = test_search_with_episodes()
    test3_ok = test_result_formatting()
    
    print("\n" + "="*50)
    print("测试结果:")
    print(f"集数检测: {'✓ 正常' if test1_ok else '✗ 异常'}")
    print(f"带集数搜索: {'✓ 正常' if test2_ok else '✗ 异常'}")
    print(f"结果格式化: {'✓ 正常' if test3_ok else '✗ 异常'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有功能修复测试通过!")
    else:
        print("\n✗ 部分功能仍存在问题，请检查上述错误信息")
        
    input("\n按回车键退出...")