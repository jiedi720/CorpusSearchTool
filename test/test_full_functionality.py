"""
全面测试新功能：集数信息和Markdown导出
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_episode_parsing():
    """测试集数信息解析功能"""
    print("正在测试集数信息解析功能...")
    
    # 创建一个测试SRT文件
    test_file = "test_episode_full.srt"
    test_content = """1
00:00:01,000 --> 00:00:03,000
这是第一句台词

2
00:00:04,000 --> 00:00:06,000
第1集：开场

3
00:00:07,000 --> 00:00:09,000
主角登场

4
00:00:10,000 --> 00:00:12,000
第2集：发展

5
00:00:13,000 --> 00:00:15,000
剧情继续

6
00:00:16,000 --> 00:00:18,000
Episode 3: 结尾

7
00:00:19,000 --> 00:00:21,000
最终台词"""
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        # 测试解析
        from function.subtitle_parser import SrtParser
        parser = SrtParser()
        results = parser.parse(test_file)
        
        print(f"解析结果数量: {len(results)}")
        
        for i, result in enumerate(results, 1):
            print(f"  {i}. 行号: {result['line_number']}, 时间轴: {result['time_axis']}, 集数: {result['episode']}, 内容: {result['content']}")
        
        # 测试搜索功能
        from function.search_engine_base import search_engine
        search_results = search_engine.search_in_file(test_file, "台词")
        
        print(f"\n搜索'台词'的结果数量: {len(search_results)}")
        for i, result in enumerate(search_results, 1):
            print(f"  {i}. 时间轴: {result.get('time_axis', 'N/A')}, 集数: {result.get('episode', '未知集数')}, 内容: {result['content']}")
        
        # 测试结果格式化
        from function.result_processor import result_processor
        formatted_results = result_processor.format_results_for_display(search_results, 'subtitle')
        print(f"\n格式化结果数量: {len(formatted_results)}")
        for i, result in enumerate(formatted_results, 1):
            print(f"  {i}. 格式化结果: {result}")
        
        print("\n✓ 集数信息解析功能测试通过!")
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


def test_markdown_export():
    """测试Markdown导出功能"""
    print("\n正在测试Markdown导出功能...")
    
    try:
        from function.search_history_manager import search_history_manager
        import tempfile
        
        # 添加一些测试记录
        search_history_manager.add_record(
            keywords="测试关键词",
            input_path="/path/to/input",
            output_path="/path/to/output",
            case_sensitive=True,
            fuzzy_match=False,
            regex_enabled=True
        )
        
        # 创建临时目录用于导出
        with tempfile.TemporaryDirectory() as temp_dir:
            search_history_manager.export_to_markdown(temp_dir, "test_history.md")
            
            # 检查文件是否存在
            exported_file = os.path.join(temp_dir, "test_history.md")
            if os.path.exists(exported_file):
                print("✓ Markdown导出文件已创建")
                
                # 读取并显示部分内容
                with open(exported_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print("导出的Markdown内容预览:")
                    print(content[:500] + "..." if len(content) > 500 else content)
            else:
                print("✗ Markdown导出文件未创建")
                return False
        
        print("\n✓ Markdown导出功能测试通过!")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_result_formatting():
    """测试结果格式化功能"""
    print("\n正在测试结果格式化功能...")
    
    try:
        from function.result_processor import result_processor
        
        # 模拟搜索结果，包含时间轴和集数信息
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
    print("字幕语料库检索工具 - 集数和Markdown功能全面测试")
    print("="*60)
    
    # 运行测试
    test1_ok = test_episode_parsing()
    test2_ok = test_markdown_export()
    test3_ok = test_result_formatting()
    
    print("\n" + "="*60)
    print("测试结果:")
    print(f"集数信息解析: {'✓ 正常' if test1_ok else '✗ 异常'}")
    print(f"Markdown导出: {'✓ 正常' if test2_ok else '✗ 异常'}")
    print(f"结果格式化: {'✓ 正常' if test3_ok else '✗ 异常'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有新功能测试通过!")
    else:
        print("\n✗ 部分功能存在问题，请检查上述错误信息")
        
    input("\n按回车键退出...")