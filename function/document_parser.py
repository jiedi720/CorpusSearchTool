"""
文档文件解析模块 - 扩展版
负责解析各种文档格式（Word, PDF, TXT, MD等）
"""

import re
from typing import List, Dict, Tuple
from pathlib import Path


class DocumentParser:
    """文档文件解析器基类"""
    
    def parse(self, file_path: str) -> List[Dict]:
        """
        解析文档文件
        
        Args:
            file_path: 文档文件路径
            
        Returns:
            解析结果列表，每个元素包含行号、文本等内容
        """
        raise NotImplementedError("子类必须实现parse方法")


class TxtParser(DocumentParser):
    """TXT文档解析器"""

    def parse(self, file_path: str) -> List[Dict]:
        """
        解析TXT文档

        Args:
            file_path: TXT文件路径

        Returns:
            解析结果列表
        """
        results = []

        # 尝试不同的编码格式
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        content = None

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            raise ValueError(f"无法使用常见编码读取文件: {file_path}")

        # 按行分割
        lines = content.split('\n')

        current_episode = "未知集数"  # 默认集数

        for i, line in enumerate(lines, 1):
            if line.strip():  # 只处理非空行
                stripped_line = line.strip()

                # 检查是否是集数标题
                if self.is_episode_title(stripped_line):
                    current_episode = stripped_line
                else:
                    # 检查是否包含时间轴格式，如 [00:02:36]
                    time_axis = self.extract_time_axis(stripped_line)

                    results.append({
                        'line_number': i,
                        'content': stripped_line,
                        'episode': current_episode,
                        'time_axis': time_axis if time_axis else 'N/A',
                        'file_path': file_path
                    })

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
        import re
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

        # 检查Markdown标题格式，如 # Death's Game S01E01
        markdown_header_pattern = r'^#{1,6}\s+.*?[Ss]\d+[Ee]\d+.*?$'  # 匹配包含SxEx的标题
        if re.match(markdown_header_pattern, line):
            return True

        return False

    def extract_time_axis(self, line: str) -> str:
        """
        从行中提取时间轴信息

        Args:
            line: 要检查的行

        Returns:
            时间轴信息，如果没有找到则返回None
        """
        import re
        # 匹配 [00:02:36] 格式的时间轴
        time_pattern = r'\[\d{1,2}:\d{2}:\d{2}\]'
        match = re.search(time_pattern, line)
        if match:
            return match.group(0)
        return None


class MdParser(DocumentParser):
    """Markdown文档解析器"""

    def parse(self, file_path: str) -> List[Dict]:
        """
        解析Markdown文档

        Args:
            file_path: MD文件路径

        Returns:
            解析结果列表
        """
        results = []

        # 尝试不同的编码格式
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        content = None

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            raise ValueError(f"无法使用常见编码读取文件: {file_path}")

        # 按行分割
        lines = content.split('\n')

        current_episode = "未知集数"  # 默认集数

        for i, line in enumerate(lines, 1):
            if line.strip():  # 只处理非空行
                stripped_line = line.strip()

                # 检查是否是集数标题
                if self.is_episode_title(stripped_line):
                    current_episode = stripped_line
                else:
                    # 检查是否包含时间轴格式，如 [00:02:36]
                    time_axis = self.extract_time_axis(stripped_line)

                    results.append({
                        'line_number': i,
                        'content': stripped_line,
                        'episode': current_episode,
                        'time_axis': time_axis if time_axis else 'N/A',
                        'file_path': file_path
                    })

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
        import re
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

        # 检查Markdown标题格式，如 # Death's Game S01E01
        markdown_header_pattern = r'^#{1,6}\s+.*?[Ss]\d+[Ee]\d+.*?$'  # 匹配包含SxEx的标题
        if re.match(markdown_header_pattern, line):
            return True

        return False

    def extract_time_axis(self, line: str) -> str:
        """
        从行中提取时间轴信息

        Args:
            line: 要检查的行

        Returns:
            时间轴信息，如果没有找到则返回None
        """
        import re
        # 匹配 [00:02:36] 格式的时间轴
        time_pattern = r'\[\d{1,2}:\d{2}:\d{2}\]'
        match = re.search(time_pattern, line)
        if match:
            return match.group(0)
        return None


class WordParser(DocumentParser):
    """Word文档解析器"""

    def parse(self, file_path: str) -> List[Dict]:
        """
        解析Word文档(.docx)

        Args:
            file_path: Word文件路径

        Returns:
            解析结果列表
        """
        try:
            from docx import Document
        except ImportError:
            raise ImportError("请安装python-docx: pip install python-docx")

        results = []
        doc = Document(file_path)

        current_episode = "未知集数"  # 默认集数

        for i, paragraph in enumerate(doc.paragraphs, 1):
            if paragraph.text.strip():  # 只处理非空段落
                content = paragraph.text.strip()

                # 检查是否是集数标题
                if self.is_episode_title(content):
                    current_episode = content
                else:
                    # 检查是否包含时间轴格式，如 [00:02:36]
                    time_axis = self.extract_time_axis(content)

                    results.append({
                        'line_number': i,
                        'content': content,
                        'episode': current_episode,
                        'time_axis': time_axis if time_axis else 'N/A',
                        'file_path': file_path
                    })

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
        import re
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

        # 检查Markdown标题格式，如 # Death's Game S01E01
        markdown_header_pattern = r'^#{1,6}\s+.*?[Ss]\d+[Ee]\d+.*?$'  # 匹配包含SxEx的标题
        if re.match(markdown_header_pattern, line):
            return True

        return False

    def extract_time_axis(self, line: str) -> str:
        """
        从行中提取时间轴信息

        Args:
            line: 要检查的行

        Returns:
            时间轴信息，如果没有找到则返回None
        """
        import re
        # 匹配 [00:02:36] 格式的时间轴
        time_pattern = r'\[\d{1,2}:\d{2}:\d{2}\]'
        match = re.search(time_pattern, line)
        if match:
            return match.group(0)
        return None


class PdfParser(DocumentParser):
    """PDF文档解析器"""

    def parse(self, file_path: str) -> List[Dict]:
        """
        解析PDF文档

        Args:
            file_path: PDF文件路径

        Returns:
            解析结果列表
        """
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError("请安装PyMuPDF: pip install PyMuPDF")

        results = []
        doc = fitz.open(file_path)

        line_number = 1
        current_episode = "未知集数"  # 默认集数

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()

            # 按行分割文本
            lines = text.split('\n')

            for line in lines:
                if line.strip():  # 只处理非空行
                    content = line.strip()

                    # 检查是否是集数标题
                    if self.is_episode_title(content):
                        current_episode = content
                    else:
                        # 检查是否包含时间轴格式，如 [00:02:36]
                        time_axis = self.extract_time_axis(content)

                        results.append({
                            'line_number': line_number,
                            'content': content,
                            'episode': current_episode,
                            'time_axis': time_axis if time_axis else 'N/A',
                            'file_path': file_path,
                            'page': page_num + 1  # 添加页码信息
                        })
                    line_number += 1

        doc.close()
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
        import re
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

        # 检查Markdown标题格式，如 # Death's Game S01E01
        markdown_header_pattern = r'^#{1,6}\s+.*?[Ss]\d+[Ee]\d+.*?$'  # 匹配包含SxEx的标题
        if re.match(markdown_header_pattern, line):
            return True

        return False

    def extract_time_axis(self, line: str) -> str:
        """
        从行中提取时间轴信息

        Args:
            line: 要检查的行

        Returns:
            时间轴信息，如果没有找到则返回None
        """
        import re
        # 匹配 [00:02:36] 格式的时间轴
        time_pattern = r'\[\d{1,2}:\d{2}:\d{2}\]'
        match = re.search(time_pattern, line)
        if match:
            return match.group(0)
        return None


def get_document_parser(file_path: str) -> DocumentParser:
    """
    根据文件扩展名获取相应的文档解析器
    
    Args:
        file_path: 文件路径
        
    Returns:
        对应的解析器实例
    """
    ext = Path(file_path).suffix.lower()
    
    if ext == '.txt':
        return TxtParser()
    elif ext in ['.md', '.markdown']:
        return MdParser()
    elif ext in ['.doc', '.docx']:
        return WordParser()
    elif ext == '.pdf':
        return PdfParser()
    else:
        raise ValueError(f"不支持的文档文件格式: {ext}")


def parse_document_file(file_path: str) -> List[Dict]:
    """
    解析文档文件的统一接口
    
    Args:
        file_path: 文档文件路径
        
    Returns:
        解析结果列表
    """
    parser = get_document_parser(file_path)
    return parser.parse(file_path)