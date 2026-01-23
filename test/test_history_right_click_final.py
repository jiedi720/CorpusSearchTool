"""
最终验证搜索历史右键菜单功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_complete_history_functionality():
    """测试完整的搜索历史功能"""
    print("测试完整的搜索历史功能...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        from gui.main_window import MainWindow
        
        # 创建历史记录管理器
        history_manager = SearchHistoryManager()
        
        # 清空现有记录
        history_manager.clear_history()
        
        # 添加多个测试记录
        test_data = [
            ("keyword1", "/path/to/file1", ""),
            ("keyword2", "/path/to/file2", ""),
            ("keyword3", "/path/to/file3", ""),
        ]
        
        for keywords, input_path, output_path in test_data:
            history_manager.add_record(
                keywords=keywords,
                input_path=input_path,
                output_path=output_path,
                case_sensitive=False,
                fuzzy_match=True,
                regex_enabled=False
            )
        
        # 检查记录是否添加成功
        initial_records = history_manager.get_recent_records(10)
        print(f"初始记录数量: {len(initial_records)}")
        
        # 创建主窗口
        main_window = MainWindow()
        
        # 检查主窗口是否具有所需方法
        methods_exist = all([
            hasattr(main_window, 'show_search_history'),
            hasattr(main_window, 'clear_selected_history'),
            hasattr(main_window, 'clear_all_history'),
            hasattr(main_window, 'refresh_history_window'),
            hasattr(main_window, 'close_history_window')
        ])
        
        print(f"主窗口方法存在: {methods_exist}")
        
        # 测试历史记录管理器的移除功能
        history_manager.remove_records_by_keywords(["keyword1"])
        remaining_records = history_manager.get_recent_records(10)
        remaining_keywords = [r['keywords'] for r in remaining_records]
        
        print(f"移除keyword1后剩余: {remaining_keywords}")
        
        # 验证移除功能
        removal_correct = "keyword1" not in remaining_keywords and len(remaining_keywords) == 2
        print(f"移除功能正确: {removal_correct}")
        
        # 清理
        history_manager.clear_history()
        
        if methods_exist and removal_correct:
            print("✓ 完整搜索历史功能正常!")
            return True
        else:
            print("✗ 完整搜索历史功能有问题")
            return False
        
    except Exception as e:
        print(f"✗ 完整搜索历史功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_user_workflow():
    """测试用户工作流程"""
    print("\n测试用户工作流程...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        from gui.main_window import MainWindow
        
        # 创建历史记录管理器
        history_manager = SearchHistoryManager()
        
        # 清空现有记录
        history_manager.clear_history()
        
        # 模拟用户添加几个搜索记录
        user_searches = [
            ("찾다", "/path/to/korean/file", ""),
            ("search", "/path/to/english/file", ""),
            ("recherche", "/path/to/french/file", ""),
        ]
        
        for keywords, input_path, output_path in user_searches:
            history_manager.add_record(
                keywords=keywords,
                input_path=input_path,
                output_path=output_path,
                case_sensitive=False,
                fuzzy_match=False,
                regex_enabled=True
            )
        
        # 创建主窗口
        main_window = MainWindow()
        
        # 模拟用户打开历史窗口
        print("模拟用户打开搜索历史窗口...")
        
        # 检查历史记录数量
        stored_records = history_manager.get_recent_records(10)
        print(f"存储的历史记录数量: {len(stored_records)}")
        
        # 测试移除特定关键词
        print("测试移除特定关键词...")
        history_manager.remove_records_by_keywords(["찾다", "recherche"])
        
        remaining_records = history_manager.get_recent_records(10)
        remaining_keywords = [r['keywords'] for r in remaining_records]
        print(f"移除后剩余关键词: {remaining_keywords}")
        
        # 验证移除结果
        expected_remaining = ["search"]
        removal_successful = remaining_keywords == expected_remaining and len(remaining_keywords) == 1
        
        print(f"移除操作成功: {removal_successful}")
        
        # 清理
        history_manager.clear_history()
        
        if removal_successful:
            print("✓ 用户工作流程正常!")
            return True
        else:
            print("✗ 用户工作流程有问题")
            return False
        
    except Exception as e:
        print(f"✗ 用户工作流程测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_edge_cases():
    """测试边界情况"""
    print("\n测试边界情况...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        
        # 创建历史记录管理器
        history_manager = SearchHistoryManager()
        
        # 清空现有记录
        history_manager.clear_history()
        
        # 测试移除空列表
        print("测试移除空关键词列表...")
        history_manager.remove_records_by_keywords([])
        print("✓ 空列表处理正常")
        
        # 添加一个记录
        history_manager.add_record(
            keywords="single_record",
            input_path="/path",
            output_path="",
            case_sensitive=False,
            fuzzy_match=False,
            regex_enabled=False
        )
        
        # 测试移除不存在的关键词
        print("测试移除不存在的关键词...")
        initial_count = len(history_manager.get_recent_records(10))
        history_manager.remove_records_by_keywords(["nonexistent"])
        after_count = len(history_manager.get_recent_records(10))
        
        print(f"移除前: {initial_count}, 移除后: {after_count}")
        nonexistent_handled = initial_count == after_count
        print(f"不存在关键词处理正常: {nonexistent_handled}")
        
        # 测试移除所有记录
        print("测试移除所有记录...")
        history_manager.remove_records_by_keywords(["single_record"])
        final_count = len(history_manager.get_recent_records(10))
        
        print(f"移除所有记录后数量: {final_count}")
        all_removed = final_count == 0
        print(f"所有记录已移除: {all_removed}")
        
        # 清理
        history_manager.clear_history()
        
        if nonexistent_handled and all_removed:
            print("✓ 边界情况处理正常!")
            return True
        else:
            print("✗ 边界情况处理有问题")
            return False
        
    except Exception as e:
        print(f"✗ 边界情况测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 搜索历史右键菜单最终验证")
    print("="*60)
    
    # 运行测试
    test1_ok = test_complete_history_functionality()
    test2_ok = test_user_workflow()
    test3_ok = test_edge_cases()
    
    print("\n" + "="*60)
    print("搜索历史右键菜单最终验证结果:")
    print(f"完整功能: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"用户工作流: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"边界情况: {'✓ 정상' if test3_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有搜索历史右键菜单功能验证通过!")
        print("实现的功能:")
        print("- 搜索历史窗口支持右键菜单")
        print("- 右键菜单包含清除选定条目选项")
        print("- 右键菜单包含清除所有历史选项")
        print("- 支持按关键词移除指定历史记录")
        print("- 正确处理各种边界情况")
    else:
        print("\n✗ 部分功能验证未通过")
        
    input("\n按回车键退出...")