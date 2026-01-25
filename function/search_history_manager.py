"""
搜索历史记录模块
管理用户的搜索历史记录
"""

import os
from datetime import datetime
from typing import List, Dict


class SearchHistoryManager:
    """搜索历史记录管理器"""
    
    def __init__(self, corpus_type: str = "eng"):
        """
        初始化搜索历史记录管理器
        
        Args:
            corpus_type: 语料库类型 ('eng' 或 'kor')
        """
        self.corpus_type = corpus_type
        self.history_file = self._get_history_file()
        self.history = self.load_history()
    
    def _get_history_file(self) -> str:
        """根据语料库类型获取历史文件名"""
        if self.corpus_type == "eng":
            return "search_history_eng.md"
        elif self.corpus_type == "kor":
            return "search_history_kor.md"
        else:
            return "search_history.md"
    
    def set_corpus_type(self, corpus_type: str):
        """
        设置语料库类型并重新加载历史记录
        
        Args:
            corpus_type: 语料库类型 ('eng' 或 'kor')
        """
        if self.corpus_type != corpus_type:
            self.corpus_type = corpus_type
            self.history_file = self._get_history_file()
            self.history = self.load_history()
    
    def load_history(self) -> List[Dict]:
        """加载历史记录"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content:
                    return []
                
                # 解析Markdown格式的历史记录
                history = []
                # 跳过标题部分，从第一条记录开始
                records = content.split('\n---\n')
                
                for record in records[1:]:  # 跳过标题部分
                    if not record.strip():
                        continue
                    
                    record_dict = {}
                    lines = record.strip().split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('**关键词**:'):
                            record_dict['keywords'] = line.split('**关键词**:', 1)[1].strip()
                        elif line.startswith('**时间**:'):
                            time_str = line.split('**时间**:', 1)[1].strip()
                            # 将时间字符串转换为ISO格式
                            try:
                                dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                                record_dict['timestamp'] = dt.isoformat()
                            except ValueError:
                                record_dict['timestamp'] = datetime.now().isoformat()
                        elif line.startswith('**输入路径**:'):
                            record_dict['input_path'] = line.split('**输入路径**:', 1)[1].strip()
                        elif line.startswith('**输出路径**:'):
                            record_dict['output_path'] = line.split('**输出路径**:', 1)[1].strip()
                        elif line.startswith('**结果数量**:'):
                            record_dict['result_count'] = int(line.split('**结果数量**:', 1)[1].strip())
                        elif line.startswith('**关键词类型**:'):
                            record_dict['keyword_type'] = line.split('**关键词类型**:', 1)[1].strip()
                        elif line.startswith('**设置**:'):
                            # 解析设置部分
                            settings = {
                                'case_sensitive': False,  # 默认值
                                'fuzzy_match': False,      # 默认值
                                'regex_enabled': False     # 默认值
                            }
                            # 设置部分在后续行，缩进显示
                            settings_lines = [l.strip() for l in lines[lines.index(line)+1:] if l.strip().startswith('-')]
                            for setting_line in settings_lines:
                                if setting_line.startswith('- **正则表达式**:'):
                                    settings['regex_enabled'] = setting_line.split('- **正则表达式**:', 1)[1].strip() == 'True'
                            record_dict['settings'] = settings
                    
                    # 确保所有必填字段存在
                    if 'keywords' in record_dict and 'timestamp' in record_dict:
                        history.append(record_dict)
                
                return history
            except Exception as e:
                print(f"加载历史记录失败: {e}")
                return []
        return []
    
    def save_history(self):
        """保存历史记录为Markdown格式"""
        # 限制历史记录数量，最多保存100条
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        with open(self.history_file, 'w', encoding='utf-8') as mdfile:
            mdfile.write("# 搜索历史记录\n\n")
            mdfile.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if not self.history:
                mdfile.write("暂无搜索历史记录。\n")
                return
            
            # 按时间倒序排列
            sorted_history = sorted(self.history, key=lambda x: x['timestamp'], reverse=True)
            
            for record in sorted_history:
                # 转换时间格式
                timestamp = datetime.fromisoformat(record['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                
                # 写入记录
                mdfile.write("---\n\n")
                mdfile.write(f"**关键词**: {record['keywords']}\n")
                mdfile.write(f"**关键词类型**: {record.get('keyword_type', '')}\n")
                
                # 添加词典形和变体信息
                lemma = record.get('lemma', '')
                if lemma:
                    mdfile.write(f"**词典形**: {lemma}\n")
                
                # 显示生成的所有变体列表
                target_variant_set = record.get('target_variant_set', [])
                if target_variant_set:
                    mdfile.write(f"**生成变体列表**: {', '.join(target_variant_set)}\n")
                
                # 显示实际命中的变体
                actual_variant_set = record.get('actual_variant_set', [])
                if actual_variant_set:
                    mdfile.write(f"**实际命中变体**: {', '.join(actual_variant_set)}\n")
                
                # 只有当正则表达式为True时，才显示正则表达式信息
                settings = record.get('settings', {})
                regex_enabled = settings.get('regex_enabled', False)
                if regex_enabled:
                    mdfile.write(f"**正则表达式**: {regex_enabled}\n")
                
                mdfile.write(f"**时间**: {timestamp}\n")
                mdfile.write(f"**输入路径**: {record['input_path']}\n")
                
                # 只有当输出路径存在且不为空时，才显示输出路径
                output_path = record.get('output_path', '')
                if output_path and output_path != 'N/A':
                    mdfile.write(f"**输出路径**: {output_path}\n")
                
                mdfile.write(f"**结果数量**: {record.get('result_count', 0)}\n")
    
    def add_record(self, keywords: str, input_path: str, output_path: str = "", 
                   case_sensitive: bool = False, fuzzy_match: bool = False, 
                   regex_enabled: bool = False, result_count: int = 0, keyword_type: str = "",
                   lemma: str = "", actual_variant_set: list = [], target_variant_set: list = []):
        """
        添加搜索记录
        
        Args:
            keywords: 搜索关键词
            input_path: 输入路径
            output_path: 输出路径
            case_sensitive: 是否区分大小写
            fuzzy_match: 是否模糊匹配
            regex_enabled: 是否启用正则表达式
            result_count: 搜索结果数量
            keyword_type: 关键词类型（如 "名词 & 副词"、"动词 & 形容词" 等）
            lemma: 系统判定的词典形
            actual_variant_set: 基于词典形实际命中的所有变体形式列表
            target_variant_set: 基于词典形生成的所有可能变体形式列表
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "keywords": keywords,
            "input_path": input_path,
            "output_path": output_path,
            "result_count": result_count,
            "keyword_type": keyword_type,
            "lemma": lemma,
            "target_variant_set": target_variant_set,
            "actual_variant_set": actual_variant_set,
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
        removed_count = 0
        
        # 预处理要删除的时间戳，只保留前19个字符（YYYY-MM-DDTHH:MM:SS）
        processed_timestamps = set()
        for ts in timestamps_list:
            # 处理不同格式的时间戳，只保留到秒
            if '.' in ts:
                # 包含微秒的格式：YYYY-MM-DDTHH:MM:SS.ffffff
                processed_timestamps.add(ts.split('.')[0])
            elif ts.endswith(':00'):
                # 手动添加的 :00 格式：YYYY-MM-DDTHH:MM:SS:00
                processed_timestamps.add(ts[:-3])
            else:
                # 其他格式，尝试只保留前19个字符
                processed_timestamps.add(ts[:19])
        
        for record in self.history:
            # 获取记录时间戳的前19个字符（YYYY-MM-DDTHH:MM:SS）
            record_ts = record['timestamp'][:19]
            if record_ts not in processed_timestamps:
                new_history.append(record)
            else:
                removed_count += 1

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