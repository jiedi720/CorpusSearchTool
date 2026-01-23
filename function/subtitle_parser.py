"""
字幕文件解析模块
负责解析各种字幕文件格式（SRT, ASS, VTT等）和带时间戳的文本文件
"""

import re
from typing import List, Dict, Tuple
from pathlib import Path


import re

class SubtitleParser:
    """字幕文件解析器基类"""

    def parse(self, file_path: str) -> List[Dict]:
        """
        解析字幕文件

        Args:
            file_path: 字幕文件路径

        Returns:
            解析结果列表，每个元素包含时间轴、文本、集数等内容
        """
        raise NotImplementedError("子类必须实现parse方法")


class SrtParser(SubtitleParser):
    """SRT字幕文件解析器"""

    def parse(self, file_path: str) -> List[Dict]:
        """
        解析SRT字幕文件

        Args:
            file_path: SRT文件路径

        Returns:
            解析结果列表
        """
        results = []

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 遍历所有行，寻找字幕块
        i = 0
        current_episode = "未知集数"  # 默认集数

        while i < len(lines):
            line = lines[i].strip()

            if line.isdigit():  # 这是一个字幕块的开始
                line_number = int(line)

                # 检查下一行是否是时间轴
                if i + 1 < len(lines):
                    time_line = lines[i + 1].strip()
                    if '-->' in time_line:
                        time_axis = time_line

                        # 提取内容行
                        content_lines = []
                        j = i + 2
                        while j < len(lines) and lines[j].strip() != '':
                            content_line = lines[j].strip()

                            # 检查是否是集数标题（通常格式为 "Episode X", "第X集", "#X" 等）
                            if self.is_episode_title(content_line):
                                current_episode = content_line
                            else:
                                content_lines.append(content_line)

                            j += 1

                        content = '\n'.join(content_lines)

                        results.append({
                            'line_number': line_number,
                            'time_axis': time_axis,
                            'content': content,
                            'episode': current_episode,
                            'file_path': file_path
                        })

                        # 跳过已处理的行
                        i = j
                        continue

            i += 1

        return results

    def is_episode_title(self, line: str) -> bool:
        """
        检查一行是否是集数标题

        Args:
            line: 要检查的行

        Returns:
            是否是集数标题
        """
        # 检查常见的集数标题格式
        episode_patterns = [
            r'^第\d+集',           # 第1集, 第2集, ...
            r'^Episode\s*\d+',     # Episode 1, Episode 2, ...
            r'^EP\s*\d+',         # EP 1, EP 2, ...
            r'^#\d+',             # #1, #2, ...
            r'^[Ss]\d+[Ee]\d+',   # S1E1, S2E5, ...
            r'^[Cc]hapter\s+\d+'   # Chapter 1, Chapter 2, ...
        ]

        line_lower = line.lower()
        for pattern in episode_patterns:
            if re.match(pattern, line_lower) or re.match(pattern, line):
                return True

        return False


class AssParser(SubtitleParser):
    """ASS/SSA字幕文件解析器"""
    
    def parse(self, file_path: str) -> List[Dict]:
        """
        解析ASS/SSA字幕文件
        
        Args:
            file_path: ASS/SSA文件路径
            
        Returns:
            解析结果列表
        """
        results = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 查找Dialogue行
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('Dialogue:'):
                # Dialogue格式: Dialogue: Mark,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
                parts = line.split(',', 9)  # 分割为10个部分
                if len(parts) >= 10:
                    start_time = parts[1]  # 开始时间
                    end_time = parts[2]    # 结束时间
                    text = parts[9]        # 字幕文本
                    
                    time_axis = f"{start_time} --> {end_time}"
                    
                    results.append({
                        'line_number': i + 1,
                        'time_axis': time_axis,
                        'content': text,
                        'file_path': file_path
                    })
        
        return results


class VttParser(SubtitleParser):
    """WebVTT字幕文件解析器"""
    
    def parse(self, file_path: str) -> List[Dict]:
        """
        解析VTT字幕文件
        
        Args:
            file_path: VTT文件路径
            
        Returns:
            解析结果列表
        """
        results = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除可能的WEBVTT头部
        content = re.sub(r'^WEBVTT\s*\n(?:\s*NOTE.*?\n)?\s*\n?', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 按空白行分割块
        blocks = re.split(r'\n\s*\n', content.strip())
        
        line_number = 1
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            
            lines = block.split('\n')
            if len(lines) < 2:
                continue
            
            # 检查是否为时间轴行 (HH:MM:SS.mmm --> HH:MM:SS.mmm)
            time_pattern = r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}'
            if re.match(time_pattern, lines[0].strip()):
                time_axis = lines[0].strip()
                
                # 提取文本内容
                text_lines = lines[1:]
                text_content = '\n'.join(text_lines).strip()
                
                results.append({
                    'line_number': line_number,
                    'time_axis': time_axis,
                    'content': text_content,
                    'file_path': file_path
                })
                
                line_number += 1
        
        return results


class TimestampParser(SubtitleParser):
    """时间戳文本文件解析器 - 处理 [00:00:49] 格式"""
    
    def parse(self, file_path: str) -> List[Dict]:
        """
        解析带时间戳的文本文件，格式如 [00:00:49] 内容
        
        Args:
            file_path: 文本文件路径
            
        Returns:
            解析结果列表
        """
        results = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        line_number = 1
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 匹配 [HH:MM:SS] 或 [H:MM:SS] 格式的时间戳
            timestamp_pattern = r'\[(\d{1,2}:\d{2}:\d{2})\]\s*(.*)'
            match = re.match(timestamp_pattern, line)
            
            if match:
                time_axis = f"[{match.group(1)}]"  # 保留原始格式
                content = match.group(2).strip()
                
                results.append({
                    'line_number': line_number,
                    'time_axis': time_axis,
                    'content': content,
                    'file_path': file_path
                })
            
            line_number += 1
        
        return results


def get_parser(file_path: str) -> SubtitleParser:
    """
    根据文件扩展名获取相应的解析器
    
    Args:
        file_path: 文件路径
        
    Returns:
        对应的解析器实例
    """
    ext = Path(file_path).suffix.lower()
    
    if ext == '.srt':
        return SrtParser()
    elif ext in ['.ass', '.ssa']:
        return AssParser()
    elif ext == '.vtt':
        return VttParser()
    elif ext in ['.txt', '.md']:  # 对于文本文件，检查是否包含时间戳
        # 先尝试时间戳解析
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            sample = f.read(1024)  # 读取前1024字符
            if re.search(r'\[\d{1,2}:\d{2}:\d{2}\]', sample):
                return TimestampParser()
        # 如果没有时间戳，则使用普通文本解析
        from function.document_parser import get_document_parser
        return get_document_parser(file_path)
    else:
        raise ValueError(f"不支持的字幕文件格式: {ext}")


def parse_subtitle_file(file_path: str) -> List[Dict]:
    """
    解析字幕文件的统一接口
    
    Args:
        file_path: 字幕文件路径
        
    Returns:
        解析结果列表
    """
    parser = get_parser(file_path)
    return parser.parse(file_path)