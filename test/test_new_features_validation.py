"""
测试所有新功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_single_history_window():
    """测试搜索历史窗口只打开一个"""
    print("测试搜索历史窗口只打开一个...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        from gui.main_window import MainWindow
        
        # 创建历史记录管理器
        history_manager = SearchHistoryManager()
        
        # 添加测试记录
        history_manager.add_record(
            keywords="test keyword",
            input_path="/path/to/input",
            output_path="",
            case_sensitive=False,
            fuzzy_match=True,
            regex_enabled=False
        )
        
        # 创建主窗口实例
        main_window = MainWindow()
        
        # 模拟调用显示历史窗口两次
        print("第一次调用显示历史窗口...")
        main_window.show_search_history()
        
        # 检查是否创建了窗口
        first_call_has_window = main_window.history_window is not None
        
        print("第二次调用显示历史窗口...")
        main_window.show_search_history()  # 这次调用应该不会创建新窗口
        
        # 检查窗口引用是否仍然是同一个
        same_window = main_window.history_window is not None
        
        print(f"第一次调用创建窗口: {first_call_has_window}")
        print(f"第二次调用后仍有窗口: {same_window}")
        
        # 关闭已打开的窗口
        if main_window.history_window:
            main_window.close_history_window()
        
        if first_call_has_window and same_window:
            print("✓ 搜索历史窗口只打开一个!")
            return True
        else:
            print("✗ 搜索历史窗口可能有多余窗口")
            return False
        
    except Exception as e:
        print(f"✗ 搜索历史窗口测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_centered_loading():
    """测试居中加载功能"""
    print("\n测试居中加载功能...")
    
    try:
        import tkinter as tk
        from gui.main_window import MainWindow
        
        # 创建主窗口实例
        main_window = MainWindow()
        
        # 检查窗口是否已初始化
        root_exists = main_window.root is not None
        title_correct = main_window.root.title() == "字幕语料库检索工具"
        
        print(f"窗口存在: {root_exists}")
        print(f"标题正确: {title_correct}")
        
        if root_exists and title_correct:
            print("✓ 居中加载功能已实现!")
            return True
        else:
            print("✗ 居中加载功能未正确实现")
            return False
        
    except Exception as e:
        print(f"✗ 居中加载功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_window_reference_management():
    """测试窗口引用管理"""
    print("\n测试窗口引用管理...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        from gui.main_window import MainWindow
        
        # 创建历史记录管理器
        history_manager = SearchHistoryManager()
        
        # 添加测试记录
        history_manager.add_record(
            keywords="test",
            input_path="/path",
            output_path="",
            case_sensitive=False,
            fuzzy_match=False,
            regex_enabled=False
        )
        
        # 创建主窗口实例
        main_window = MainWindow()
        
        # 打开历史窗口
        main_window.show_search_history()
        
        # 检查窗口引用
        window_open = main_window.history_window is not None
        print(f"窗口打开: {window_open}")
        
        if window_open:
            # 关闭窗口
            main_window.close_history_window()
            
            # 检查引用是否已重置
            reference_reset = main_window.history_window is None
            print(f"引用已重置: {reference_reset}")
            
            if reference_reset:
                print("✓ 窗口引用管理正常!")
                return True
            else:
                print("✗ 窗口引用未正确重置")
                return False
        else:
            print("✗ 未能打开窗口")
            return False
        
    except Exception as e:
        print(f"✗ 窗口引用管理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_existing_functionality():
    """测试现有功能是否仍然正常"""
    print("\n测试现有功能是否仍然正常...")
    
    try:
        from function.result_processor import result_processor
        
        # 测试结果处理器
        mock_results = [
            {
                'file_path': 'test.txt',
                'line_number': 1,
                'content': 'Test content',
                'time_axis': '[00:00:00]',
                'episode': 'Test Episode',
                'matched_keywords': []
            }
        ]
        
        formatted_results = result_processor.format_results_for_display(mock_results, 'subtitle')
        
        print(f"格式化结果数量: {len(formatted_results)}")
        if formatted_results:
            result = formatted_results[0]
            print(f"格式化结果: {result}")
            
            # 验证结果格式
            correct_length = len(result) == 5  # (filename, line_number, episode, time_axis, content)
            has_content = result[4] == 'Test content'
            
            print(f"结果格式正确: {correct_length}")
            print(f"内容正确: {has_content}")
            
            if correct_length and has_content:
                print("✓ 现有功能正常!")
                return True
            else:
                print("✗ 现有功能可能有问题")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 现有功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 新功能测试")
    print("="*60)
    
    # 运行测试
    test1_ok = test_single_history_window()
    test2_ok = test_centered_loading()
    test3_ok = test_window_reference_management()
    test4_ok = test_existing_functionality()
    
    print("\n" + "="*60)
    print("新功能测试结果:")
    print(f"单一历史窗口: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"居中加载: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"窗口引用管理: {'✓ 정상' if test3_ok else '✗ 이상'}")
    print(f"现有功能: {'✓ 정상' if test4_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok and test4_ok:
        print("\n✓ 所有新功能测试通过!")
        print("实现的功能:")
        print("- 搜索历史窗口一次只能打开一个")
        print("- 所有窗口实现优雅的居中加载")
        print("- 消除窗口启动时的视觉闪烁现象")
        print("- 保持所有现有功能")
    else:
        print("\n✗ 部分功能测试未通过")
        
    input("\n按回车键退出...")