"""
搜索历史记录模块
管理用户的搜索历史记录
"""

import json
import os
from datetime import datetime
from typing import List, Dict


class SearchHistoryManager:
    """搜索历史记录管理器"""
    
    def __init__(self, history_file: str = "search_history.json"):
        """
        初始化搜索历史记录管理器
        
        Args:
            history_file: 历史记录文件名
        """
        self.history_file = history_file
        self.history = self.load_history()
    
    def load_history(self) -> List[Dict]:
        """加载历史记录"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_history(self):
        """保存历史记录"""
        # 限制历史记录数量，最多保存100条
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_record(self, keywords: str, input_path: str, output_path: str = "", 
                   case_sensitive: bool = False, fuzzy_match: bool = False, 
                   regex_enabled: bool = False):
        """
        添加搜索记录
        
        Args:
            keywords: 搜索关键词
            input_path: 输入路径
            output_path: 输出路径
            case_sensitive: 是否区分大小写
            fuzzy_match: 是否模糊匹配
            regex_enabled: 是否启用正则表达式
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "keywords": keywords,
            "input_path": input_path,
            "output_path": output_path,
            "settings": {
                "case_sensitive": case_sensitive,
                "fuzzy_match": fuzzy_match,
                "regex_enabled": regex_enabled
            }
        }
        
        self.history.append(record)
        self.save_history()
    
    def get_recent_records(self, count: int = 10) -> List[Dict]:
        """
        获取最近的搜索记录

        Args:
            count: 获取记录的数量

        Returns:
            最近的搜索记录列表
        """
        return self.history[-count:] if len(self.history) >= count else self.history[:]

    def export_to_markdown(self, output_path: str, filename: str = "search_history.md"):
        """
        将搜索历史导出为Markdown格式

        Args:
            output_path: 输出目录路径
            filename: 输出文件名
        """
        import os
        from datetime import datetime

        output_file = os.path.join(output_path, filename)

        with open(output_file, 'w', encoding='utf-8') as mdfile:
            mdfile.write("# 搜索历史记录\n\n")
            mdfile.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            if not self.history:
                mdfile.write("暂无搜索历史记录。\n")
                return

            # 按时间倒序排列
            sorted_history = sorted(self.history, key=lambda x: x['timestamp'], reverse=True)

            for i, record in enumerate(sorted_history, 1):
                timestamp = datetime.fromisoformat(record['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

                mdfile.write(f"## 记录 {i}\n")
                mdfile.write(f"- **时间**: {timestamp}\n")
                mdfile.write(f"- **关键词**: {record['keywords']}\n")
                mdfile.write(f"- **输入路径**: {record['input_path']}\n")
                mdfile.write(f"- **输出路径**: {record.get('output_path', 'N/A')}\n")
                mdfile.write(f"- **大小写敏感**: {record['settings']['case_sensitive']}\n")
                mdfile.write(f"- **模糊匹配**: {record['settings']['fuzzy_match']}\n")
                mdfile.write(f"- **正则表达式**: {record['settings']['regex_enabled']}\n")
                mdfile.write("\n")
    
    def remove_records_by_keywords(self, keywords_list):
        """
        根据关键词列表移除历史记录

        Args:
            keywords_list: 要移除的关键词列表
        """
        if not keywords_list:
            return

        # 创建新的历史记录列表，排除指定关键词的记录
        new_history = []
        for record in self.history:
            if record['keywords'] not in keywords_list:
                new_history.append(record)

        # 更新历史记录
        self.history = new_history
        self.save_history()
        
    def remove_records_by_timestamp(self, timestamps_list):
        """
        根据时间戳列表移除特定的历史记录

        Args:
            timestamps_list: 要移除的记录时间戳列表
        """
        if not timestamps_list:
            return

        # 创建新的历史记录列表，排除指定时间戳的记录
        new_history = []
        for record in self.history:
            if record['timestamp'] not in timestamps_list:
                new_history.append(record)

        # 更新历史记录
        self.history = new_history
        self.save_history()

    def clear_history(self):
        """清空历史记录"""
        self.history = []
        self.save_history()
    
    def search_in_history(self, keyword: str) -> List[Dict]:
        """
        在历史记录中搜索包含特定关键词的记录
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的记录列表
        """
        keyword_lower = keyword.lower()
        matches = []
        
        for record in self.history:
            if (keyword_lower in record.get('keywords', '').lower() or
                keyword_lower in record.get('input_path', '').lower()):
                matches.append(record)
        
        return matches


# 全局搜索历史记录管理器实例
search_history_manager = SearchHistoryManager()