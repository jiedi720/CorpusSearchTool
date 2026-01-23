"""
结果展示与导出模块
负责结果的展示和导出功能
"""

import csv
import json
from typing import List, Dict, Tuple
from pathlib import Path


class ResultExporter:
    """结果导出器"""
    
    def __init__(self):
        """初始化结果导出器"""
        pass
    
    def export_to_csv(self, results: List[Tuple], output_path: str, filename: str = "search_results.csv"):
        """
        导出结果到CSV文件

        Args:
            results: 搜索结果列表，每个元素为元组 (文件名, 时间轴/页码, 行号, 集数, 内容) 或 (文件名, 时间轴/页码, 行号, 内容)
            output_path: 输出目录路径
            filename: 输出文件名
        """
        output_file = Path(output_path) / filename

        with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)

            # 根据结果格式确定表头
            if results and len(results[0]) == 5:  # (文件名, 时间轴, 行号, 集数, 内容)
                writer.writerow(['文件名', '时间轴', '行号', '集数', '内容'])
            else:  # (文件名, 时间轴/页码, 行号, 内容)
                writer.writerow(['文件名', '时间轴/页码', '行号', '内容'])

            # 写入数据
            for row in results:
                writer.writerow(row)

    def export_to_txt(self, results: List[Tuple], output_path: str, filename: str = "search_results.txt"):
        """
        导出结果到TXT文件

        Args:
            results: 搜索结果列表，每个元素为元组 (文件名, 时间轴/页码, 行号, 集数, 内容) 或 (文件名, 时间轴/页码, 行号, 内容)
            output_path: 输出目录路径
            filename: 输出文件名
        """
        output_file = Path(output_path) / filename

        with open(output_file, 'w', encoding='utf-8') as txtfile:
            txtfile.write("搜索结果\n")
            txtfile.write("=" * 50 + "\n\n")

            for idx, row in enumerate(results, 1):
                txtfile.write(f"结果 {idx}:\n")

                if len(row) == 5:  # (文件名, 时间轴, 行号, 集数, 内容)
                    filename, time_or_page, line_num, episode, content = row
                    txtfile.write(f"  文件: {filename}\n")
                    txtfile.write(f"  时间轴: {time_or_page}\n")
                    txtfile.write(f"  行号: {line_num}\n")
                    txtfile.write(f"  集数: {episode}\n")
                    txtfile.write(f"  内容: {content}\n")
                else:  # (文件名, 时间轴/页码, 行号, 内容)
                    filename, time_or_page, line_num, content = row
                    txtfile.write(f"  文件: {filename}\n")
                    txtfile.write(f"  时间轴/页码: {time_or_page}\n")
                    txtfile.write(f"  行号: {line_num}\n")
                    txtfile.write(f"  内容: {content}\n")

                txtfile.write("-" * 30 + "\n\n")
    
    def export_to_json(self, results: List[Tuple], output_path: str, filename: str = "search_results.json"):
        """
        导出结果到JSON文件
        
        Args:
            results: 搜索结果列表，每个元素为元组 (文件名, 时间轴/页码, 行号, 内容)
            output_path: 输出目录路径
            filename: 输出文件名
        """
        # 将元组转换为字典格式
        json_results = []
        for filename, time_or_page, line_num, content in results:
            json_results.append({
                "filename": filename,
                "time_or_page": time_or_page,
                "line_number": line_num,
                "content": content
            })
        
        output_file = Path(output_path) / filename
        
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(json_results, jsonfile, ensure_ascii=False, indent=2)


# 全局结果导出器实例
result_exporter = ResultExporter()