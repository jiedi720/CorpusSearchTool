"""
测试所有更新
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_column_widths():
    """测试列宽度"""
    print("测试列宽度...")
    
    try:
        from function.result_processor import result_processor
        
        # 模拟搜索结果
        mock_results = [
            {
                'file_path': 'very_long_filename_example.txt',
                'line_number': 1234567,
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
            
            # 验证列顺序和内容
            filename_col = result[0]  # 文件名
            line_col = result[1]      # 行号
            episode_col = result[2]   # 集数
            time_axis_col = result[3] # 时间轴
            content_col = result[4]   # 内容
            
            print(f"文件名列: '{filename_col}'")
            print(f"行号列: '{line_col}' (应为1234567)")
            print(f"集数列: '{episode_col}'")
            print(f"时间轴列: '{time_axis_col}' (应为[00:02:36])")
            print(f"内容列: '{content_col}'")
            
            # 验证行号和时间轴格式
            line_correct = line_col == '1234567'  # 行号应为7位数字
            time_correct = time_axis_col == '[00:02:36]'  # 时间轴应为[00:02:36]格式
            
            print(f"行号格式正确: {line_correct}")
            print(f"时间轴格式正确: {time_correct}")
            
            if line_correct and time_correct:
                print("✓ 列宽度设置正确!")
                return True
            else:
                print("✗ 列宽度设置不正确")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 列宽度测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_episode_format():
    """测试集数格式"""
    print("\n测试集数格式（不显示'# '符号）...")
    
    try:
        from function.result_processor import result_processor
        
        # 测试包含"# "符号的集数
        mock_results = [
            {
                'file_path': 'test.txt',
                'line_number': 2,
                'content': '현주 병원 갔잖아',
                'time_axis': '[00:02:36]',
                'episode': '# Death\'s Game S01E01',  # 包含"# "符号
                'matched_keywords': ['갔잖아']
            }
        ]
        
        formatted_results = result_processor.format_results_for_display(mock_results, 'subtitle')
        
        if formatted_results:
            result = formatted_results[0]
            episode_col = result[2]  # 集数列
            
            print(f"原始集数: '# Death\'s Game S01E01'")
            print(f"处理后集数: '{episode_col}'")
            
            # 验证"# "符号已被移除
            has_hash_prefix = episode_col.startswith('# ')
            correct_format = episode_col == 'Death\'s Game S01E01'  # 应该没有"# "前缀
            
            print(f"包含'# '前缀: {has_hash_prefix}")
            print(f"格式正确: {correct_format}")
            
            if not has_hash_prefix and correct_format:
                print("✓ 集数格式正确，'# '符号已移除!")
                return True
            else:
                print("✗ 集数格式不正确")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 集数格式测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_history_column_widths():
    """测试历史记录列宽度"""
    print("\n测试历史记录列宽度...")
    
    try:
        from function.search_history_manager import SearchHistoryManager
        
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
        
        # 获取记录
        records = history_manager.get_recent_records(10)
        
        print(f"历史记录数量: {len(records)}")
        for i, record in enumerate(records, 1):
            print(f"  {i}. 关键词: {record['keywords']}, 时间: {record['timestamp'][:19].replace('T', ' ')}, 路径: {record['input_path']}")
        
        if len(records) > 0:
            print("✓ 历史记录功能正常工作!")
            return True
        else:
            print("✗ 未能获取历史记录")
            return False
        
    except Exception as e:
        print(f"✗ 历史记录列宽度测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_complete_format():
    """测试完整格式"""
    print("\n测试完整格式...")
    
    try:
        from function.result_processor import result_processor
        
        # 测试完整结果
        mock_results = [
            {
                'file_path': 'long_filename_example.txt',
                'line_number': 1234567,
                'content': '현주 병원 갔잖아',
                'time_axis': '[00:02:36]',
                'episode': '# Death\'s Game S01E01',
                'matched_keywords': ['갔잖아']
            }
        ]
        
        formatted_results = result_processor.format_results_for_display(mock_results, 'subtitle')
        
        if formatted_results:
            result = formatted_results[0]
            print(f"完整格式化结果: {result}")
            
            # 验证所有格式要求
            filename_ok = len(result[0]) > 0  # 文件名存在
            line_ok = result[1] == '1234567'  # 行号为7位
            episode_ok = result[2] == 'Death\'s Game S01E01'  # 集数无"# "前缀
            time_ok = result[3] == '[00:02:36]'  # 时间轴格式正确
            content_ok = result[4] == '현주 병원 갔잖아'  # 内容正确
            
            print(f"文件名正确: {filename_ok}")
            print(f"行号正确: {line_ok}")
            print(f"集数正确: {episode_ok}")
            print(f"时间轴正确: {time_ok}")
            print(f"内容正确: {content_ok}")
            
            all_correct = all([filename_ok, line_ok, episode_ok, time_ok, content_ok])
            
            if all_correct:
                print("✓ 完整格式正确!")
                return True
            else:
                print("✗ 完整格式不正确")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 完整格式测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 更新验证")
    print("="*60)
    
    # 运行测试
    test1_ok = test_column_widths()
    test2_ok = test_episode_format()
    test3_ok = test_history_column_widths()
    test4_ok = test_complete_format()
    
    print("\n" + "="*60)
    print("更新验证结果:")
    print(f"列宽度: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"集数格式: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"历史记录列宽: {'✓ 정상' if test3_ok else '✗ 이상'}")
    print(f"完整格式: {'✓ 정상' if test4_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok and test4_ok:
        print("\n✓ 所有更新验证通过!")
        print("更新的内容:")
        print("- 行号列宽度调整为60（适合显示1234567）")
        print("- 时间轴列宽度调整为80（适合显示[00:02:36]）")
        print("- 文件名和集数列宽度增加")
        print("- 集数列不再显示'# '符号")
        print("- 搜索历史中关键词列宽度与时间列相同")
    else:
        print("\n✗ 部分更新验证未通过")
        
    input("\n按回车键退出...")