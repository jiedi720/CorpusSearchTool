#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试结果格式化功能，确保行号和关键词高亮正常工作
"""

from function.result_processor import result_processor


def test_result_formatting():
    """测试结果格式化功能"""
    print("=== 测试结果格式化功能 ===")
    
    # 测试数据1：使用lineno字段
    test_result1 = {
        'file_path': 'test/test_kor.txt',
        'lineno': 4,
        'episode': '未知集数',
        'time_axis': 'N/A',
        'content': '나는 그에게 속아요.  # 속다 (欺骗) 的变形',
        'matched_keyword': '속'
    }
    
    # 测试数据2：使用line_number字段
    test_result2 = {
        'file_path': 'test/test_kor.txt',
        'line_number': 5,
        'episode': '未知集数',
        'time_axis': 'N/A',
        'content': '그는 나를 속였어.  # 속다 (欺骗) 的变形',
        'matched_keyword': '속다'
    }
    
    test_results = [test_result1, test_result2]
    
    # 调用格式化函数
    formatted_results = result_processor.format_results_for_display(test_results, 'document')
    
    print(f"格式化结果数量: {len(formatted_results)}")
    
    for i, result in enumerate(formatted_results):
        filename, line_number, episode, time_axis, content, file_path = result
        print(f"\n结果 {i+1}:")
        print(f"  文件名: {filename}")
        print(f"  行号: {line_number}")
        print(f"  集数: {episode}")
        print(f"  时间轴: {time_axis}")
        print(f"  内容: {content}")
        print(f"  文件路径: {file_path}")
        
        # 检查行号是否正确
        if i == 0:
            assert line_number == '4', f"期望行号4，实际得到{line_number}"
        elif i == 1:
            assert line_number == '5', f"期望行号5，实际得到{line_number}"
        
        # 检查内容中是否有高亮标记
        assert '<b><span style="color: #ffff00;">' in content, "内容中没有高亮标记"
    
    print("\n=== 所有测试通过！===\n")


if __name__ == "__main__":
    test_result_formatting()
