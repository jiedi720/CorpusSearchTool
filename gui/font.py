"""
字体配置模块
统一管理不同语言的字体设置
"""

from PySide6.QtGui import QFont


class FontConfig:
    """字体配置类"""
    
    # 韩语字体
    KOREAN_FONT_FAMILY = "Malgun Gothic"
    KOREAN_FONT_SIZE = 11
    
    # 英语字体（使用系统默认）
    ENGLISH_FONT_FAMILY = ""  # 空字符串表示使用系统默认字体
    ENGLISH_FONT_SIZE = 11
    
    # 表格其他列字体
    TABLE_OTHER_FONT_FAMILY = ""
    TABLE_OTHER_FONT_SIZE = 10
    
    @staticmethod
    def get_korean_font(size=None):
        """
        获取韩语字体
        
        Args:
            size: 字体大小，如果为None则使用默认大小
            
        Returns:
            QFont: 韩语字体对象
        """
        font = QFont()
        font.setFamily(FontConfig.KOREAN_FONT_FAMILY)
        font.setPointSize(size if size is not None else FontConfig.KOREAN_FONT_SIZE)
        # 启用完全提示，消除字体锯齿
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        return font
    
    @staticmethod
    def get_english_font(size=None):
        """
        获取英语字体
        
        Args:
            size: 字体大小，如果为None则使用默认大小
            
        Returns:
            QFont: 英语字体对象
        """
        font = QFont()
        if FontConfig.ENGLISH_FONT_FAMILY:
            font.setFamily(FontConfig.ENGLISH_FONT_FAMILY)
        font.setPointSize(size if size is not None else FontConfig.ENGLISH_FONT_SIZE)
        return font
    
    @staticmethod
    def get_table_other_font(size=None):
        """
        获取表格其他列字体
        
        Args:
            size: 字体大小，如果为None则使用默认大小
            
        Returns:
            QFont: 表格其他列字体对象
        """
        font = QFont()
        if FontConfig.TABLE_OTHER_FONT_FAMILY:
            font.setFamily(FontConfig.TABLE_OTHER_FONT_FAMILY)
        font.setPointSize(size if size is not None else FontConfig.TABLE_OTHER_FONT_SIZE)
        return font