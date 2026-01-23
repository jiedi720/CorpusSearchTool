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
            'window_y': '-1'
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


# 全局配置管理器实例
config_manager = ConfigManager()