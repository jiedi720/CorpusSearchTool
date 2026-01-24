"""
结果处理模块
负责处理搜索结果，包括排序、过滤等功能
"""

from typing import List, Dict, Any
from pathlib import Path


class ResultProcessor:
    """结果处理器"""
    
    def __init__(self):
        """初始化结果处理器"""
        pass
    
    def format_results_for_display(self, results: List[Dict], file_type: str = 'subtitle') -> List[tuple]:
        """
        格式化搜索结果以供显示

        Args:
            results: 搜索结果列表
            file_type: 文件类型 ('subtitle' 或 'document')

        Returns:
            格式化后的结果列表，每个元素为元组 (文件名, 行号, 集数, 时间轴, 内容, 完整文件路径)
        """
        formatted_results = []

        for result in results:
            file_path = result.get('file_path', 'Unknown')
            line_number = result.get('line_number', 0)
            content = result.get('content', '')

            # 获取文件名
            filename = Path(file_path).name

            if file_type == 'subtitle':
                # 字幕文件有时间轴信息
                time_axis = result.get('time_axis', 'N/A')
                # 如果时间轴是N/A但内容中有类似时间轴的格式，尝试从内容中提取
                if time_axis == 'N/A':
                    # 尝试从内容中提取时间轴信息，例如 [00:00:49] 格式
                    time_match = re.search(r'\[(\d{1,2}:\d{2}:\d{2})\]', content)
                    if time_match:
                        time_axis = f"[{time_match.group(1)}]"

                # 获取集数信息，并移除可能的"# "符号
                episode = result.get('episode', '未知集数')
                # 移除集数信息中的"# "符号
                if episode.startswith('# '):
                    episode = episode[2:]  # 移除前两个字符 "# "

                # 从内容中移除时间轴信息（如果时间轴已单独提取）
                cleaned_content = content
                if time_axis != 'N/A' and time_axis in content:
                    # 移除时间轴部分，只保留实际内容
                    cleaned_content = content.replace(time_axis, '').strip()

                # 高亮关键词（如果存在）
                matched_keywords = result.get('matched_keywords', [])
                highlighted_content = self.highlight_content_with_keywords(cleaned_content, matched_keywords)

                formatted_results.append((filename, str(line_number), episode, time_axis, highlighted_content, file_path))
            else:
                # 文档文件可能有页码信息
                page_info = result.get('page', 'N/A')
                # 获取集数信息，并移除可能的"# "符号
                episode = result.get('episode', '未知集数')
                # 移除集数信息中的"# "符号
                if episode.startswith('# '):
                    episode = episode[2:]  # 移除前两个字符 "# "
                # 对于文档文件，使用相同的格式，优先使用解析出的时间轴，否则使用页码信息
                time_axis = result.get('time_axis', 'N/A')
                if time_axis == 'N/A':
                    time_axis = str(page_info)  # 如果没有解析出时间轴，使用页码信息

                # 从内容中移除时间轴信息（如果时间轴已单独提取）
                cleaned_content = content
                if time_axis != 'N/A' and time_axis in content:
                    # 移除时间轴部分，只保留实际内容
                    cleaned_content = content.replace(time_axis, '').strip()

                # 高亮关键词（如果存在）
                matched_keywords = result.get('matched_keywords', [])
                highlighted_content = self.highlight_content_with_keywords(cleaned_content, matched_keywords)

                formatted_results.append((filename, str(line_number), episode, time_axis, highlighted_content, file_path))

        return formatted_results
    
    def sort_results(self, results: List[Dict], sort_by: str = 'file', reverse: bool = False) -> List[Dict]:
        """
        排序搜索结果

        Args:
            results: 搜索结果列表
            sort_by: 排序字段 ('file', 'line', 'content', 'episode')
            reverse: 是否逆序

        Returns:
            排序后的结果列表
        """
        if sort_by == 'file':
            return sorted(results, key=lambda x: x.get('file_path', ''), reverse=reverse)
        elif sort_by == 'line':
            return sorted(results, key=lambda x: x.get('line_number', 0), reverse=reverse)
        elif sort_by == 'content':
            return sorted(results, key=lambda x: x.get('content', ''), reverse=reverse)
        elif sort_by == 'episode':
            return sorted(results, key=lambda x: x.get('episode', '未知集数'), reverse=reverse)
        else:
            # 默认按文件名和行号排序
            return sorted(results, key=lambda x: (x.get('file_path', ''), x.get('line_number', 0)), reverse=reverse)
    
    def filter_results(self, results: List[Dict], filters: Dict[str, Any]) -> List[Dict]:
        """
        过滤搜索结果

        Args:
            results: 搜索结果列表
            filters: 过滤条件字典

        Returns:
            过滤后的结果列表
        """
        filtered_results = results[:]

        # 按文件名过滤
        if 'filename_contains' in filters:
            filename_filter = filters['filename_contains'].lower()
            filtered_results = [r for r in filtered_results
                               if filename_filter in Path(r.get('file_path', '')).name.lower()]

        # 按内容过滤
        if 'content_contains' in filters:
            content_filter = filters['content_contains'].lower()
            filtered_results = [r for r in filtered_results
                               if content_filter in r.get('content', '').lower()]

        # 按集数过滤
        if 'episode_contains' in filters:
            episode_filter = filters['episode_contains'].lower()
            filtered_results = [r for r in filtered_results
                               if episode_filter in r.get('episode', '未知集数').lower()]

        # 按行号范围过滤
        if 'line_min' in filters:
            min_line = filters['line_min']
            filtered_results = [r for r in filtered_results
                               if r.get('line_number', 0) >= min_line]

        if 'line_max' in filters:
            max_line = filters['line_max']
            filtered_results = [r for r in filtered_results
                               if r.get('line_number', 0) <= max_line]

        return filtered_results
    
    def extract_full_dialogue(self, results: List[Dict], context_lines: int = 1) -> List[Dict]:
        """
        提取匹配行的完整对话上下文

        Args:
            results: 搜索结果列表
            context_lines: 上下文行数

        Returns:
            包含上下文的结果列表
        """
        # 这个功能需要访问原始文件来获取上下文
        # 由于当前实现中我们没有保存原始文件内容的完整结构，
        # 这里提供一个概念性的实现
        enhanced_results = []

        for result in results:
            enhanced_result = result.copy()

            # 添加上下文信息（如果可用）
            # 这里只是占位符，实际实现需要访问原始文件
            enhanced_result['context_before'] = []
            enhanced_result['context_after'] = []

            enhanced_results.append(enhanced_result)

        return enhanced_results

    def highlight_matched_keywords(self, content: str, matched_keywords: List[str]) -> str:
        """
        为匹配的关键词添加标记（用于后续在GUI中高亮显示）

        Args:
            content: 原始内容
            matched_keywords: 匹配的关键词列表

        Returns:
            标记后的内容
        """
        # 这单返回原始内容，高亮将在GUI层处理
        return content

    def get_highlight_positions(self, content: str, matched_keywords: List[str]) -> List[tuple]:
        """
        获取关键词在内容中的位置信息，用于GUI高亮显示

        Args:
            content: 原始内容
            matched_keywords: 匹配的关键词列表

        Returns:
            位置信息列表 [(keyword, start_pos, end_pos), ...]
        """
        positions = []
        for keyword in matched_keywords:
            start = 0
            while True:
                pos = content.find(keyword, start)
                if pos == -1:
                    break
                positions.append((keyword, pos, pos + len(keyword)))
                start = pos + 1
        return positions

    def highlight_content_with_keywords(self, content: str, matched_keywords: List[str]) -> str:
        """
        在内容中高亮关键词
        
        对于动词/形容词（以 다 结尾），会同时高亮其过去时态形式（如 닮다 → 닮은）
        
        Args:
            content: 原始内容
            matched_keywords: 匹配的关键词列表

        Returns:
            处理后的内容，关键词将被标记以便在 GUI 中高亮显示
        """
        # 移除重复的关键词
        unique_keywords = list(set(matched_keywords))
        # 按照长度降序排列，确保长关键词优先匹配
        unique_keywords.sort(key=lambda x: len(x), reverse=True)
        
        if not unique_keywords:
            # 如果没有关键词，返回白色文本
            return f'<span style="color: #ffffff;">{content}</span>'
        
        # 为每个动词/形容词生成过去时态形式
        keyword_variants = {}
        for keyword in unique_keywords:
            variants = [keyword]
            # 检查是否是动词/形容词（以 다 结尾）
            if keyword.endswith('다'):
                base = keyword[:-2]  # 去掉 다
                # 添加过去时态形式
                for past_suffix in ['았', '었']:
                    variants.append(base + past_suffix)
                    variants.append(base + past_suffix + '다')
                    variants.append(base + past_suffix + '어')
                    variants.append(base + past_suffix + '어요')
                    variants.append(base + past_suffix + '고')
                # 添加其他常见变体
                variants.append(base + '은')  # 过去时定语
                variants.append(base + '는')  # 现在时定语
                variants.append(base + 'ㄴ')  # 过去时定语（开音节）
                variants.append(base + '을')  # 将来时定语
                variants.append(base + 'ㄹ')  # 将来时定语（开音节）
                variants.append(base + '어')  # 基本形
                variants.append(base + '아')  # 基本形
                variants.append(base + '게')  # 副词化
                variants.append(base + '해')  # 하다类型
                variants.append(base + '했')  # 하다类型过去时
            keyword_variants[keyword] = variants
        
        # 使用 HTML 标签高亮关键词及其变体
        highlighted_content = content
        for keyword, variants in keyword_variants.items():
            for variant in variants:
                if variant in highlighted_content:
                    # 使用 <b> 和 <span style="color: #ffff00;"> 标记变体（黄色）
                    highlighted_content = highlighted_content.replace(variant, f'<b><span style="color: #ffff00;">{variant}</span></b>')
        
        # 将整个文本包裹在白色 span 中
        return f'<span style="color: #ffffff;">{highlighted_content}</span>'


# 全局结果处理器实例
result_processor = ResultProcessor()