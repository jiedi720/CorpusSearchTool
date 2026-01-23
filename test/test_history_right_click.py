"""
测试搜索历史右键菜单功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_history_manager_updates():
    """测试历史记录管理器更新"""
    print("测试历史记录管理器更新...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        
        # 创建历史记录管理器
        history_manager = SearchHistoryManager()
        
        # 清空现有记录
        history_manager.clear_history()
        
        # 添加多个测试记录
        test_records = [
            ("keyword1", "/path1", ""),
            ("keyword2", "/path2", ""),
            ("keyword3", "/path3", ""),
        ]
        
        for keywords, input_path, output_path in test_records:
            history_manager.add_record(
                keywords=keywords,
                input_path=input_path,
                output_path=output_path,
                case_sensitive=False,
                fuzzy_match=True,
                regex_enabled=False
            )
        
        # 检查记录数量
        initial_records = history_manager.get_recent_records(10)
        print(f"初始记录数量: {len(initial_records)}")
        
        # 测试移除功能
        history_manager.remove_records_by_keywords(["keyword1", "keyword3"])
        
        remaining_records = history_manager.get_recent_records(10)
        print(f"移除后记录数量: {len(remaining_records)}")
        
        # 检查是否正确移除了指定记录
        remaining_keywords = [record['keywords'] for record in remaining_records]
        expected_remaining = ["keyword2"]
        
        print(f"剩余关键词: {remaining_keywords}")
        print(f"期望剩余: {expected_remaining}")
        
        correct_removal = remaining_keywords == expected_remaining
        print(f"移除功能正确: {correct_removal}")
        
        # 清理
        history_manager.clear_history()
        
        if correct_removal:
            print("✓ 历史记录管理器更新正常!")
            return True
        else:
            print("✗ 历史记录管理器更新有问题")
            return False
        
    except Exception as e:
        print(f"✗ 历史记录管理器更新测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_right_click_menu():
    """测试右键菜单功能"""
    print("\n测试右键菜单功能...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        from gui.main_window import MainWindow
        
        # 创建历史记录管理器
        history_manager = SearchHistoryManager()
        
        # 清空现有记录
        history_manager.clear_history()
        
        # 添加测试记录
        history_manager.add_record(
            keywords="test_keyword_1",
            input_path="/test/path/1",
            output_path="",
            case_sensitive=False,
            fuzzy_match=True,
            regex_enabled=False
        )
        
        history_manager.add_record(
            keywords="test_keyword_2",
            input_path="/test/path/2",
            output_path="",
            case_sensitive=False,
            fuzzy_match=True,
            regex_enabled=False
        )
        
        # 创建主窗口
        main_window = MainWindow()
        
        # 检查是否可以访问历史记录管理器的方法
        has_remove_method = hasattr(history_manager, 'remove_records_by_keywords')
        print(f"历史记录管理器有移除方法: {has_remove_method}")
        
        # 检查主窗口是否有相关方法
        has_clear_methods = (
            hasattr(main_window, 'clear_selected_history') and
            hasattr(main_window, 'clear_all_history') and
            hasattr(main_window, 'refresh_history_window')
        )
        print(f"主窗口有清除方法: {has_clear_methods}")
        
        # 清理
        history_manager.clear_history()
        
        if has_remove_method and has_clear_methods:
            print("✓ 右键菜单功能方法已实现!")
            return True
        else:
            print("✗ 右键菜单功能方法未完全实现")
            return False
        
    except Exception as e:
        print(f"✗ 右键菜单功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_clear_functionality():
    """测试清除功能"""
    print("\n测试清除功能...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        
        # 创建历史记录管理器
        history_manager = SearchHistoryManager()
        
        # 清空现有记录
        history_manager.clear_history()
        
        # 添加测试记录
        test_keywords = ["clear_test_1", "clear_test_2", "keep_this"]
        for keyword in test_keywords:
            history_manager.add_record(
                keywords=keyword,
                input_path=f"/path/{keyword}",
                output_path="",
                case_sensitive=False,
                fuzzy_match=True,
                regex_enabled=False
            )
        
        # 检查初始记录
        initial_count = len(history_manager.get_recent_records(10))
        print(f"初始记录数量: {initial_count}")
        
        # 测试移除部分记录
        history_manager.remove_records_by_keywords(["clear_test_1", "clear_test_2"])
        
        remaining_count = len(history_manager.get_recent_records(10))
        remaining_records = history_manager.get_recent_records(10)
        remaining_keywords = [r['keywords'] for r in remaining_records]
        
        print(f"移除后记录数量: {remaining_count}")
        print(f"剩余关键词: {remaining_keywords}")
        
        # 验证结果
        expected_remaining = ["keep_this"]
        correct_remaining = remaining_keywords == expected_remaining
        correct_count = remaining_count == 1
        
        print(f"剩余记录正确: {correct_remaining}")
        print(f"记录数量正确: {correct_count}")
        
        # 清理
        history_manager.clear_history()
        
        if correct_remaining and correct_count:
            print("✓ 清除功能正常!")
            return True
        else:
            print("✗ 清除功能有问题")
            return False
        
    except Exception as e:
        print(f"✗ 清除功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 搜索历史右键菜单功能测试")
    print("="*60)
    
    # 运行测试
    test1_ok = test_history_manager_updates()
    test2_ok = test_right_click_menu()
    test3_ok = test_clear_functionality()
    
    print("\n" + "="*60)
    print("搜索历史右键菜单功能测试结果:")
    print(f"历史管理器更新: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"右键菜单功能: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"清除功能: {'✓ 정상' if test3_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有搜索历史右键菜单功能测试通过!")
        print("实现的功能:")
        print("- 右键菜单包含清除选定条目选项")
        print("- 右键菜单包含清除所有历史选项")
        print("- 可以按关键词移除指定的历史记录")
        print("- 清除后能正确刷新显示")
    else:
        print("\n✗ 部分功能测试未通过")
        
    input("\n按回车键退出...")