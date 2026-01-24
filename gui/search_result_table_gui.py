# -*- coding: utf-8 -*-
"""
搜索结果表格GUI设定模块
负责搜索结果表格的样式、布局、代理等GUI相关设定
"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QFont, QTextDocument, QPainter, QBrush
from PySide6.QtWidgets import QStyledItemDelegate, QTableWidget, QHeaderView, QStyleOptionViewItem


class HTMLDelegate(QStyledItemDelegate):
    """自定义代理类，支持 HTML 渲染和关键词高亮"""
    
    def __init__(self, parent=None, search_params=None, variants=None):
        """初始化代理类"""
        super().__init__(parent)
        self.current_search_params = search_params if search_params else {}
        self.variants = variants if variants else []
    
    def set_search_params(self, search_params, variants=None):
        """设置搜索参数，用于关键词高亮"""
        self.current_search_params = search_params if search_params else {}
        self.variants = variants if variants else []
    
    def paint(self, painter, option, index):
        """绘制单元格"""
        model = index.model()
        text = model.data(index, Qt.ItemDataRole.DisplayRole)
        
        # 处理 None 值
        if text is None:
            text = ''
        
        # 获取前景色
        foreground = model.data(index, Qt.ItemDataRole.ForegroundRole)
        if foreground is None:
            color = QColor('#ffffff')  # 默认白色
        else:
            # foreground 是 QBrush 对象，需要获取其颜色
            color = foreground.color()
        
        # 获取文本对齐方式
        alignment = model.data(index, Qt.ItemDataRole.TextAlignmentRole)
        if alignment is None:
            alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        
        # 设置文本选项，支持 HTML
        option.features |= QStyleOptionViewItem.ViewItemFeature.HasDisplay
        
        # 使用 HTML 渲染
        doc = QTextDocument()
        
        # 设置字体大小
        font = QFont()
        # 除了对应台词列（索引2）之外，其他列都使用10pt字体
        if index.column() == 2:  # 对应台词列
            font.setPointSize(11)
        else:  # 其他列（集数、时间轴、行号、文件名）
            font.setPointSize(10)
        doc.setDefaultFont(font)
        
        # 获取当前搜索的关键词，用于高亮
        current_keywords = []
        if self.current_search_params:
            # 从当前搜索参数获取关键词
            keywords = self.current_search_params.get('keywords', '')
            if keywords:
                # 简单处理：按空格分割关键词
                current_keywords = keywords.split()
                # 同时添加生成的变体作为关键词
                if self.variants:
                    current_keywords.extend(self.variants)
                # 去重
                current_keywords = list(set(current_keywords))
        
        # 处理文本，添加关键词高亮
        plain_text = str(text)
        html_text = plain_text
        
        # 如果有关键词，添加高亮
        if current_keywords:
            import re
            # 确保关键词按长度降序排列，避免短关键词匹配长关键词的一部分
            current_keywords.sort(key=lambda x: len(x), reverse=True)
            
            # 创建高亮后的HTML文本
            highlighted_text = plain_text
            for keyword in current_keywords:
                if keyword:
                    # 使用正则表达式替换，确保只替换完整的单词，不区分大小写
                    regex_pattern = re.escape(keyword)
                    highlighted_text = re.sub(
                        rf'(\b{regex_pattern}\b)',
                        r'<b><span style="color: #ffff00;">\1</span></b>',
                        highlighted_text,
                        flags=re.IGNORECASE
                    )
            
            html_text = highlighted_text
        
        # 用前景色包裹文本
        final_html = f'<span style="color: {color.name()};">{html_text}</span>'
        
        doc.setHtml(final_html)
        doc.setTextWidth(option.rect.width())
        
        painter.save()
        
        # 根据对齐方式计算绘制位置
        text_width = doc.idealWidth()
        text_height = doc.size().height()
        
        x = option.rect.left()
        y = option.rect.top() + (option.rect.height() - text_height) / 2
        
        if alignment & Qt.AlignmentFlag.AlignHCenter:
            x += (option.rect.width() - text_width) / 2
        elif alignment & Qt.AlignmentFlag.AlignRight:
            x += option.rect.width() - text_width
        
        painter.translate(x, y)
        
        # 不裁剪绘制区域，允许文本超出单元格
        doc.drawContents(painter)
        painter.restore()
    
    def sizeHint(self, option, index):
        """返回单元格大小"""
        model = index.model()
        text = model.data(index, Qt.ItemDataRole.DisplayRole)
        
        # 处理 None 值
        if text is None:
            text = ''
        
        # 保留HTML标签，正确计算带有HTML的文本大小
        doc = QTextDocument()
        
        # 设置字体大小
        font = QFont()
        # 除了对应台词列（索引2）之外，其他列都使用10pt字体
        if index.column() == 2:  # 对应台词列
            font.setPointSize(11)
        else:  # 其他列（集数、时间轴、行号、文件名）
            font.setPointSize(10)
        doc.setDefaultFont(font)
        
        # 获取当前搜索的关键词，用于高亮
        current_keywords = []
        if self.current_search_params:
            # 从当前搜索参数获取关键词
            keywords = self.current_search_params.get('keywords', '')
            if keywords:
                # 简单处理：按空格分割关键词
                current_keywords = keywords.split()
                # 同时添加生成的变体作为关键词
                if self.variants:
                    current_keywords.extend(self.variants)
                # 去重
                current_keywords = list(set(current_keywords))
        
        # 处理文本，添加关键词高亮，用于计算尺寸
        plain_text = str(text)
        html_text = plain_text
        
        # 如果有关键词，添加高亮
        if current_keywords:
            import re
            # 确保关键词按长度降序排列，避免短关键词匹配长关键词的一部分
            current_keywords.sort(key=lambda x: len(x), reverse=True)
            
            # 创建高亮后的HTML文本
            highlighted_text = plain_text
            for keyword in current_keywords:
                if keyword:
                    # 使用正则表达式替换，确保只替换完整的单词，不区分大小写
                    regex_pattern = re.escape(keyword)
                    highlighted_text = re.sub(
                        rf'(\b{regex_pattern}\b)',
                        r'<b><span style="color: #ffff00;">\1</span></b>',
                        highlighted_text,
                        flags=re.IGNORECASE
                    )
            
            html_text = highlighted_text
        
        # 用前景色包裹文本
        final_html = f'<span style="color: #ffffff;">{html_text}</span>'
        
        doc.setHtml(final_html)
        # 不设置文本宽度，让文档自然计算宽度
        
        # 返回固定高度，宽度使用文档的理想宽度
        return QSize(int(doc.idealWidth()), 30)  # 高度为30，与行高一致


class SearchResultTableManager:
    """搜索结果表格GUI管理器
    负责搜索结果表格的初始化、样式设置、布局调整等GUI相关操作
    """
    
    def __init__(self, result_table):
        """初始化表格管理器"""
        self.result_table = result_table
        self.html_delegate = None
    
    def initialize_table(self):
        """初始化表格设置"""
        # 设置表格属性
        self.result_table.setAlternatingRowColors(True)
        self.result_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.result_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.result_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.result_table.setWordWrap(False)  # 禁止文字换行
        self.result_table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)  # 像素级横向滚动
        self.result_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # 需要时显示横向滚动条
        
        # 设置行高
        self.result_table.verticalHeader().setDefaultSectionSize(30)
        self.result_table.verticalHeader().setVisible(False)
        
        # 初始化HTML代理
        self.html_delegate = HTMLDelegate(self.result_table)
        self.result_table.setItemDelegate(self.html_delegate)
        
        # 设置右键菜单
        self.result_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        
        # 应用初始样式
        self.fix_table_style()
    
    def fix_table_style(self):
        """修复表格样式和布局"""
        # 清除UI设计器生成的错误样式
        self.result_table.setStyleSheet("")
        
        # 设置表格样式
        self.result_table.setStyleSheet("""
            /* 表格主体样式 */
            QTableWidget {
                background-color: #1f1f1f;
                alternate-background-color: #252525;
                color: #ffffff;
                gridline-color: #404040;
                border: 1px solid #404040;
                border-radius: 5px;
                font-size: 11pt;
                margin: 0;
                padding: 0;
            }
            
            /* 表格项样式 */
            QTableWidget::item:selected {
                background-color: #005a9e;
                color: white;
            }
            
            QTableWidget::item:hover {
                background-color: #3d3d3d;
                color: white;
            }
            
            /* 表头样式 */
            QHeaderView {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #404040;
                font-size: 10pt;
                font-weight: bold;
            }
            
            QHeaderView::section {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #404040;
                padding: 5px;
                min-height: 30px;
            }
            
            QHeaderView::section:checked {
                background-color: #005a9e;
            }
            
            /* 表头在Dark主题下的样式 */
            QHeaderView[theme="dark"] {
                background-color: #2a2a2a;
                color: #ffffff;
            }
            
            QHeaderView[theme="dark"]::section {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #404040;
            }
            
            /* 表头在Light主题下的样式 */
            QHeaderView[theme="light"] {
                background-color: #f0f0f0;
                color: #000000;
            }
            
            QHeaderView[theme="light"]::section {
                background-color: #f0f0f0;
                color: #000000;
                border: 1px solid #cccccc;
            }
        """)
    
    def set_table_theme(self, theme_mode):
        """设置表格主题"""
        # 特别为result_table的表头设置theme属性
        header = self.result_table.horizontalHeader()
        if header:
            header.setProperty("theme", theme_mode)
            # 强制刷新表头样式
            header.style().unpolish(header)
            header.style().polish(header)
        
        # 强制刷新result_table的样式
        self.result_table.style().unpolish(self.result_table)
        self.result_table.style().polish(self.result_table)
        self.result_table.update()
    
    def set_search_params(self, search_params, variants=None):
        """设置搜索参数，用于关键词高亮"""
        if self.html_delegate:
            self.html_delegate.set_search_params(search_params, variants)
            self.result_table.update()
    
    def reset_column_widths(self):
        """重置列宽"""
        self.result_table.setColumnWidth(0, 200)  # 出处列
        self.result_table.setColumnWidth(1, 30)   # 时间轴列（固定）
        self.result_table.setColumnWidth(2, 600)  # 对应台词列
        self.result_table.setColumnWidth(3, 50)   # 行号列（固定）
        self.result_table.setColumnWidth(4, 200)  # 文件名列
    
    def get_html_delegate(self):
        """获取HTML代理对象"""
        return self.html_delegate
