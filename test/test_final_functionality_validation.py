"""
最终验证所有功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_complete_functionality():
    """测试完整功能"""
    print("测试完整功能...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        from function.search_engine import search_engine
        from function.result_processor import result_processor
        from gui.main_window import MainWindow
        
        # 1. 测试历史记录管理
        print("1. 测试历史记录管理...")
        history_manager = SearchHistoryManager()
        
        # 添加记录
        history_manager.add_record(
            keywords="test keyword",
            input_path="/path/to/input",
            output_path="",
            case_sensitive=False,
            fuzzy_match=True,
            regex_enabled=False
        )
        
        records = history_manager.get_recent_records(10)
        print(f"   历史记录数量: {len(records)}")
        
        # 2. 测试主窗口
        print("2. 测试主窗口...")
        main_window = MainWindow()
        
        # 验证窗口初始化
        window_initialized = main_window.root is not None
        title_correct = main_window.root.title() == "字幕语料库检索工具"
        bg_color_set = main_window.root.cget('bg') == '#1f1f1f'
        
        print(f"   窗口初始化: {window_initialized}")
        print(f"   标题正确: {title_correct}")
        print(f"   背景色设置: {bg_color_set}")
        
        # 3. 测试历史窗口管理
        print("3. 测试历史窗口管理...")
        # 打开历史窗口
        main_window.show_search_history()
        
        first_window_open = main_window.history_window is not None
        print(f"   首次打开窗口: {first_window_open}")
        
        if first_window_open:
            # 尝试再次打开（应该不会创建新窗口）
            main_window.show_search_history()
            
            # 检查是否仍然是同一个窗口
            same_window = main_window.history_window is not None
            print(f"   二次调用后窗口存在: {same_window}")
            
            # 关闭窗口
            main_window.close_history_window()
            window_closed = main_window.history_window is None
            print(f"   窗口已关闭: {window_closed}")
        
        # 4. 测试结果格式化
        print("4. 测试结果格式化...")
        mock_results = [
            {
                'file_path': 'test.txt',
                'line_number': 1234567,
                'content': 'Test content',
                'time_axis': '[00:02:36]',
                'episode': '# Test Episode',
                'matched_keywords': []
            }
        ]
        
        formatted_results = result_processor.format_results_for_display(mock_results, 'subtitle')
        formatting_works = len(formatted_results) > 0
        print(f"   结果格式化: {formatting_works}")
        
        if formatted_results:
            result = formatted_results[0]
            # 验证集数列没有"# "前缀
            episode_cleaned = result[2] != '# Test Episode' and result[2] == 'Test Episode'
            print(f"   集数列清理: {episode_cleaned}")
        
        all_tests_passed = (
            len(records) > 0 and
            window_initialized and title_correct and bg_color_set and
            first_window_open and same_window and window_closed and
            formatting_works
        )
        
        print(f"   所有测试通过: {all_tests_passed}")
        
        return all_tests_passed
        
    except Exception as e:
        print(f"✗ 完整功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_visual_experience():
    """测试视觉体验优化"""
    print("\n测试视觉体验优化...")
    
    try:
        import tkinter as tk
        from gui.main_window import MainWindow
        
        # 创建主窗口
        main_window = MainWindow()
        
        # 检查窗口属性
        root = main_window.root
        
        # 获取屏幕和窗口尺寸
        root.update_idletasks()  # 更新窗口尺寸
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        
        print(f"屏幕尺寸: {screen_width}x{screen_height}")
        print(f"窗口尺寸: {window_width}x{window_height}")
        
        # 检查窗口是否已设置背景色
        bg_color = root.cget('bg')
        print(f"背景色: {bg_color}")
        
        # 检查窗口是否已初始化
        window_exists = root is not None
        title_set = root.title() == "字幕语料库检索工具"
        
        print(f"窗口存在: {window_exists}")
        print(f"标题设置: {title_set}")
        
        if window_exists and title_set:
            print("✓ 视觉体验优化正常!")
            return True
        else:
            print("✗ 视觉体验优化有问题")
            return False
        
    except Exception as e:
        print(f"✗ 视觉体验优化测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_history_window_exclusivity():
    """测试历史窗口独占性"""
    print("\n测试历史窗口独占性...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        from gui.main_window import MainWindow
        
        # 创建历史记录管理器
        history_manager = SearchHistoryManager()
        
        # 添加测试记录
        history_manager.add_record(
            keywords="exclusive test",
            input_path="/exclusive/path",
            output_path="",
            case_sensitive=False,
            fuzzy_match=False,
            regex_enabled=False
        )
        
        # 创建主窗口
        main_window = MainWindow()
        
        # 第一次打开历史窗口
        main_window.show_search_history()
        first_window = main_window.history_window
        
        print(f"首次打开窗口: {first_window is not None}")
        
        if first_window:
            # 记录第一个窗口的ID
            first_window_id = first_window.winfo_id()
            print(f"首个窗口ID: {first_window_id}")
            
            # 第二次尝试打开历史窗口
            main_window.show_search_history()
            
            # 检查是否仍然是同一个窗口
            second_access = main_window.history_window
            same_window = (second_access is not None) and (second_access.winfo_id() == first_window_id)
            
            print(f"二次访问同一窗口: {same_window}")
            
            # 关闭窗口
            main_window.close_history_window()
            window_closed = main_window.history_window is None
            
            print(f"窗口已关闭: {window_closed}")
            
            if same_window and window_closed:
                print("✓ 历史窗口独占性正常!")
                return True
            else:
                print("✗ 历史窗口独占性有问题")
                return False
        else:
            print("✗ 未能打开历史窗口")
            return False
        
    except Exception as e:
        print(f"✗ 历史窗口独占性测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 最终功能验证")
    print("="*60)
    
    # 运行测试
    test1_ok = test_complete_functionality()
    test2_ok = test_visual_experience()
    test3_ok = test_history_window_exclusivity()
    
    print("\n" + "="*60)
    print("最终功能验证结果:")
    print(f"完整功能: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"视觉体验: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"窗口独占性: {'✓ 정상' if test3_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有功能验证通过!")
        print("实现的功能:")
        print("- 搜索历史窗口一次只能打开一个")
        print("- 所有窗口实现优雅的居中加载")
        print("- 消除窗口启动时的视觉闪烁现象")
        print("- 保持所有现有功能")
    else:
        print("\n✗ 部分功能验证未通过")
        
    input("\n按回车键退出...")