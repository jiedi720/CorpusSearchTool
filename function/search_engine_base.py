"""
搜索引擎基础模块
实现通用的关键词匹配、模糊搜索、正则表达式等功能
"""

import re
from typing import List, Dict, Union
from function.subtitle_parser import parse_subtitle_file
from function.document_parser import parse_document_file
from pathlib import Path


class SearchEngineBase:
    """搜索引擎基础类"""
    
    def __init__(self):
        """初始化搜索引擎"""
        pass
    
    def search_in_file(self, file_path: str, keywords: Union[str, List[str]], 
                      case_sensitive: bool = False, fuzzy_match: bool = False, 
                      regex_enabled: bool = False) -> List[Dict]:
        """
        在单个文件中搜索关键词
        
        Args:
            file_path: 文件路径
            keywords: 关键词，可以是字符串或字符串列表
            case_sensitive: 是否区分大小写
            fuzzy_match: 是否启用模糊匹配
            regex_enabled: 是否启用正则表达式
            
        Returns:
            搜索结果列表
        """
        # 确保keywords是列表
        if isinstance(keywords, str):
            keywords = [keywords]
        
        # 根据文件类型选择解析器
        file_ext = Path(file_path).suffix.lower()
        subtitle_exts = ['.srt', '.ass', '.ssa', '.vtt']
        
        if file_ext in subtitle_exts:
            # 字幕文件
            parsed_data = parse_subtitle_file(file_path)
            return self._search_in_parsed_data(parsed_data, keywords, case_sensitive, 
                                             fuzzy_match, regex_enabled, is_subtitle=True)
        else:
            # 文档文件
            parsed_data = parse_document_file(file_path)
            return self._search_in_parsed_data(parsed_data, keywords, case_sensitive, 
                                             fuzzy_match, regex_enabled, is_subtitle=False)
    
    def _search_in_parsed_data(self, parsed_data: List[Dict], keywords: List[str], 
                              case_sensitive: bool, fuzzy_match: bool, 
                              regex_enabled: bool, is_subtitle: bool) -> List[Dict]:
        """
        在解析后的数据中搜索关键词
        
        Args:
            parsed_data: 解析后的数据
            keywords: 关键词列表
            case_sensitive: 是否区分大小写
            fuzzy_match: 是否启用模糊匹配
            regex_enabled: 是否启用正则表达式
            is_subtitle: 是否为字幕文件
            
        Returns:
            搜索结果列表
        """
        results = []
        
        for item in parsed_data:
            content = item.get('content', '')
            
            # 根据是否区分大小写来处理内容和关键词
            search_content = content if case_sensitive else content.lower()
            search_keywords = keywords if case_sensitive else [kw.lower() for kw in keywords]
            
            matched = False
            matched_keywords = []
            
            for keyword in search_keywords:
                if regex_enabled:
                    # 正则表达式匹配
                    flags = 0 if case_sensitive else re.IGNORECASE
                    if re.search(keyword, content, flags):
                        matched = True
                        matched_keywords.append(keyword)
                elif fuzzy_match:
                    # 模糊匹配 - 简单实现：检查关键词是否在内容中（允许一定编辑距离）
                    if self._fuzzy_match(keyword, search_content):
                        matched = True
                        matched_keywords.append(keyword)
                else:
                    # 精确匹配
                    if keyword in search_content:
                        matched = True
                        matched_keywords.append(keyword)
                        print(f"[DEBUG] 找到匹配: 关键词='{keyword}' 在内容中")
            
            if matched:
                result_item = item.copy()
                result_item['matched_keywords'] = matched_keywords
                results.append(result_item)
        
        return results
    
    def _fuzzy_match(self, pattern: str, text: str, threshold: float = 0.6) -> bool:
        """
        简单的模糊匹配实现
        
        Args:
            pattern: 搜索模式
            text: 要搜索的文本
            threshold: 匹配阈值
            
        Returns:
            是否匹配
        """
        # 简单的子串匹配，未来可以扩展为更复杂的模糊算法
        return pattern in text
    
    def search_in_files(self, file_paths: List[str], keywords: Union[str, List[str]], 
                       case_sensitive: bool = False, fuzzy_match: bool = False, 
                       regex_enabled: bool = False) -> List[Dict]:
        """
        在多个文件中搜索关键词
        
        Args:
            file_paths: 文件路径列表
            keywords: 关键词，可以是字符串或字符串列表
            case_sensitive: 是否区分大小写
            fuzzy_match: 是否启用模糊匹配
            regex_enabled: 是否启用正则表达式
            
        Returns:
            搜索结果列表
        """
        all_results = []
        for file_path in file_paths:
            results = self.search_in_file(file_path, keywords, case_sensitive, 
                                         fuzzy_match, regex_enabled)
            all_results.extend(results)
        return all_results
    
    def search_exact_match(self, file_path: str, exact_text: str, 
                         case_sensitive: bool = False) -> List[Dict]:
        """
        完全匹配搜索（引号内的内容）
        
        Args:
            file_path: 文件路径
            exact_text: 要完全匹配的文本
            case_sensitive: 是否区分大小写
            
        Returns:
            搜索结果列表
        """
        # 根据文件类型选择解析器
        file_ext = Path(file_path).suffix.lower()
        subtitle_exts = ['.srt', '.ass', '.ssa', '.vtt']
        
        if file_ext in subtitle_exts:
            parsed_data = parse_subtitle_file(file_path)
        else:
            parsed_data = parse_document_file(file_path)
        
        results = []
        
        for item in parsed_data:
            content = item.get('content', '')
            
            # 完全匹配检查
            search_content = content if case_sensitive else content.lower()
            search_exact = exact_text if case_sensitive else exact_text.lower()
            
            if search_exact in search_content:
                result = {
                    'file_path': file_path,
                    'lineno': item.get('lineno', ''),
                    'episode': item.get('episode', ''),
                    'time_axis': item.get('time_axis', ''),
                    'content': content,
                    'matched_keywords': [exact_text]
                }
                results.append(result)
                print(f"[DEBUG] 完全匹配: {content}")
        
        return results


# 全局搜索引擎实例
search_engine_base = SearchEngineBase()
search_engine = search_engine_base  # 向后兼容，保持全局实例名称不变