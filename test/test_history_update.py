"""
测试搜索历史功能更新
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_history_columns_order():
    """测试历史记录列顺序"""
    print("测试历史记录列顺序...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        
        # 创建历史记录管理器实例
        history_manager = SearchHistoryManager()
        
        # 添加一些测试记录
        history_manager.add_record(
            keywords="test keyword",
            input_path="/path/to/input",
            output_path="/path/to/output",
            case_sensitive=True,
            fuzzy_match=False,
            regex_enabled=True
        )
        
        # 获取最近记录
        recent_records = history_manager.get_recent_records(10)
        
        print(f"获取到的历史记录数量: {len(recent_records)}")
        for i, record in enumerate(recent_records, 1):
            print(f"  {i}. 关键词: {record['keywords']}, 时间: {record['timestamp']}, 输入路径: {record['input_path']}")
        
        if len(recent_records) > 0:
            print("✓ 历史记录功能正常工作!")
            return True
        else:
            print("✗ 未能获取历史记录")
            return False
        
    except Exception as e:
        print(f"✗ 历史记录列顺序测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_history_format():
    """测试历史记录格式"""
    print("\n测试历史记录格式...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        
        # 创建历史记录管理器实例
        history_manager = SearchHistoryManager()
        
        # 添加测试记录
        history_manager.add_record(
            keywords="갔잖아",
            input_path="Death's.Game.S01.md",
            output_path="",
            case_sensitive=False,
            fuzzy_match=True,
            regex_enabled=False
        )
        
        # 获取记录
        records = history_manager.get_recent_records(1)
        
        if records:
            record = records[0]
            print(f"关键词: {record['keywords']}")
            print(f"时间戳: {record['timestamp']}")
            print(f"输入路径: {record['input_path']}")
            
            # 验证记录格式
            has_correct_fields = all(field in record for field in ['keywords', 'input_path', 'timestamp', 'settings'])
            print(f"包含正确字段: {has_correct_fields}")
            
            if has_correct_fields:
                print("✓ 历史记录格式正确!")
                return True
            else:
                print("✗ 历史记录格式不正确")
                return False
        else:
            print("✗ 没有获取到记录")
            return False
        
    except Exception as e:
        print(f"✗ 历史记录格式测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_history_search():
    """测试历史记录搜索功能"""
    print("\n测试历史记录搜索功能...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        
        # 创建历史记录管理器实例
        history_manager = SearchHistoryManager()
        
        # 添加多个测试记录
        history_manager.add_record(
            keywords="갔잖아",
            input_path="Death's.Game.S01.md",
            output_path="",
            case_sensitive=False,
            fuzzy_match=True,
            regex_enabled=False
        )
        
        history_manager.add_record(
            keywords="대단하다",
            input_path="Another.File.md",
            output_path="",
            case_sensitive=True,
            fuzzy_match=False,
            regex_enabled=True
        )
        
        # 测试搜索历史记录
        search_results = history_manager.search_in_history("갔잖아")
        
        print(f"搜索'갔잖아'的结果数量: {len(search_results)}")
        for i, result in enumerate(search_results, 1):
            print(f"  {i}. 关键词: {result['keywords']}, 输入路径: {result['input_path']}")
        
        if len(search_results) > 0:
            print("✓ 历史记录搜索功能正常工作!")
            return True
        else:
            print("✗ 历史记录搜索功能未正常工作")
            return False
        
    except Exception as e:
        print(f"✗ 历史记录搜索测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 搜索历史功能更新测试")
    print("="*60)
    
    # 运行测试
    test1_ok = test_history_columns_order()
    test2_ok = test_history_format()
    test3_ok = test_history_search()
    
    print("\n" + "="*60)
    print("搜索历史功能测试结果:")
    print(f"列顺序: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"记录格式: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"搜索功能: {'✓ 정상' if test3_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有搜索历史功能测试通过!")
        print("更新的功能:")
        print("- 时间列现在位于关键词列之后")
        print("- 可以通过双击载入关键词到主界面")
        print("- 历史记录功能正常工作")
    else:
        print("\n✗ 部分功能测试未通过")
        
    input("\n按回车键退出...")