"""
测试新的列顺序
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_new_column_order():
    """测试新的列顺序：文件名、行号、集数、时间轴、内容"""
    print("测试新的列顺序：文件名、行号、集数、时间轴、内容...")
    
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
        
        print(f"格式化结果数量: {len(formatted_results)}")
        for i, result in enumerate(formatted_results, 1):
            print(f"  {i}. {result}")
        
        if formatted_results:
            result = formatted_results[0]
            print(f"\n列1 (文件名): {result[0]}")
            print(f"列2 (行号): {result[1]}")
            print(f"列3 (集数): {result[2]}")
            print(f"列4 (时间轴): {result[3]}")
            print(f"列5 (内容): {result[4]}")
            
            # 验证列顺序
            correct_order = (
                result[0] == 'test.txt' and  # 文件名
                result[1] == '2' and        # 行号
                result[2] == 'Death\'s Game S01E01' and  # 集数
                result[3] == '[00:02:36]' and  # 时间轴
                result[4] == '현주 병원 갔잖아'  # 内容
            )
            
            print(f"列顺序正确: {correct_order}")
            print(f"时间轴列在集数和内容之间: {result[3] == '[00:02:36]' and result[2] == 'Death\'s Game S01E01' and result[4] == '현주 병원 갔잖아'}")
            
            if correct_order:
                print("✓ 新的列顺序正常工作!")
                return True
            else:
                print("✗ 新的列顺序有问题")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 新列顺序测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_time_axis_position():
    """测试时间轴位置"""
    print("\n测试时间轴位置：应在集数和内容之间...")
    
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
            filename_col = result[0]  # 文件名
            line_col = result[1]      # 行号
            episode_col = result[2]   # 集数
            time_axis_col = result[3] # 时间轴
            content_col = result[4]   # 内容
            
            print(f"文件名: '{filename_col}'")
            print(f"行号: '{line_col}'")
            print(f"集数: '{episode_col}'")
            print(f"时间轴: '{time_axis_col}'")
            print(f"内容: '{content_col}'")
            
            # 验证时间轴位置
            time_axis_correct = time_axis_col == '[00:02:36]'
            content_clean = content_col == '현주 병원 갔잖아'  # 应该只有实际内容，没有时间轴
            position_correct = episode_col == 'Death\'s Game S01E01'  # 集数在时间轴之前
            
            print(f"时间轴位置正确: {time_axis_correct}")
            print(f"内容列干净: {content_clean}")
            print(f"集数在时间轴之前: {position_correct}")
            
            if time_axis_correct and content_clean and position_correct:
                print("✓ 时间轴位置正确!")
                return True
            else:
                print("✗ 时间轴位置不正确")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 时间轴位置测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_document_results():
    """测试文档结果的列顺序"""
    print("\n测试文档结果的列顺序...")
    
    try:
        from function.result_processor import result_processor
        
        # 模拟文档搜索结果
        mock_results = [
            {
                'file_path': 'test.txt',
                'line_number': 1,
                'content': '이것은 문서 내용입니다',
                'episode': 'Chapter 1',
                'page': 1,
                'matched_keywords': ['문서']
            }
        ]
        
        formatted_results = result_processor.format_results_for_display(mock_results, 'document')
        
        print(f"文档格式化结果数量: {len(formatted_results)}")
        for i, result in enumerate(formatted_results, 1):
            print(f"  {i}. {result}")
        
        if formatted_results:
            result = formatted_results[0]
            print(f"\n文档列1 (文件名): {result[0]}")
            print(f"文档列2 (行号): {result[1]}")
            print(f"文档列3 (集数): {result[2]}")
            print(f"文档列4 (时间轴/页码): {result[3]}")
            print(f"文档列5 (内容): {result[4]}")
            
            # 验证文档列顺序
            correct_order = (
                result[0] == 'test.txt' and  # 文件名
                result[1] == '1' and        # 行号
                result[2] == 'Chapter 1' and  # 集数
                result[3] == '1' and  # 页码
                result[4] == '이것은 문서 내용입니다'  # 内容
            )
            
            print(f"文档列顺序正确: {correct_order}")
            
            if correct_order:
                print("✓ 文档列顺序正常工作!")
                return True
            else:
                print("✗ 文档列顺序有问题")
                return False
        else:
            print("✗ 没有文档格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 文档列顺序测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 新列顺序验证")
    print("="*60)
    
    # 运行测试
    test1_ok = test_new_column_order()
    test2_ok = test_time_axis_position()
    test3_ok = test_document_results()
    
    print("\n" + "="*60)
    print("新列顺序验证结果:")
    print(f"列顺序: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"时间轴位置: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"文档列顺序: {'✓ 정상' if test3_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有新列顺序验证通过!")
        print("新的列顺序为: 文件名、行号、集数、时间轴、内容")
        print("时间轴列现在位于集数和内容列之间")
    else:
        print("\n✗ 部分验证未通过")
        
    input("\n按回车键退出...")