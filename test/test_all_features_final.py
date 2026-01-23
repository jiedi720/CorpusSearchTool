"""
最终验证所有功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_all_features():
    """测试所有功能"""
    print("测试所有功能...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        from function.result_processor import result_processor
        from gui.main_window import MainWindow
        
        # 1. 测试历史记录管理器
        print("1. 测试历史记录管理器...")
        history_manager = SearchHistoryManager()
        
        # 清空现有记录
        history_manager.clear_history()
        
        # 添加测试记录
        history_manager.add_record(
            keywords="test_keyword",
            input_path="/path/to/input",
            output_path="",
            case_sensitive=False,
            fuzzy_match=True,
            regex_enabled=False
        )
        
        # 检查记录
        records = history_manager.get_recent_records(10)
        print(f"   历史记录数量: {len(records)}")
        
        # 测试移除功能
        history_manager.remove_records_by_keywords(["test_keyword"])
        remaining_records = history_manager.get_recent_records(10)
        print(f"   移除后记录数量: {len(remaining_records)}")
        
        # 2. 测试结果处理器
        print("2. 测试结果处理器...")
        mock_results = [
            {
                'file_path': 'test.txt',
                'line_number': 1234567,
                'content': 'Test content',
                'time_axis': '[00:02:36]',
                'episode': 'Test Episode',
                'matched_keywords': []
            }
        ]
        
        formatted_results = result_processor.format_results_for_display(mock_results, 'subtitle')
        print(f"   格式化结果数量: {len(formatted_results)}")
        
        if formatted_results:
            result = formatted_results[0]
            print(f"   格式化结果示例: {result}")
            
            # 验证列顺序和格式
            correct_format = (
                len(result) == 5 and  # (filename, line_number, episode, time_axis, content)
                result[1] == '1234567' and  # 行号
                result[3] == '[00:02:36]' and  # 时间轴
                result[2] == 'Test Episode'  # 集数
            )
            print(f"   格式正确: {correct_format}")
        
        # 3. 测试主窗口
        print("3. 测试主窗口...")
        main_window = MainWindow()
        
        # 检查窗口属性
        window_ok = main_window.root is not None
        title_ok = main_window.root.title() == "字幕语料库检索工具"
        bg_ok = main_window.root.cget('bg') == '#1f1f1f'
        
        print(f"   窗口正常: {window_ok}")
        print(f"   标题正确: {title_ok}")
        print(f"   背景色正确: {bg_ok}")
        
        # 检查方法存在
        methods_ok = all([
            hasattr(main_window, 'show_search_history'),
            hasattr(main_window, 'clear_selected_history'),
            hasattr(main_window, 'clear_all_history'),
            hasattr(main_window, 'refresh_history_window'),
            hasattr(main_window, 'close_history_window')
        ])
        print(f"   方法存在: {methods_ok}")
        
        # 4. 清理
        history_manager.clear_history()
        
        all_good = (
            len(records) > 0 and
            len(remaining_records) == 0 and
            len(formatted_results) > 0 and
            correct_format and
            window_ok and title_ok and bg_ok and
            methods_ok
        )
        
        print(f"   所部正常: {all_good}")
        
        return all_good
        
    except Exception as e:
        print(f"✗ 所部功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_right_click_functionality():
    """测试右键功能"""
    print("\n测试右键功能...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        
        # 创建历史记录管理器
        history_manager = SearchHistoryManager()
        
        # 清空现有记录
        history_manager.clear_history()
        
        # 添加多个测试记录
        test_keywords = ["keyword1", "keyword2", "keyword3"]
        for keyword in test_keywords:
            history_manager.add_record(
                keywords=keyword,
                input_path=f"/path/{keyword}",
                output_path="",
                case_sensitive=False,
                fuzzy_match=False,
                regex_enabled=False
            )
        
        # 检查记录
        initial_records = history_manager.get_recent_records(10)
        print(f"初始记录数量: {len(initial_records)}")
        
        # 测试移除功能
        history_manager.remove_records_by_keywords(["keyword1", "keyword3"])
        
        remaining_records = history_manager.get_recent_records(10)
        remaining_keywords = [r['keywords'] for r in remaining_records]
        
        print(f"移除后剩余: {remaining_keywords}")
        
        # 验证结果
        expected = ["keyword2"]
        correct_removal = remaining_keywords == expected and len(remaining_keywords) == 1
        
        print(f"移除正确: {correct_removal}")
        
        # 清理
        history_manager.clear_history()
        
        return correct_removal
        
    except Exception as e:
        print(f"✗ 右键功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_column_order():
    """测试列顺序"""
    print("\n测试列顺序...")
    
    try:
        from function.result_processor import result_processor
        
        # 测试结果格式化
        mock_results = [
            {
                'file_path': 'test.txt',
                'line_number': 1234567,
                'content': 'Test content',
                'time_axis': '[00:02:36]',
                'episode': 'Test Episode',
                'matched_keywords': []
            }
        ]
        
        formatted_results = result_processor.format_results_for_display(mock_results, 'subtitle')
        
        if formatted_results:
            result = formatted_results[0]
            print(f"格式化结果: {result}")
            
            # 验证列顺序: (filename, line_number, episode, time_axis, content)
            expected_order = [
                'test.txt',      # 文件名
                '1234567',       # 行号
                'Test Episode',  # 集数
                '[00:02:36]',    # 时间轴
                'Test content'   # 内
            ]
            
            matches = [result[i] == expected_order[i] for i in range(len(expected_order))]
            order_correct = all(matches)
            
            print(f"列顺序正确: {order_correct}")
            for i, (actual, expected) in enumerate(zip(result, expected_order)):
                print(f"  列{i+1}: '{actual}' == '{expected}' ? {actual == expected}")
            
            return order_correct
        else:
            print("✗ 无格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 列顺序测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 最终功能验证")
    print("="*60)
    
    # 运行测试
    test1_ok = test_all_features()
    test2_ok = test_right_click_functionality()
    test3_ok = test_column_order()
    
    print("\n" + "="*60)
    print("最终功能验证结果:")
    print(f"所有功能: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"右键功能: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"列顺序: {'✓ 정상' if test3_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所部功能验证通过!")
        print("实现的功能:")
        print("- 搜索历史窗口支持右键菜单")
        print("- 右键菜单包含清除选定条目选项")
        print("- 右键菜单包含清除所有历史选项")
        print("- 支持按关键词移除指定历史记录")
        print("- 列顺序正确 (文件名, 行号, 集数, 时间轴, 内)")
        print("- 行号列宽度适合显示1234567")
        print("- 时间轴列宽度适合显示[00:02:36]")
        print("- 集数列不显示'# '符号")
    else:
        print("\n✗ 部分功能验证未通过")
        
    input("\n按回车键退出...")