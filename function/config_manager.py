"""
配置管理模块
负责读取和写入配置文件，管理应用程序的配置信息
"""

import configparser
import os
from typing import Optional


class ConfigManager:
    """配置管理类"""
    
    def __init__(self, config_file: str = "CorpusSearchTool.ini"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件名
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
        else:
            # 如果配置文件不存在，则创建默认配置
            self.create_default_config()
    
    def create_default_config(self):
        """创建默认配置"""
        self.config['DEFAULT'] = {}
        self.config['PATH'] = {
            'input_dir': '',
            'output_dir': '',
        }
        self.config['SEARCH'] = {
            'case_sensitive': 'False',
            'fuzzy_match': 'False',
            'regex_enabled': 'False'
        }
        self.config['UI'] = {
            'window_width': '800',
            'window_height': '600',
            'window_x': '-1',  # -1表示居中
            'window_y': '-1',
            'current_tab': '0'  # 当前选择的标签页（0=英语，1=韩语）
        }
        self.config['COLUMNS'] = {
            'result_widths': '',
            'result_order': '',
            'result_visibility': '',
            'history_widths': '',
            'history_order': '',
            'history_visibility': ''
        }
        # 英语语料库配置
        self.config['ENGLISH'] = {
            'input_dir': '',
            'keyword_type': '0',  # 关键词类型索引
            'case_sensitive': 'False',
            'fuzzy_match': 'False',
            'regex_enabled': 'False'
        }
        # 韩语语料库配置
        self.config['KOREAN'] = {
            'input_dir': '',
            'keyword_type': '0',  # 关键词类型索引
            'case_sensitive': 'False',
            'fuzzy_match': 'False',
            'regex_enabled': 'False'
        }
        
        self.save_config()
    
    def save_config(self):
        """保存配置到文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get_input_dir(self) -> str:
        """获取输入目录"""
        return self.config.get('PATH', 'input_dir', fallback='')
    
    def set_input_dir(self, input_dir: str):
        """设置输入目录"""
        if 'PATH' not in self.config:
            self.config['PATH'] = {}
        self.config.set('PATH', 'input_dir', input_dir)
    
    def get_output_dir(self) -> str:
        """获取输出目录"""
        return self.config.get('PATH', 'output_dir', fallback='')
    
    def set_output_dir(self, output_dir: str):
        """设置输出目录"""
        if 'PATH' not in self.config:
            self.config['PATH'] = {}
        if output_dir == '' or output_dir is None:
            # 如果未指定输出目录，则默认同源
            self.config.set('PATH', 'output_dir', self.get_input_dir())
        else:
            self.config.set('PATH', 'output_dir', output_dir)
    
    def get_ui_settings(self) -> dict:
        """获取UI设置"""
        ui_settings = {
            'width': self.config.getint('UI', 'window_width', fallback=800),
            'height': self.config.getint('UI', 'window_height', fallback=600),
            'x': self.config.getint('UI', 'window_x', fallback=-1),
            'y': self.config.getint('UI', 'window_y', fallback=-1)
        }
        return ui_settings
    
    def set_ui_settings(self, width: int, height: int, x: int, y: int):
        """设置UI设置"""
        if 'UI' not in self.config:
            self.config['UI'] = {}
        self.config.set('UI', 'window_width', str(width))
        self.config.set('UI', 'window_height', str(height))
        self.config.set('UI', 'window_x', str(x))
        self.config.set('UI', 'window_y', str(y))
    
    def get_search_settings(self) -> dict:
        """获取搜索设置"""
        search_settings = {
            'case_sensitive': self.config.getboolean('SEARCH', 'case_sensitive', fallback=False),
            'fuzzy_match': self.config.getboolean('SEARCH', 'fuzzy_match', fallback=False),
            'regex_enabled': self.config.getboolean('SEARCH', 'regex_enabled', fallback=False)
        }
        return search_settings
    
    def set_search_settings(self, case_sensitive: bool = None, fuzzy_match: bool = None, regex_enabled: bool = None):
        """设置搜索设置"""
        if 'SEARCH' not in self.config:
            self.config['SEARCH'] = {}
        
        if case_sensitive is not None:
            self.config.set('SEARCH', 'case_sensitive', str(case_sensitive))
        if fuzzy_match is not None:
            self.config.set('SEARCH', 'fuzzy_match', str(fuzzy_match))
        if regex_enabled is not None:
            self.config.set('SEARCH', 'regex_enabled', str(regex_enabled))
    
    def get_column_settings(self, table_name: str) -> dict:
        """
        获取列设置

        Args:
            table_name: 表格名称（'result' 或 'history'）

        Returns:
            列设置字典，包含 'widths'、'order' 和 'visibility'
        """
        if 'COLUMNS' not in self.config:
            return {'widths': [], 'order': [], 'visibility': []}
        
        widths_key = f'{table_name}_widths'
        order_key = f'{table_name}_order'
        visibility_key = f'{table_name}_visibility'
        
        widths_str = self.config.get('COLUMNS', widths_key, fallback='')
        order_str = self.config.get('COLUMNS', order_key, fallback='')
        visibility_str = self.config.get('COLUMNS', visibility_key, fallback='')
        
        widths = [int(w) for w in widths_str.split(',') if w] if widths_str else []
        order = [int(o) for o in order_str.split(',') if o] if order_str else []
        visibility = [bool(int(v)) for v in visibility_str.split(',') if v] if visibility_str else []
        
        return {'widths': widths, 'order': order, 'visibility': visibility}
    
    def set_column_settings(self, table_name: str, widths: list, order: list, visibility: list = None):
        """
        设置列设置

        Args:
            table_name: 表格名称（'result' 或 'history'）
            widths: 列宽列表
            order: 列顺序列表
            visibility: 列显示状态列表（True表示可见，False表示隐藏）
        """
        if 'COLUMNS' not in self.config:
            self.config['COLUMNS'] = {}
        
        widths_key = f'{table_name}_widths'
        order_key = f'{table_name}_order'
        visibility_key = f'{table_name}_visibility'
        
        self.config.set('COLUMNS', widths_key, ','.join(str(w) for w in widths))
        self.config.set('COLUMNS', order_key, ','.join(str(o) for o in order))
        if visibility is not None:
            self.config.set('COLUMNS', visibility_key, ','.join(str(int(v)) for v in visibility))
    
    def get_current_tab(self) -> int:
        """获取当前选择的标签页（0=英语，1=韩语）"""
        return self.config.getint('UI', 'current_tab', fallback=0)
    
    def set_current_tab(self, tab_index: int):
        """设置当前选择的标签页"""
        if 'UI' not in self.config:
            self.config['UI'] = {}
        self.config.set('UI', 'current_tab', str(tab_index))
    
    def get_corpus_config(self, corpus_type: str) -> dict:
        """
        获取语料库配置
        
        Args:
            corpus_type: 语料库类型 ('english' 或 'korean')
            
        Returns:
            语料库配置字典
        """
        section = 'ENGLISH' if corpus_type.lower() == 'english' else 'KOREAN'
        
        return {
            'input_dir': self.config.get(section, 'input_dir', fallback=''),
            'keyword_type': self.config.get(section, 'keyword_type', fallback=''),
            'case_sensitive': self.config.getboolean(section, 'case_sensitive', fallback=False),
            'fuzzy_match': self.config.getboolean(section, 'fuzzy_match', fallback=False),
            'regex_enabled': self.config.getboolean(section, 'regex_enabled', fallback=False)
        }
    
    def set_corpus_config(self, corpus_type: str, input_dir: str = None, keyword_type: str = None,
                         case_sensitive: bool = None, fuzzy_match: bool = None, regex_enabled: bool = None):
        """
        设置语料库配置
        
        Args:
            corpus_type: 语料库类型 ('english' 或 'korean')
            input_dir: 输入目录
            keyword_type: 关键词类型（实际选项文本）
            case_sensitive: 是否区分大小写
            fuzzy_match: 是否模糊匹配
            regex_enabled: 是否启用正则表达式
        """
        section = 'ENGLISH' if corpus_type.lower() == 'english' else 'KOREAN'
        
        if section not in self.config:
            self.config[section] = {}
        
        if input_dir is not None:
            self.config.set(section, 'input_dir', input_dir)
        if keyword_type is not None:
            self.config.set(section, 'keyword_type', keyword_type)
        if case_sensitive is not None:
            self.config.set(section, 'case_sensitive', str(case_sensitive))
        if fuzzy_match is not None:
            self.config.set(section, 'fuzzy_match', str(fuzzy_match))
        if regex_enabled is not None:
            self.config.set(section, 'regex_enabled', str(regex_enabled))


# 全局配置管理器实例
config_manager = ConfigManager()