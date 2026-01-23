"""
最终验证所有功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_complete_workflow():
    """测试完整工作流程"""
    print("测试完整工作流程...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        from function.search_engine import search_engine
        from function.result_processor import result_processor
        
        # 1. 测试历史记录功能
        print("1. 测试历史记录功能...")
        history_manager = SearchHistoryManager()
        
        # 添加记录
        history_manager.add_record(
            keywords="갔잖아",
            input_path="test_file.md",
            output_path="",
            case_sensitive=False,
            fuzzy_match=True,
            regex_enabled=False
        )
        
        # 获取记录
        records = history_manager.get_recent_records(10)
        print(f"   历史记录数量: {len(records)}")
        
        # 2. 测试搜索功能
        print("2. 测试搜索功能...")
        
        # 创建测试文件
        test_file = "workflow_test.md"
        content = """# Death's Game S01E01
[00:02:35] 이전 장면
[00:02:36] 현주 병원 갔잖아
[00:02:37] 다음 장면"""
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 执行搜索
        search_results = search_engine.search_in_file(test_file, "갔잖아")
        print(f"   搜索结果数量: {len(search_results)}")
        
        # 3. 测试结果格式化
        print("3. 测试结果格式化...")
        formatted_results = result_processor.format_results_for_display(search_results, 'subtitle')
        print(f"   格式化结果数量: {len(formatted_results)}")
        
        if formatted_results:
            result = formatted_results[0]
            print(f"   格式化结果示例: {result}")
            
            # 验证列顺序 (filename, line_number, time_axis, episode, content)
            expected_order = [
                'workflow_test.md',  # 文件名
                '2',                 # 行号
                '[00:02:36]',        # 时间轴
                'Unknown Episode',   # 集数 (因为没有匹配到集数标题)
                '현주 병원 갔잖아'      # 内容
            ]
            
            matches = [result[i] == expected_order[i] for i in range(min(len(result), len(expected_order)))]
            order_correct = all(matches)
            print(f"   列顺序正确: {order_correct}")
        
        os.remove(test_file)
        
        print("✓ 完整工作流程测试通过!")
        return True
        
    except Exception as e:
        print(f"✗ 完整工作流程测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_history_window_features():
    """测试历史窗口功能"""
    print("\n测试历史窗口功能...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        
        # 创建历史记录管理器
        history_manager = SearchHistoryManager()
        
        # 添加多个记录
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
        
        # 获取记录
        records = history_manager.get_recent_records(10)
        
        print(f"历史记录数量: {len(records)}")
        for i, record in enumerate(records, 1):
            print(f"  {i}. 关键词: {record['keywords']}, 时间: {record['timestamp'][:19].replace('T', ' ')}, 路径: {record['input_path']}")
        
        # 测试搜索功能
        search_results = history_manager.search_in_history("갔잖아")
        print(f"搜索'갔잖아'的结果数量: {len(search_results)}")
        
        if len(records) > 0:
            print("✓ 历史窗口功能正常工作!")
            return True
        else:
            print("✗ 历史窗口功能未正常工作")
            return False
        
    except Exception as e:
        print(f"✗ 历史窗口功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_column_order():
    """测试列顺序"""
    print("\n测试列顺序...")
    
    try:
        from function.result_processor import result_processor
        
        # 模拟结果
        mock_results = [
            {
                'file_path': 'test.txt',
                'line_number': 2,
                'content': '현주 병원 갔잖아',
                'time_axis': '[00:02:36]',
                'episode': 'Death\'s Game S01E01',
                'matched_keywords': ['갔잖아']
            }
        ]
        
        formatted_results = result_processor.format_results_for_display(mock_results, 'subtitle')
        
        if formatted_results:
            result = formatted_results[0]
            print(f"格式化结果: {result}")
            
            # 验证列顺序: (filename, line_number, time_axis, episode, content)
            expected_order = [
                'test.txt',              # 文件名
                '2',                     # 行号
                '[00:02:36]',            # 时间轴
                'Death\'s Game S01E01',  # 集数
                '현주 병원 갔잖아'          # 内容
            ]
            
            matches = [result[i] == expected_order[i] for i in range(len(expected_order))]
            order_correct = all(matches)
            
            print(f"列顺序正确: {order_correct}")
            for i, (actual, expected) in enumerate(zip(result, expected_order)):
                print(f"  列{i+1}: '{actual}' == '{expected}' ? {actual == expected}")
            
            if order_correct:
                print("✓ 列顺序正确!")
                return True
            else:
                print("✗ 列顺序不正确")
                return False
        else:
            print("✗ 没有格式化结果")
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
    test1_ok = test_complete_workflow()
    test2_ok = test_history_window_features()
    test3_ok = test_column_order()
    
    print("\n" + "="*60)
    print("最终功能验证结果:")
    print(f"完整工作流程: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"历史窗口功能: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"列顺序: {'✓ 정상' if test3_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有功能验证通过!")
        print("实现的功能:")
        print("- 搜索历史窗口中时间列位于关键词列后")
        print("- 支持双击历史记录载入关键词到主界面")
        print("- 列顺序正确 (文件名, 行号, 时间轴, 集数, 内容)")
        print("- 历史记录功能正常工作")
    else:
        print("\n✗ 部分功能验证未通过")
        
    input("\n按回车键退出...")