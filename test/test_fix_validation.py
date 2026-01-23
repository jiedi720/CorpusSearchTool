"""
测试修复后的功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_column_order():
    """测试列顺序"""
    print("测试列顺序...")
    
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
        
        print(f"格式化结果: {formatted_results[0] if formatted_results else 'None'}")
        
        if formatted_results:
            result = formatted_results[0]
            print(f"列1 (文件名): {result[0]}")
            print(f"列2 (行号): {result[1]}")
            print(f"列3 (时间轴): {result[2]}")
            print(f"列4 (集数): {result[3]}")
            print(f"列5 (内容): {result[4]}")
            
            # 验证列顺序
            correct_order = (
                result[0] == 'test.txt' and  # 文件名
                result[1] == '2' and        # 行号
                result[2] == '[00:02:36]' and  # 时间轴
                result[3] == 'Death\'s Game S01E01' and  # 集数
                result[4] == '현주 병원 갔잖아'  # 内容，没有高亮标签
            )
            
            print(f"列顺序正确: {correct_order}")
            print(f"内容列没有高亮标签: {'<highlight>' not in result[4]}")
            
            if correct_order and '<highlight>' not in result[4]:
                print("✓ 列顺序和高亮修复正常工作!")
                return True
            else:
                print("✗ 列顺序或高亮修复有问题")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 列顺序测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_time_axis_cleanup():
    """测试时间轴清理"""
    print("\n测试时间轴清理...")
    
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
            time_axis_col = result[2]  # 时间轴列
            content_col = result[4]    # 内容列
            
            print(f"时间轴列: '{time_axis_col}'")
            print(f"内容列: '{content_col}'")
            
            # 验证时间轴没有在内容列重复
            time_axis_not_in_content = time_axis_col not in content_col or time_axis_col == 'N/A'
            content_correct = content_col == '현주 병원 갔잖아'  # 应该只有实际内容
            
            print(f"时间轴未在内容列重复: {time_axis_not_in_content}")
            print(f"内容列正确: {content_correct}")
            
            if time_axis_not_in_content and content_correct:
                print("✓ 时间轴清理正常工作!")
                return True
            else:
                print("✗ 时间轴清理有问题")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 时间轴清理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_no_highlight_tags():
    """测试没有高亮标签"""
    print("\n测试没有高亮标签...")
    
    try:
        from function.result_processor import result_processor
        
        # 测试包含关键词的内容
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
            content_col = result[4]  # 内容列
            
            print(f"内容列: '{content_col}'")
            print(f"包含高亮标签: {'<highlight>' in content_col}")
            
            if '<highlight>' not in content_col:
                print("✓ 没有高亮标签!")
                return True
            else:
                print("✗ 仍有高亮标签")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 高亮标签测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 修复验证")
    print("="*60)
    
    # 运行测试
    test1_ok = test_column_order()
    test2_ok = test_time_axis_cleanup()
    test3_ok = test_no_highlight_tags()
    
    print("\n" + "="*60)
    print("修复验证结果:")
    print(f"列顺序: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"时间轴清理: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"无高亮标签: {'✓ 정상' if test3_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有修复验证通过!")
        print("修复的问题:")
        print("- 列顺序已调整 (时间轴列在内容列之前)")
        print("- 高亮标签不再显示为文本")
        print("- 时间轴信息只在时间轴列显示")
    else:
        print("\n✗ 部分修复仍存在问题")
        
    input("\n按回车键退出...")