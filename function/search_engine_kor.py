"""
韩语搜索引擎模块
实现韩语特定的搜索功能，包括变形匹配、惯用语搜索等
"""

import re
from typing import List, Dict
from function.search_engine_base import SearchEngineBase


class KoreanSearchEngine(SearchEngineBase):
    """韩语搜索引擎类"""
    
    def __init__(self):
        """初始化韩语搜索引擎"""
        super().__init__()
    
    def search_korean_variants(self, file_path: str, base_words: List[str],
                              case_sensitive: bool = False) -> List[Dict]:
        """
        搜索韩语变形匹配
        
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
            variants = self._generate_korean_variants(word)
            print(f"[DEBUG] 词 '{word}' 生成的变体: {variants}")
            all_keywords.extend(variants)
        
        # 去重
        all_keywords = list(set(all_keywords))
        
        return self.search_in_file(file_path, all_keywords, case_sensitive, 
                                 fuzzy_match=False, regex_enabled=False)
    
    def search_korean_idiom(self, file_path: str, idiom: str, 
                          case_sensitive: bool = False) -> List[Dict]:
        """
        搜索韩语惯用语
        
        惯用语规则：
        - 关键词中的各个词可以不相连
        - 助词可以省略
        - 必须同时包含所有核心词
        - 动词/形容词可以匹配其变体
        
        Args:
            file_path: 文件路径
            idiom: 惯用语字符串（如 "인심을 쓰다"）
            case_sensitive: 是否区分大小写
            
        Returns:
            搜索结果列表
        """
        # 根据文件类型选择解析器
        from pathlib import Path
        from function.subtitle_parser import parse_subtitle_file
        from function.document_parser import parse_document_file
        
        file_ext = Path(file_path).suffix.lower()
        subtitle_exts = ['.srt', '.ass', '.ssa', '.vtt']
        
        if file_ext in subtitle_exts:
            parsed_data = parse_subtitle_file(file_path)
        else:
            parsed_data = parse_document_file(file_path)
        
        # 提取核心词（去掉助词）
        core_words = self._extract_core_words(idiom)
        print(f"[DEBUG] 惯用语核心词: {core_words}")
        
        # 为每个核心词生成变体（动词/形容词）
        all_word_variants = {}
        for word in core_words:
            variants = self._generate_korean_variants(word)
            all_word_variants[word] = variants
            print(f"[DEBUG] '{word}' 的变体: {variants}")
        
        results = []
        
        for item in parsed_data:
            content = item.get('content', '')
            search_content = content if case_sensitive else content.lower()
            
            # 检查是否按顺序包含所有核心词的任意变体
            matched_positions = []
            all_matched = True
            matched_variants = []
            
            current_pos = 0
            for word in core_words:
                variants = all_word_variants[word]
                found = False
                found_pos = -1
                found_variant = ''
                
                # 从当前位置开始搜索，确保语序正确
                for variant in variants:
                    search_variant = variant if case_sensitive else variant.lower()
                    
                    # 使用单词边界匹配
                    pattern = r'\b' + re.escape(search_variant) + r'\b'
                    match = re.search(pattern, search_content[current_pos:])
                    
                    if match:
                        # 额外检查：确保匹配的是完整的韩语单词
                        matched_text = match.group()
                        start_pos = current_pos + match.start()
                        end_pos = current_pos + match.end()
                        
                        # 检查前面是否有韩语字符（不是开头）
                        if start_pos > 0:
                            prev_char = search_content[start_pos - 1]
                            if '\uac00' <= prev_char <= '\ud7af':
                                match = None
                        
                        # 检查后面是否有韩语字符（不是结尾）
                        if match and end_pos < len(search_content):
                            next_char = search_content[end_pos]
                            if '\uac00' <= next_char <= '\ud7af':
                                match = None
                        
                        if match:
                            found = True
                            found_pos = start_pos
                            found_variant = variant
                            break
                
                if found:
                    matched_positions.append(found_pos)
                    matched_variants.append(found_variant)
                    # 更新搜索位置为找到位置的末尾
                    current_pos = found_pos + len(found_variant)
                else:
                    all_matched = False
                    break
            
            if all_matched:
                # 找到匹配，添加到结果
                result = {
                    'file_path': file_path,
                    'lineno': item.get('lineno', ''),
                    'episode': item.get('episode', ''),
                    'time_axis': item.get('time_axis', ''),
                    'content': content,
                    'matched_keywords': matched_variants
                }
                results.append(result)
                print(f"[DEBUG] 惯用语匹配: {content}")
        
        return results
    
    def _extract_core_words(self, text: str) -> List[str]:
        """
        从惯用语中提取核心词（去掉助词）
        
        Args:
            text: 惯用语文本
            
        Returns:
            核心词列表
        """
        # 韩语常见助词列表
        particles = [
            '을', '를',  # 宾格助词
            '이', '가',  # 主格助词
            '은', '는',  # 主题助词
            '에', '에서',  # 处格助词
            '으로', '로',  # 方格助词
            '와', '과',  # 和
            '의',  # 属格助词
            '만',  # 只
            '도',  # 也
            '부터',  # 从
            '까지',  # 到
            '께서',  # 从（敬语）
            '께',  # 给（敬语）
            '한테',  # 给
            '에게',  # 给
            '에게서',  # 从
        ]
        
        words = text.split()
        core_words = []
        
        for word in words:
            # 检查是否以助词结尾
            is_particle = False
            for particle in particles:
                if word.endswith(particle):
                    core_word = word[:-len(particle)]
                    if core_word:  # 确保不是空字符串
                        core_words.append(core_word)
                    is_particle = True
                    break
            
            if not is_particle:
                core_words.append(word)
        
        return core_words
    
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
            word: 韩语基础词（以다结尾的动词/形容词）

        Returns:
            韩语变形词列表
        """
        variants = []

        # 韩语动词和形容词的时态和变体规则
        # 假设输入的是词干形式（去掉다的词干）
        if word.endswith('다'):  # 动词/形容词原形
            base = word[:-1]  # 去掉다
            
            # 检查是否是 하다 类型的动词/形容词（하다用言）
            if base.endswith('하'):
                # 하다类型：존경하다, 가득하다, 좋아하다, 생각하다 等
                root = base[:-1]  # 去掉 '하' 得到词根（主题）
                
                # 主题（Topic Form）- 词根本身
                variants.append(root)
                
                # 基本形（原形）
                variants.append(word)  # 존경하다
                variants.append(base)  # 존경하
                
                # 第Ⅰ语基形式（第一语基）
                # 用于 -기, -게, -고 等连接词尾
                variants.extend([
                    root + '하기',   # 존경하기
                    root + '하게',   # 존경하게
                    root + '하고',   # 존경하고
                ])
                
                # 第Ⅱ语基形式（第二语基）
                # 用于 -ㄴ, -ㄹ, -ㅁ 等连接词尾
                variants.extend([
                    root + '한',     # 존경한
                    root + '함',     # 존경함
                    root + '할',     # 존경할
                ])
                
                # 第Ⅲ语基形式（第三语基）
                # 用于 -아/어, -아서/어서 等连接词尾
                variants.extend([
                    root + '해',     # 존경해
                    root + '하여',   # 존경하여
                    root + '해요',   # 존경해요
                    root + '해서',   # 존경해서
                ])
                
                # 过去式（过去时态）
                variants.extend([
                    root + '했',     # 존경했
                    root + '했다',   # 존경했다
                    root + '했어',   # 존경했어
                    root + '했어요', # 존경했어요
                    root + '했고',   # 존경했고
                    root + '했다가', # 존경했다가
                    root + '했으면', # 존경했으면
                ])
                
                # 其他常见变体
                variants.extend([
                    root + '하는',   # 존경하는（现在时定语）
                    root + '하면',   # 존경하면（条件形）
                    root + '하니',   # 존경하니（原因形）
                    root + '하지',   # 존경하지（否定前缀）
                    root + '하지 않다',   # 존경하지 않다
                    root + '하지 않아요', # 존경하지 않아요
                ])
                
                # 使动形式
                variants.extend([
                    root + '하게',   # 존경하게（使动副词）
                    root + '하게 해',   # 존경하게 해
                    root + '하게 했다', # 존경하게 했다
                ])
            else:
                # 普通动词/形容词（非하다用言）
                # 基本形
                variants.append(word)
                
                # 基础变位
                variants.extend([
                    base + '고',      # 속고
                    base + '지',      # 속지
                    base + '아',      # 속아
                    base + '아서',    # 속아서
                    base + '아요',    # 속아요
                    base + '으니',    # 속으니
                    base + '는',      # 속는
                    base + '은',      # 속은
                    base + '을',      # 속을
                    base + '음',      # 속음
                    base + '기',      # 속기
                ])
                
                # 过去时
                variants.extend([
                    base + '았다',    # 속았다
                    base + '았어',    # 속았어
                    base + '았어요',  # 속았어요
                    base + '았고',    # 속았고
                ])
                
                # 使役派生（-이다形式）
                causative_base = base + '이'  # 속이
                variants.extend([
                    causative_base + '다',     # 속이다
                    causative_base[:-1] + '여', # 속여 (속이 + 여)
                    causative_base[:-1] + '여서', # 속여서
                    causative_base[:-1] + '여요', # 속여요
                    causative_base[:-1] + '였다', # 속였다
                    causative_base[:-1] + '였어', # 속였어
                    causative_base[:-1] + '였어요', # 속였어요
                    causative_base + '고',     # 속이고
                ])
        else:
            # 如果不是以다结尾，可能是词干或其他形式
            # 直接添加原词
            variants.append(word)
        
        return variants


# 全局韩语搜索引擎实例
search_engine_kor = KoreanSearchEngine()