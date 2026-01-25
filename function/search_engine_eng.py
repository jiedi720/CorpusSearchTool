"""
英语搜索引擎模块
实现英语特定的搜索功能，包括变形匹配等
"""

from typing import List, Dict
from function.search_engine_base import SearchEngineBase


class EnglishSearchEngine(SearchEngineBase):
    """英语搜索引擎类"""
    
    def __init__(self):
        """初始化英语搜索引擎"""
        super().__init__()
    
    def search_english_variants(self, file_path: str, base_words: List[str],
                               case_sensitive: bool = False) -> List[Dict]:
        """
        搜索英语变形匹配
        
        Args:
            file_path: 文件路径
            base_words: 基础词列表（原型词）
            case_sensitive: 是否区分大小写
            
        Returns:
            搜索结果列表
        """
        # 生成可能的变形词
        all_keywords = []
        
        for word in base_words:
            # 生成可能的变形词
            variants = self._generate_english_variants(word)
            all_keywords.extend(variants)
        
        # 去重
        all_keywords = list(set(all_keywords))
        
        return self.search_in_file(file_path, all_keywords, case_sensitive, 
                                 fuzzy_match=False, regex_enabled=False)

    def _generate_english_variants(self, word: str) -> List[str]:
        """
        生成英语单词的可能变形（简化版本）

        Args:
            word: 英语基础词

        Returns:
            英语变形词列表
        """
        variants = [word]  # 至少包含原词
        
        # 简化的英语变形规则
        # 复数形式
        if not word.endswith('s'):
            variants.append(word + 's')
        
        # 过去式（以e结尾的加d，否则加ed）
        if word.endswith('e'):
            variants.append(word + 'd')
        else:
            variants.append(word + 'ed')
        
        # 进行时
        if word.endswith('e'):
            variants.append(word[:-1] + 'ing')
        else:
            variants.append(word + 'ing')
        
        return variants


# 全局英语搜索引擎实例
search_engine_eng = EnglishSearchEngine()