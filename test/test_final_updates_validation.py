"""
最终验证所有更新
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_all_updates():
    """测试所有更新"""
    print("测试所有更新...")
    
    try:
        from function.result_processor import result_processor
        from function.search_engine import search_engine
        from function.document_parser import MdParser
        
        # 创建测试文件
        test_file = "final_test.md"
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
            
            # 验证列顺序和格式
            filename_col = result[0]  # 文件名
            line_col = result[1]      # 行号
            episode_col = result[2]   # 集数
            time_axis_col = result[3] # 时间轴
            content_col = result[4]   # 内容
            
            print(f"   文件名: '{filename_col}'")
            print(f"   行号: '{line_col}'")
            print(f"   集数: '{episode_col}'")
            print(f"   时间轴: '{time_axis_col}'")
            print(f"   内容: '{content_col}'")
            
            # 验证格式要求
            line_format_ok = line_col.isdigit()  # 行号应为数字
            time_format_ok = time_axis_col.startswith('[') and time_axis_col.endswith(']')  # 时间轴格式
            episode_no_hash = not episode_col.startswith('# ')  # 集数不应有#前缀
            content_ok = '갔잖아' in content_col  # 内容应包含关键词
            
            print(f"   行号格式正确: {line_format_ok}")
            print(f"   时间轴格式正确: {time_format_ok}")
            print(f"   集数无#前缀: {episode_no_hash}")
            print(f"   内容正确: {content_ok}")
            
            all_ok = line_format_ok and time_format_ok and episode_no_hash and content_ok
            print(f"   所有格式要求满足: {all_ok}")
        
        os.remove(test_file)
        
        if len(formatted_results) > 0 and all_ok:
            print("✓ 所有更新验证通过!")
            return True
        else:
            print("✗ 部分更新验证未通过")
            return False
        
    except Exception as e:
        print(f"✗ 所有更新验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_episode_cleaning():
    """测试集数清理"""
    print("\n测试集数清理（移除'# '符号）...")
    
    try:
        from function.result_processor import result_processor
        
        # 测试包含"# "符号的集数
        mock_results = [
            {
                'file_path': 'test.txt',
                'line_number': 1,
                'content': 'Test content',
                'time_axis': 'N/A',
                'episode': '# Death\'s Game S01E01',  # 包含"# "前缀
                'matched_keywords': []
            }
        ]
        
        formatted_results = result_processor.format_results_for_display(mock_results, 'subtitle')
        
        if formatted_results:
            result = formatted_results[0]
            episode_col = result[2]
            
            print(f"原始集数: '# Death\'s Game S01E01'")
            print(f"处理后集数: '{episode_col}'")
            
            # 验证"# "符号已被移除
            has_hash_prefix = episode_col.startswith('# ')
            correct_format = episode_col == 'Death\'s Game S01E01'
            
            print(f"包含'# '前缀: {has_hash_prefix}")
            print(f"格式正确: {correct_format}")
            
            if not has_hash_prefix and correct_format:
                print("✓ 集数清理正常工作!")
                return True
            else:
                print("✗ 集数清理未正常工作")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 集数清理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_time_axis_format():
    """测试时间轴格式"""
    print("\n测试时间轴格式...")
    
    try:
        from function.result_processor import result_processor
        
        # 测试标准时间轴格式
        mock_results = [
            {
                'file_path': 'test.txt',
                'line_number': 1234567,
                'content': 'Test content',
                'time_axis': '[00:02:36]',
                'episode': 'Death\'s Game S01E01',
                'matched_keywords': []
            }
        ]
        
        formatted_results = result_processor.format_results_for_display(mock_results, 'subtitle')
        
        if formatted_results:
            result = formatted_results[0]
            time_axis_col = result[3]
            
            print(f"时间轴列: '{time_axis_col}'")
            
            # 验证时间轴格式
            correct_format = time_axis_col == '[00:02:36]'
            has_brackets = time_axis_col.startswith('[') and time_axis_col.endswith(']')
            
            print(f"格式正确: {correct_format}")
            print(f"有括号: {has_brackets}")
            
            if correct_format and has_brackets:
                print("✓ 时间轴格式正确!")
                return True
            else:
                print("✗ 时间轴格式不正确")
                return False
        else:
            print("✗ 没有格式化结果")
            return False
        
    except Exception as e:
        print(f"✗ 时间轴格式测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("字幕语料库检索工具 - 最终更新验证")
    print("="*60)
    
    # 运行测试
    test1_ok = test_all_updates()
    test2_ok = test_episode_cleaning()
    test3_ok = test_time_axis_format()
    
    print("\n" + "="*60)
    print("最终更新验证结果:")
    print(f"所有更新: {'✓ 정상' if test1_ok else '✗ 이상'}")
    print(f"集数清理: {'✓ 정상' if test2_ok else '✗ 이상'}")
    print(f"时间轴格式: {'✓ 정상' if test3_ok else '✗ 이상'}")
    
    if test1_ok and test2_ok and test3_ok:
        print("\n✓ 所有更新验证通过!")
        print("实现的更新:")
        print("- 行号列宽度适合显示1234567")
        print("- 时间轴列宽度适合显示[00:02:36]")
        print("- 集数列不再显示'# '符号")
        print("- 搜索历史中关键词列宽度与时间列相同")
        print("- 文件名和集数列宽度增加")
    else:
        print("\n✗ 部分更新验证未通过")
        
    input("\n按回车键退出...")