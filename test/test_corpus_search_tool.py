"""
测试模块
用于测试字幕语料库检索工具的各项功能
"""

import unittest
import os
import tempfile
from function.subtitle_parser import SrtParser, AssParser, VttParser
from function.document_parser import TxtParser, MdParser, WordParser, PdfParser
from function.search_engine import SearchEngine
from function.result_processor import ResultProcessor
from function.config_manager import ConfigManager
from function.search_history_manager import SearchHistoryManager


class TestCorpusSearchTool(unittest.TestCase):
    """字幕语料库检索工具测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.search_engine = SearchEngine()
        self.result_processor = ResultProcessor()
        self.config_manager = ConfigManager()
        self.search_history_manager = SearchHistoryManager()
    
    def test_srt_parser(self):
        """测试SRT解析器"""
        # 创建临时SRT文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as f:
            srt_content = """1
00:00:01,000 --> 00:00:03,000
这是第一行字幕

2
00:00:04,000 --> 00:00:06,000
这是第二行字幕
"""
            f.write(srt_content)
            temp_file = f.name
        
        try:
            parser = SrtParser()
            results = parser.parse(temp_file)
            
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0]['content'], '这是第一行字幕')
            self.assertEqual(results[1]['time_axis'], '00:00:04,000 --> 00:00:06,000')
        finally:
            os.unlink(temp_file)
    
    def test_txt_parser(self):
        """测试TXT解析器"""
        # 创建临时TXT文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            txt_content = """第一行文本
第二行文本
第三行文本"""
            f.write(txt_content)
            temp_file = f.name
        
        try:
            parser = TxtParser()
            results = parser.parse(temp_file)
            
            self.assertEqual(len(results), 3)
            self.assertEqual(results[0]['content'], '第一行文本')
            self.assertEqual(results[1]['line_number'], 2)
        finally:
            os.unlink(temp_file)
    
    def test_search_functionality(self):
        """测试搜索功能"""
        # 创建临时文件进行搜索测试
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            txt_content = """这是一个测试文件
包含一些测试内容
用于测试搜索功能"""
            f.write(txt_content)
            temp_file = f.name
        
        try:
            # 测试搜索
            results = self.search_engine.search_in_file(
                temp_file, 
                '测试', 
                case_sensitive=False, 
                fuzzy_match=False, 
                regex_enabled=False
            )
            
            self.assertGreater(len(results), 0)
            self.assertIn('测试', results[0]['content'])
        finally:
            os.unlink(temp_file)
    
    def test_result_processing(self):
        """测试结果处理"""
        mock_results = [
            {'file_path': 'test.srt', 'line_number': 1, 'content': '测试内容', 'time_axis': '00:00:01,000 --> 00:00:03,000'}
        ]
        
        formatted = self.result_processor.format_results_for_display(mock_results, 'subtitle')
        self.assertEqual(len(formatted), 1)
        self.assertEqual(formatted[0][0], 'test.srt')  # 文件名
        self.assertEqual(formatted[0][1], '00:00:01,000 --> 00:00:03,000')  # 时间轴
    
    def test_config_management(self):
        """测试配置管理"""
        # 测试设置和获取输入目录
        test_dir = '/tmp/test'
        self.config_manager.set_input_dir(test_dir)
        self.assertEqual(self.config_manager.get_input_dir(), test_dir)
        
        # 测试默认输出目录逻辑
        self.config_manager.set_output_dir('')  # 设置为空
        self.assertEqual(self.config_manager.get_output_dir(), test_dir)  # 应该等于输入目录
    
    def test_search_history(self):
        """测试搜索历史"""
        # 添加一条记录
        self.search_history_manager.add_record(
            keywords='test keyword',
            input_path='/path/to/input',
            output_path='/path/to/output'
        )
        
        # 获取最近记录
        recent = self.search_history_manager.get_recent_records(10)
        self.assertGreaterEqual(len(recent), 1)
        self.assertEqual(recent[-1]['keywords'], 'test keyword')


def run_tests():
    """运行所有测试"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()