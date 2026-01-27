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
        """根据语料库类型获取历史文件名，生成到searchhistory文件夹"""
        import os
        # 获取主程序目录
        base_dir = os.path.dirname(os.path.dirname(__file__))
        # 生成searchhistory文件夹路径
        history_dir = os.path.join(base_dir, "searchhistory")
        # 如果目录不存在则创建
        if not os.path.exists(history_dir):
            os.makedirs(history_dir, exist_ok=True)
        
        # 返回完整的历史文件路径，使用txt格式
        if self.corpus_type == "eng":
            return os.path.join(history_dir, "search_history_eng.txt")
        elif self.corpus_type == "kor":
            return os.path.join(history_dir, "search_history_kor.txt")
        else:
            return os.path.join(history_dir, "search_history.txt")
    
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
    
    def scan_html_files(self):
        """
        扫描searchhistory目录中的所有HTML文件，将其添加到搜索历史中
        
        Returns:
            添加的记录数量
        """
        import os
        from bs4 import BeautifulSoup
        import re
        
        # 获取searchhistory目录路径
        base_dir = os.path.dirname(os.path.dirname(__file__))
        history_dir = os.path.join(base_dir, "searchhistory")
        
        # 如果目录不存在则创建
        if not os.path.exists(history_dir):
            os.makedirs(history_dir, exist_ok=True)
            return 0
        
        added_count = 0
        
        # 遍历目录中的所有HTML文件
        for file_name in os.listdir(history_dir):
            if file_name.endswith('.html'):
                file_path = os.path.join(history_dir, file_name)
                
                try:
                    # 读取HTML文件内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    # 解析HTML内容
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # 提取搜索信息
                    search_info = {}
                    
                    # 查找搜索关键词
                    keyword_p = soup.find('p', string=re.compile(r'搜索关键词:'))
                    if not keyword_p:
                        continue
                    search_info['keywords'] = keyword_p.text.split('搜索关键词:')[-1].strip()
                    
                    # 查找搜索路径，判断是否为韩语语料库
                    path_p = soup.find('p', string=re.compile(r'搜索路径:'))
                    if not path_p:
                        continue
                    search_path = path_p.text.split('搜索路径:')[-1].strip()
                    
                    # 从搜索路径、文件名和关键词判断是否为韩语语料库
                    is_korean = False
                    # 检查搜索路径
                    if '韩语' in search_path or 'Korean' in search_path:
                        is_korean = True
                    # 检查文件名
                    if 'Korean' in file_name:
                        is_korean = True
                    # 检查关键词是否包含韩字
                    import re
                    korean_pattern = re.compile(r'[\uac00-\ud7af]')
                    if korean_pattern.search(search_info['keywords']):
                        is_korean = True
                    
                    search_info['corpus_type'] = 'korean' if is_korean else 'english'
                    search_info['search_path'] = search_path
                    
                    # 查找关键词类型
                    keyword_type_p = None
                    for p in soup.find_all('p'):
                        if '关键词类型:' in p.text:
                            keyword_type_p = p
                            break
                    if keyword_type_p:
                        search_info['keyword_type'] = keyword_type_p.text.split('关键词类型:')[-1].strip()
                    
                    # 查找结果数量
                    result_count = 0
                    result_p = soup.find('p', string=re.compile(r'结果数量:'))
                    if result_p:
                        try:
                            result_count = int(result_p.text.split('结果数量:')[-1].strip())
                        except ValueError:
                            # 从表格中计算结果数量
                            table = soup.find('table')
                            if table:
                                rows = table.find_all('tr')
                                result_count = len(rows) - 1  # 减去表头行
                    
                    # 查找lemma和lemmalist信息
                    lemma_text = ''
                    lemmalist_text = ''
                    lemma_p = soup.find('p', id='lemma_text')
                    lemmalist_p = soup.find('p', id='lemmalist_text')
                    if lemma_p:
                        lemma_text = lemma_p.get_text(strip=True)
                    if lemmalist_p:
                        lemmalist_text = lemmalist_p.get_text(strip=True)
                    
                    # 将lemmalist_text拆分为target_variant_set和actual_variant_set
                    target_variant_set = []
                    actual_variant_set = []
                    if lemmalist_text:
                        # 提取生成变体列表
                        target_match = re.search(r'生成变体列表:\s*(.*?)(?:;|$)', lemmalist_text)
                        if target_match:
                            target_variant_set = [v.strip() for v in target_match.group(1).split(',') if v.strip()]
                        # 提取实际命中变体
                        actual_match = re.search(r'实际命中变体:\s*(.*?)(?:;|$)', lemmalist_text)
                        if actual_match:
                            actual_variant_set = [v.strip() for v in actual_match.group(1).split(',') if v.strip()]
                    
                    # 检查该记录是否已存在于搜索历史中
                    record_exists = False
                    for record in self.history:
                        if record.get('keywords') == search_info['keywords'] and record.get('result_count') == result_count:
                            record_exists = True
                            break
                    
                    if not record_exists:
                        # 提取HTML文件的相对路径
                        rel_html_path = os.path.relpath(file_path, base_dir)
                        
                        # 根据语料库类型切换search_history_manager的语料库类型
                        old_corpus_type = self.corpus_type
                        if search_info['corpus_type'] == 'korean':
                            self.set_corpus_type('kor')
                        else:
                            self.set_corpus_type('eng')
                        
                        # 添加记录到搜索历史
                        self.add_record(
                            keywords=search_info['keywords'],
                            input_path=search_info['search_path'],
                            html_path=rel_html_path,
                            case_sensitive=False,
                            fuzzy_match=False,
                            regex_enabled=False,
                            result_count=result_count,
                            keyword_type=search_info.get('keyword_type', ''),
                            lemma=lemma_text,
                            actual_variant_set=actual_variant_set,
                            target_variant_set=target_variant_set
                        )
                        added_count += 1
                        print(f"已添加HTML文件到搜索历史: {file_name} (语料库类型: {self.corpus_type})")
                        
                        # 恢复原来的语料库类型
                        self.set_corpus_type(old_corpus_type)
                        
                except Exception as e:
                    print(f"处理HTML文件 {file_name} 时出错: {str(e)}")
                    continue
        
        return added_count
    
    def load_history(self) -> List[Dict]:
        """加载历史记录"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content:
                    return []
                
                # 解析历史记录
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
                        elif line.startswith('**HTML路径**:'):
                            record_dict['html_path'] = line.split('**HTML路径**:', 1)[1].strip()
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
        """保存历史记录，使用兼容Markdown的文本格式"""
        # 限制历史记录数量，最多保存100条
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            f.write("# 搜索历史记录\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if not self.history:
                f.write("暂无搜索历史记录。\n")
                return
            
            # 按时间倒序排列
            sorted_history = sorted(self.history, key=lambda x: x['timestamp'], reverse=True)
            
            for record in sorted_history:
                # 转换时间格式
                timestamp = datetime.fromisoformat(record['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                
                # 写入记录
                f.write("---\n\n")
                f.write(f"**关键词**: {record['keywords']}\n")
                f.write(f"**关键词类型**: {record.get('keyword_type', '')}\n")
                
                # 添加词典形和变体信息
                lemma = record.get('lemma', '')
                if lemma:
                    f.write(f"**词典形**: {lemma}\n")
                
                # 显示生成的所有变体列表
                target_variant_set = record.get('target_variant_set', [])
                if target_variant_set:
                    f.write(f"**生成变体列表**: {', '.join(target_variant_set)}\n")
                
                # 显示实际命中的变体
                actual_variant_set = record.get('actual_variant_set', [])
                if actual_variant_set:
                    f.write(f"**实际命中变体**: {', '.join(actual_variant_set)}\n")
                
                # 只有当正则表达式为True时，才显示正则表达式信息
                settings = record.get('settings', {})
                regex_enabled = settings.get('regex_enabled', False)
                if regex_enabled:
                    f.write(f"**正则表达式**: {regex_enabled}\n")
                
                f.write(f"**时间**: {timestamp}\n")
                f.write(f"**输入路径**: {record['input_path']}\n")
                
                # 只有当输出路径存在且不为空时，才显示输出路径
                output_path = record.get('output_path', '')
                if output_path and output_path != 'N/A':
                    f.write(f"**输出路径**: {output_path}\n")
                
                # 只有当HTML路径存在且不为空时，才显示HTML路径
                html_path = record.get('html_path', '')
                if html_path:
                    f.write(f"**HTML路径**: {html_path}\n")
                
                f.write(f"**结果数量**: {record.get('result_count', 0)}\n")
    
    def add_record(self, keywords: str, input_path: str, output_path: str = "", 
                   case_sensitive: bool = False, fuzzy_match: bool = False, 
                   regex_enabled: bool = False, result_count: int = 0, keyword_type: str = "",
                   lemma: str = "", actual_variant_set: list = [], target_variant_set: list = [],
                   html_path: str = ""):
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
            html_path: HTML文件路径
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "keywords": keywords,
            "input_path": input_path,
            "output_path": output_path,
            "html_path": html_path,
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