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
            'current_tab': '0',  # 当前选择的标签页（0=英语，1=韩语）
            'theme': 'Light'  # 主题设置（Light/Dark/System）
        }
        self.config['COLUMNS'] = {
            'result_widths': '',
            'history_widths': '',
            'result_order': '',
            'result_visibility': '',
            'history_order': '',
            'history_visibility': ''
        }
        # 英语语料库配置
        self.config['ENGLISH'] = {
            'input_dir': '',
            'output_dir': '',
            'keyword_type': '0',  # 关键词类型索引
            'case_sensitive': 'False',
            'fuzzy_match': 'False',
            'regex_enabled': 'False'
        }
        # 韩语语料库配置
        self.config['KOREAN'] = {
            'input_dir': '',
            'output_dir': '',
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
        """获取当前语料库的输入目录"""
        # 根据当前选择的标签页确定语料库类型
        current_tab = self.get_current_tab()
        section = 'ENGLISH' if current_tab == 0 else 'KOREAN'
        return self.config.get(section, 'input_dir', fallback='')
    
    def set_input_dir(self, input_dir: str):
        """设置当前语料库的输入目录"""
        # 根据当前选择的标签页确定语料库类型
        current_tab = self.get_current_tab()
        section = 'ENGLISH' if current_tab == 0 else 'KOREAN'
        
        if section not in self.config:
            self.config[section] = {}
        self.config.set(section, 'input_dir', input_dir)
    
    def get_output_dir(self) -> str:
        """获取当前语料库的输出目录"""
        # 根据当前选择的标签页确定语料库类型
        current_tab = self.get_current_tab()
        section = 'ENGLISH' if current_tab == 0 else 'KOREAN'
        output_dir = self.config.get(section, 'output_dir', fallback='')
        # 如果输出目录为空，则返回输入目录作为默认值
        if output_dir == '':
            return self.get_input_dir()
        return output_dir
    
    def set_output_dir(self, output_dir: str):
        """设置当前语料库的输出目录"""
        # 根据当前选择的标签页确定语料库类型
        current_tab = self.get_current_tab()
        section = 'ENGLISH' if current_tab == 0 else 'KOREAN'
        
        if section not in self.config:
            self.config[section] = {}
        
        if output_dir == '' or output_dir is None:
            # 如果未指定输出目录，则默认同源
            self.config.set(section, 'output_dir', self.get_input_dir())
        else:
            self.config.set(section, 'output_dir', output_dir)
    
    def get_ui_settings(self) -> dict:
        """获取UI设置"""
        ui_settings = {
            'width': self.config.getint('UI', 'window_width', fallback=800),
            'height': self.config.getint('UI', 'window_height', fallback=600),
            'x': self.config.getint('UI', 'window_x', fallback=-1),
            'y': self.config.getint('UI', 'window_y', fallback=-1),
            'theme': self.config.get('UI', 'theme', fallback='Light')
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
    
    def get_theme(self) -> str:
        """获取主题设置"""
        return self.config.get('UI', 'theme', fallback='Light')
    
    def set_theme(self, theme: str):
        """设置主题设置
        
        Args:
            theme: 主题模式，可选值: "Light", "Dark" 或 "System"
        """
        if 'UI' not in self.config:
            self.config['UI'] = {}
        self.config.set('UI', 'theme', theme)
    
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
        
        # 按每列分开获取宽度设置
        widths = []
        column_index = 0
        while True:
            width_key = f'{table_name}_column_{column_index}_width'
            if width_key in self.config['COLUMNS']:
                widths.append(self.config.getint('COLUMNS', width_key))
                column_index += 1
            else:
                break
        
        # 获取顺序和可见性设置
        order_key = f'{table_name}_order'
        visibility_key = f'{table_name}_visibility'
        
        order_str = self.config.get('COLUMNS', order_key, fallback='')
        visibility_str = self.config.get('COLUMNS', visibility_key, fallback='')
        
        order = [int(o) for o in order_str.split(',') if o] if order_str else []
        visibility = [bool(int(v)) for v in visibility_str.split(',') if v] if visibility_str else []
        
        return {'widths': widths, 'order': order, 'visibility': visibility}
    
    def set_column_settings(self, table_name: str, widths: list, order: list = None, visibility: list = None):
        """
        设置列设置

        Args:
            table_name: 表格名称（'result' 或 'history'）
            widths: 列宽列表
            order: 列顺序列表（可选，默认使用当前顺序）
            visibility: 列显示状态列表（True表示可见，False表示隐藏，可选）
        """
        if 'COLUMNS' not in self.config:
            self.config['COLUMNS'] = {}
        
        # 按每列分开保存宽度设置
        for i, width in enumerate(widths):
            width_key = f'{table_name}_column_{i}_width'
            self.config.set('COLUMNS', width_key, str(width))
        
        # 删除超出范围的旧列宽设置
        column_index = len(widths)
        while True:
            width_key = f'{table_name}_column_{column_index}_width'
            if width_key in self.config['COLUMNS']:
                del self.config['COLUMNS'][width_key]
                column_index += 1
            else:
                break
        
        # 获取顺序和可见性设置的键
        order_key = f'{table_name}_order'
        visibility_key = f'{table_name}_visibility'
        
        # 如果提供了order参数，则保存，否则使用默认顺序
        if order is not None:
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
        
        input_dir = self.config.get(section, 'input_dir', fallback='')
        output_dir = self.config.get(section, 'output_dir', fallback='')
        
        # 如果输出目录为空，则使用输入目录作为默认值
        if output_dir == '':
            output_dir = input_dir
        
        return {
            'input_dir': input_dir,
            'output_dir': output_dir,
            'keyword_type': self.config.get(section, 'keyword_type', fallback=''),
            'case_sensitive': self.config.getboolean(section, 'case_sensitive', fallback=False),
            'fuzzy_match': self.config.getboolean(section, 'fuzzy_match', fallback=False),
            'regex_enabled': self.config.getboolean(section, 'regex_enabled', fallback=False)
        }
    
    def set_corpus_config(self, corpus_type: str, input_dir: str = None, output_dir: str = None, keyword_type: str = None,
                         case_sensitive: bool = None, fuzzy_match: bool = None, regex_enabled: bool = None):
        """
        设置语料库配置
        
        Args:
            corpus_type: 语料库类型 ('english' 或 'korean')
            input_dir: 输入目录
            output_dir: 输出目录
            keyword_type: 关键词类型（实际选项文本）
            case_sensitive: 是否区分大小写
            fuzzy_match: 是否模糊匹配
            regex_enabled: 是否启用正则表达式
        """
        section = 'ENGLISH' if corpus_type.lower() == 'english' else 'KOREAN'
        
        if section not in self.config:
            self.config[section] = {}
        
        # 先设置输入目录（如果提供）
        if input_dir is not None:
            self.config.set(section, 'input_dir', input_dir)
        
        # 处理输出目录，如果为空或None，则使用输入目录作为默认值
        if output_dir is not None:
            if output_dir == '' or output_dir is None:
                # 使用输入目录作为默认值
                current_input_dir = self.config.get(section, 'input_dir', fallback='')
                self.config.set(section, 'output_dir', current_input_dir)
            else:
                self.config.set(section, 'output_dir', output_dir)
        else:
            # 如果output_dir参数为None，检查配置中是否已存在output_dir
            # 如果不存在或为空，则使用输入目录作为默认值
            current_output_dir = self.config.get(section, 'output_dir', fallback='')
            current_input_dir = self.config.get(section, 'input_dir', fallback='')
            if current_output_dir == '' or current_output_dir is None:
                self.config.set(section, 'output_dir', current_input_dir)
            else:
                # 如果已存在output_dir且不为空，则保持不变
                pass
        
        if keyword_type is not None:
            self.config.set(section, 'keyword_type', keyword_type)
        if case_sensitive is not None:
            self.config.set(section, 'case_sensitive', str(case_sensitive))
        if fuzzy_match is not None:
            self.config.set(section, 'fuzzy_match', str(fuzzy_match))
        if regex_enabled is not None:
            self.config.set(section, 'regex_enabled', str(regex_enabled))
        
        # 确保input_dir和output_dir在配置中的顺序：input_dir在前，output_dir在后
        # 1. 获取当前section的所有选项
        section_items = dict(self.config[section])
        
        # 2. 移除input_dir和output_dir，稍后重新添加以保证顺序
        if 'input_dir' in section_items:
            del section_items['input_dir']
        if 'output_dir' in section_items:
            del section_items['output_dir']
        
        # 3. 创建新的有序字典，先添加input_dir和output_dir，再添加其他选项
        new_section_items = {}
        
        # 添加input_dir（如果存在）
        if 'input_dir' in self.config[section]:
            new_section_items['input_dir'] = self.config[section]['input_dir']
        
        # 添加output_dir（如果存在）
        if 'output_dir' in self.config[section]:
            new_section_items['output_dir'] = self.config[section]['output_dir']
        
        # 添加其他选项
        new_section_items.update(section_items)
        
        # 4. 清空并重新填充section
        self.config[section].clear()
        for key, value in new_section_items.items():
            self.config[section][key] = value


# 全局配置管理器实例
config_manager = ConfigManager()