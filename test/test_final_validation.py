"""
最终验证所有功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_complete_setup():
    """测试完整设置"""
    print("测试完整设置...")
    
    try:
        from function.result_processor import result_processor
        from function.search_engine import search_engine
        from function.document_parser import MdParser
        
        # 创建一个测试文件
        test_file = "complete_test.md"
        content = """# Death's Game S01E01
[00:02:35] 이전 장면
[00:02:36] 현주 병원 갔잖아
[00:02:37] 다음 장면"""
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 测试搜索
        print("1. 测试搜索功能...")
        search_results = search_engine.search_in_file(test_file, "갔잖아")
        print(f"   搜索结果数量: {len(search_results)}")
        
        # 测试结果格式化
        print("2. 测试结果格式化...")
        formatted_results = result_processor.format_results_for_display(search_results, 'subtitle')
        print(f"   格式化结果数量: {len(formatted_results)}")
        
        if formatted_results:
            result = formatted_results[0]
            print(f"   格式化结果: {result}")
            
            # 验证列顺序 (filename, line_number, episode, time_axis, content)
            expected_order = [
                'complete_test.md',      # 文件名
                '2',                     # 行号
                'Death\'s Game S01E01',  # 集数
                '[00:02:36]',            # 时间轴
                '현주 병원 갔잖아'          # 内容
            ]
            
            matches = [result[i] == expected_order[i] for i in range(len(expected_order))]
            order_correct = all(matches)
            
            print(f"   列顺序正确: {order_correct}")
            for i, (actual, expected) in enumerate(zip(result, expected_order)):
                print(f"     列{i+1}: '{actual}' == '{expected}' ? {actual == expected}")
        
        os.remove(test_file)
        
        if len(formatted_results) > 0 and order_correct:
            print("✓ 完整设置测试通过!")
            return True
        else:
            print("✗ 完整设置测试未通过")
            return False
        
    except Exception as e:
        print(f"✗ 完整设置测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_column_positions():
    """测试列位置"""
    print("\n测试列位置...")
    
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
            
            print(f"列1 (文件名): {result[0]}")
            print(f"列2 (行号): {result[1]}")
            print(f"列3 (集数): {result[2]}")
            print(f"列4 (时间轴): {result[3]}")
            print(f"列5 (内容): {result[4]}")
            
            # 验证时间轴在集数和内容之间
            time_axis_position = result[3] == '[00:02:36]'  # 时间轴在第4列
            episode_before_time_axis = result[2] == 'Death\'s Game S01E01'  # 集数在第3列
            content_after_time_axis = result[4] == '현주 병원 갔잖아'  # 内容在第5列
            
            print(f"时间轴位置: {time_axis_position}")
            print(f"集数在时间轴前: {episode_before_time_axis}")
            print(f"内容在时间轴后: {content_after_time_axis}")
            
            if time_axis_position and episode_before_time_axis and content_after_time_axis:
                print("✓ 列位置正确!")
                return True
            else:
                print("✗ 列位置不正确")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 列位置测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_no_duplicate_time_axis():
    """测试时间轴不重复"""
    print("\n测试时间轴不重复...")
    
    try:
        from function.result_processor import result_processor
        
        # 测试包含时间轴的内容
        mock_results = [
            {
                'file_path': 'test.txt',
                'line_number': 2,
                'content': '[00:02:36] 현주 병원 갔잖아',
                'time_axis': '[00:02:36]',
                'episode': 'Death\'s Game S01E01',
                'matched_keywords': ['갔잖아']
            }
        ]
        
        formatted_results = result_processor.format_results_for_display(mock_results, 'subtitle')
        
        if formatted_results:
            result = formatted_results[0]
            time_axis_col = result[3]  # 时间轴列
            content_col = result[4]    # 内容列
            
            print(f"时间轴列: '{time_axis_col}'")
            print(f"内容列: '{content_col}'")
            
            # 验证时间轴没有在内容列重复
            time_axis_not_in_content = time_axis_col not in content_col or time_axis_col == 'N/A'
            content_is_clean = content_col == '현주 병원 갔잖아'  # 应该只有实际内容
            
            print(f"时间轴未在内容列重复: {time_axis_not_in_content}")
            print(f"内容列干净: {content_is_clean}")
            
            if time_axis_not_in_content and content_is_clean:
                print("✓ 时间轴不重复!")
                return True
            else:
                print("✗ 时间轴重复或内容列不干净")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 时间轴不重复测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 最终验证")
    print("="*60)
    
    # 运行测试
    test1_ok = test_complete_setup()
    test2_ok = test_column_positions()
    test3_ok = test_no_duplicate_time_axis()
    
    print("\n" + "="*60)
    print("最终验证结果:")
    print(f"完整设置: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"列位置: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"时间轴不重复: {'✓ 정상' if test3_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有验证通过!")
        print("当前实现的列顺序: 文件名、行号、集数、时间轴、内容")
        print("时间轴列位于集数和内容列之间")
        print("时间轴信息不会在内容列重复显示")
    else:
        print("\n✗ 部分验证未通过")
        
    input("\n按回车键退出...")