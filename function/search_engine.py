"""
搜索引擎模块
实现关键词匹配、模糊搜索、正则表达式等功能
"""

import re
from typing import List, Dict, Union
from function.subtitle_parser import parse_subtitle_file
from function.document_parser import parse_document_file
from pathlib import Path


class SearchEngine:
    """搜索引擎类"""
    
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
                    # 精确匹配 - 确保关键词确实存在于内容中
                    if keyword in search_content:
                        matched = True
                        matched_keywords.append(keyword)
            
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
            try:
                file_results = self.search_in_file(file_path, keywords, 
                                                 case_sensitive, fuzzy_match, regex_enabled)
                all_results.extend(file_results)
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {str(e)}")
                continue
        
        return all_results
    
    def search_korean_english_variants(self, file_path: str, base_words: List[str],
                                      case_sensitive: bool = False) -> List[Dict]:
        """
        搜索韩语/英语变形匹配
        
        Args:
            file_path: 文件路径
            base_words: 基础词列表（原型词）
            case_sensitive: 是否区分大小写
            
        Returns:
            搜索结果列表
        """
        # 这里需要实现韩语/英语变形匹配算法
        # 由于复杂性，这里提供一个框架实现
        all_keywords = []
        
        for word in base_words:
            # 生成可能的变形词
            variants = self._generate_word_variants(word)
            all_keywords.extend(variants)
        
        # 去重
        all_keywords = list(set(all_keywords))
        
        return self.search_in_file(file_path, all_keywords, case_sensitive, 
                                 fuzzy_match=False, regex_enabled=False)
    
    def _generate_word_variants(self, word: str) -> List[str]:
        """
        生成单词的可能变形（支持韩语/英语变形）

        Args:
            word: 基础词

        Returns:
            变形词列表
        """
        variants = [word]  # 至少包含原词

        # 检测是否为韩语
        if self._is_korean(word):
            # 韩语变形规则
            korean_variants = self._generate_korean_variants(word)
            variants.extend(korean_variants)
        else:
            # 英语变形示例（简化）
            english_variants = self._generate_english_variants(word)
            variants.extend(english_variants)

        return variants

    def _is_korean(self, text: str) -> bool:
        """
        检测文本是否包含韩语字符

        Args:
            text: 要检测的文本

        Returns:
            是否包含韩语字符
        """
        # 韩文字母范围: U+AC00–U+D7AF
        korean_pattern = re.compile(r'[\uac00-\ud7af]')
        return bool(korean_pattern.search(text))

    def _generate_korean_variants(self, word: str) -> List[str]:
        """
        生成韩语单词的可能变形

        Args:
            word: 韩语基础词

        Returns:
            韩语变形词列表
        """
        variants = []

        # 简单的韩语变形规则（可以根据需要扩展）
        # 例如: 아직 -> 아직도, 않다 -> 안, etc.
        if word.endswith('다'):  # 动词原形
            base = word[:-1]  # 去掉다
            variants.extend([
                base,  # 기본형
                base + '요',  # 요
                base + '서',  # 서
                base + '고',  # 고
                base + '는',  # 는
                base + 'ㄴ',  # ㄴ
                base + 'ㄹ',  # ㄹ
            ])

        # 特定词汇的变形
        if word == '아직도':
            variants.extend(['아직', '아직은', '아직까지'])
        elif word == '않다':
            variants.extend(['안', '않', '않는', '않을'])

        return variants

    def _generate_english_variants(self, word: str) -> List[str]:
        """
        生成英语单词的可能变形

        Args:
            word: 英语基础词

        Returns:
            英语变形词列表
        """
        variants = []

        # 英语变形示例（简化）
        if word.endswith('e'):
            variants.append(word[:-1] + 'ing')  # like -> liking
            variants.append(word[:-1] + 'ed')   # like -> liked
        elif word.endswith('y'):
            variants.append(word[:-1] + 'ies')  # beauty -> beauties
            variants.append(word[:-1] + 'ied')  # cry -> cried
        else:
            variants.append(word + 's')         # cat -> cats
            variants.append(word + 'ing')       # run -> running
            variants.append(word + 'ed')        # walk -> walked

        return variants


# 全局搜索引擎实例
search_engine = SearchEngine()