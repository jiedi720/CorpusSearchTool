"""
最终修复验证
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_original_problem_fixed():
    """测试原始问题是否修复"""
    print("测试原始问题是否修复: 현주 병원 <highlight>갔잖아</highlight> ...")
    
    try:
        from function.result_processor import result_processor
        from function.document_parser import MdParser
        from function.search_engine import search_engine
        
        # 创建一个包含时间轴和关键词的测试文件
        test_file = "test_original_problem.md"
        content = """# Death's Game S01E01
[00:02:35] 이전 장면
[00:02:36] 현주 병원 갔잖아
[00:02:37] 다음 장면"""
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 搜索关键词
        search_results = search_engine.search_in_file(test_file, "갔잖아")
        
        print(f"搜索'갔잖아'的结果数量: {len(search_results)}")
        for i, result in enumerate(search_results, 1):
            print(f"  {i}. 行号: {result['line_number']}, 时间轴: {result.get('time_axis', 'N/A')}, 集数: {result.get('episode', 'N/A')}, 内容: {result['content']}")
        
        # 格式化结果
        formatted_results = result_processor.format_results_for_display(search_results, 'subtitle')
        
        print(f"\n格式化结果数量: {len(formatted_results)}")
        for i, result in enumerate(formatted_results, 1):
            print(f"  {i}. 格式化结果: {result}")
        
        # 检查格式化结果
        if formatted_results:
            first_result = formatted_results[0]
            content_field = first_result[4]  # 内容在第5个位置 (索引4)
            
            print(f"\n内容字段: '{content_field}'")
            print(f"包含<highlight>标签: {'<highlight>' in content_field}")
            
            # 验证问题是否修复
            has_highlight_tags = '<highlight>' in content_field
            correct_content = content_field == '현주 병원 갔잖아'  # 应该只有实际内容
            
            print(f"内容正确: {correct_content}")
            print(f"无高亮标签: {not has_highlight_tags}")
            
            os.remove(test_file)
            
            if not has_highlight_tags and correct_content:
                print("✓ 原始问题已修复!")
                return True
            else:
                print("✗ 原始问题未完全修复")
                return False
        else:
            print("✗ 没有格式化结果")
            os.remove(test_file)
            return False
        
    except Exception as e:
        print(f"✗ 原始问题修复测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_column_order():
    """测试列顺序"""
    print("\n测试列顺序: 时间轴列应在内容列之前 ...")
    
    try:
        from function.result_processor import result_processor
        
        # 模拟搜索结果
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
                'test.txt',  # 文件名
                '2',         # 行号
                '[00:02:36]', # 时间轴
                'Death\'s Game S01E01',  # 集数
                '현주 병원 갔잖아'  # 内容
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


def test_time_axis_separation():
    """测试时间轴分离"""
    print("\n测试时间轴分离: 时间轴不应在内容列重复 ...")
    
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
            time_axis_field = result[2]  # 时间轴在第3个位置 (索引2)
            content_field = result[4]    # 内容在第5个位置 (索引4)
            
            print(f"时间轴字段: '{time_axis_field}'")
            print(f"内容字段: '{content_field}'")
            
            # 验证时间轴没有在内容字段重复
            time_axis_not_in_content = time_axis_field not in content_field or time_axis_field == 'N/A'
            content_is_clean = content_field == '현주 병원 갔잖아'  # 应该只有实际内容
            
            print(f"时间轴未在内容字段重复: {time_axis_not_in_content}")
            print(f"内容字段干净: {content_is_clean}")
            
            if time_axis_not_in_content and content_is_clean:
                print("✓ 时间轴分离正常工作!")
                return True
            else:
                print("✗ 时间轴分离有问题")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 时间轴分离测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 最终修复验证")
    print("="*60)
    
    # 运行测试
    test1_ok = test_original_problem_fixed()
    test2_ok = test_column_order()
    test3_ok = test_time_axis_separation()
    
    print("\n" + "="*60)
    print("最终修复验证结果:")
    print(f"原始问题修复: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"列顺序: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"时间轴分离: {'✓ 정상' if test3_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有修复验证通过!")
        print("修复的问题:")
        print("- 内容列不再显示<highlight>标签")
        print("- 列顺序已调整 (文件名, 行号, 时间轴, 集数, 内容)")
        print("- 时间轴信息只在时间轴列显示，不在内容列重复")
    else:
        print("\n✗ 部分修复仍存在问题")
        
    input("\n按回车键退出...")