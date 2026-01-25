"""
搜索结果表格GUI设定模块
负责搜索结果表格的样式、布局、代理等GUI相关设定
"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QFont, QTextDocument, QPainter, QBrush, QLinearGradient, QPen
from PySide6.QtWidgets import QStyledItemDelegate, QTableWidget, QHeaderView, QStyleOptionViewItem, QSizePolicy, QMenu
from gui.font import FontConfig
from function.config_manager import ConfigManager

# 创建配置管理器实例
config_manager = ConfigManager()


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
        try:
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
            
            # 创建 QTextDocument 对象
            doc = QTextDocument()
            
            # 设置字体大小和字体族
            # 除了对应台词列（索引2）之外，其他列都使用10pt字体
            if index.column() == 2:  # 对应台词列
                # 根据当前语料库类型设置字体
                # 韩语使用 Noto Sans KR，英语使用系统默认
                # 这里统一使用较大的字体大小
                font = FontConfig.get_korean_font() if hasattr(self, 'current_search_params') and self.current_search_params.get('corpus_type') == 'korean' else FontConfig.get_english_font()
            else:  # 其他列（集数、时间轴、行号、文件名）
                font = FontConfig.get_table_other_font()
            doc.setDefaultFont(font)
            
            # 设置文档布局，控制行高
            doc.setDocumentMargin(0)
            
            # 获取当前搜索的关键词，用于高亮
            current_keywords = []
            if self.current_search_params:
                # 从当前搜索参数获取关键词
                keywords = self.current_search_params.get('keywords', '')
                if keywords:
                    # 处理关键词：可能是字符串或列表
                    if isinstance(keywords, str):
                        # 字符串：按空格分割
                        current_keywords = keywords.split()
                    elif isinstance(keywords, list):
                        # 列表：直接使用
                        current_keywords = keywords
                    # 同时添加生成的变体作为关键词
                    if self.variants:
                        current_keywords.extend(self.variants)
                    # 去重并过滤空字符串
                    current_keywords = [k for k in list(set(current_keywords)) if k]
            
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
                        # 使用正则表达式替换，不使用单词边界（适用于韩语）
                        regex_pattern = re.escape(keyword)
                        highlighted_text = re.sub(
                            rf'({regex_pattern})',
                            r'<b><span style="color: #ffff00;">\1</span></b>',
                            highlighted_text,
                            flags=re.IGNORECASE
                        )
                
                html_text = highlighted_text
            
            # 用前景色包裹文本
            final_html = f'<span style="color: {color.name()}; margin: 0px; padding: 0px; line-height: 1;">{html_text}</span>'
            
            doc.setHtml(final_html)
            
            # 设置文本宽度，确保换行正确
            doc.setTextWidth(option.rect.width() - 16)
            
            painter.save()
            
            # 根据对齐方式计算绘制位置
            text_width = doc.idealWidth()
            text_height = doc.size().height()
            
            # 添加左右边距
            padding_left = 8
            padding_right = 8
            available_width = option.rect.width() - padding_left - padding_right
            
            x = option.rect.left() + padding_left
            
            # 垂直居中：文字应该在单元格内垂直居中
            # 计算垂直居中的 y 坐标
            available_height = option.rect.height()
            y = option.rect.top() + (available_height - int(text_height)) / 2
            
            if alignment & Qt.AlignmentFlag.AlignHCenter:
                x += (available_width - text_width) / 2
            elif alignment & Qt.AlignmentFlag.AlignRight:
                x += available_width - text_width
            
            painter.translate(x, y)
            
            # 不裁剪绘制区域，允许文本超出单元格
            doc.drawContents(painter)
            painter.restore()
        except Exception as e:
            # 出错时显示简单的文本
            import traceback
            print(f"Error in paint: {e}")
            traceback.print_exc()
            # 回退到默认绘制
            super().paint(painter, option, index)
    
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
        # 除了对应台词列（索引2）之外，其他列都使用10pt字体
        if index.column() == 2:  # 对应台词列
            # 根据当前语料库类型设置字体
            font = FontConfig.get_korean_font() if hasattr(self, 'current_search_params') and self.current_search_params.get('corpus_type') == 'korean' else FontConfig.get_english_font()
        else:  # 其他列（集数、时间轴、行号、文件名）
            font = FontConfig.get_table_other_font()
        doc.setDefaultFont(font)
        
        # 设置文档布局，控制行高
        doc.setDocumentMargin(0)
        
        # 获取当前搜索的关键词，用于高亮
        current_keywords = []
        if self.current_search_params:
            # 从当前搜索参数获取关键词
            keywords = self.current_search_params.get('keywords', '')
            if keywords:
                # 处理关键词：可能是字符串或列表
                if isinstance(keywords, str):
                    # 字符串：按空格分割
                    current_keywords = keywords.split()
                elif isinstance(keywords, list):
                    # 列表：直接使用
                    current_keywords = keywords
                # 同时添加生成的变体作为关键词
                if self.variants:
                    current_keywords.extend(self.variants)
                # 去重并过滤空字符串
                current_keywords = [k for k in list(set(current_keywords)) if k]
        
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
                    # 使用正则表达式替换，不使用单词边界（适用于韩语）
                    regex_pattern = re.escape(keyword)
                    highlighted_text = re.sub(
                        rf'({regex_pattern})',
                        r'<b><span style="color: #ffff00;">\1</span></b>',
                        highlighted_text,
                        flags=re.IGNORECASE
                    )
            
            html_text = highlighted_text
        
        # 用前景色包裹文本
        final_html = f'<span style="color: #ffffff; margin: 0px; padding: 0px; line-height: 1.3;">{html_text}</span>'
        
        doc.setHtml(final_html)
        
        # 设置文本宽度，模拟实际渲染时的宽度限制
        # 减去左右边距（各8px）
        doc.setTextWidth(option.rect.width() - 16)
        
        # 计算文档实际高度
        text_height = doc.size().height()
        
        # 添加上下边距（各8px）
        row_height = int(text_height) + 16
        
        # 确保单行时至少30px（文字高度约14px + 上下各8px）
        if row_height < 30:
            row_height = 30
        
        # 返回固定高度，宽度使用文档的理想宽度
        return QSize(int(doc.idealWidth()), row_height)


class SearchResultTableManager:
    """搜索结果表格GUI管理器
    负责搜索结果表格的初始化、样式设置、布局调整等GUI相关操作
    """
    
    def __init__(self, result_table):
        """初始化表格管理器"""
        self.result_table = result_table
        self.html_delegate = None
        
        # 统一的列宽配置
        # 列索引: 0=集数, 1=时间轴, 2=对应台词, 3=行号, 4=文件名
        self.COLUMN_CONFIG = {
            0: {'mode': 'interactive', 'fixed_width': None, 'min_width': 100, 'max_width': 500, 'default': 200},
            1: {'mode': 'fixed', 'fixed_width': 80, 'min_width': None, 'max_width': None, 'default': 80},
            2: {'mode': 'interactive', 'fixed_width': None, 'min_width': 200, 'max_width': 800, 'default': 600},
            3: {'mode': 'fixed', 'fixed_width': 60, 'min_width': None, 'max_width': None, 'default': 60},
            4: {'mode': 'interactive', 'fixed_width': None, 'min_width': 150, 'max_width': 600, 'default': 200}
        }
    
    def get_column_config(self, column_index):
        """获取列配置
        
        Args:
            column_index: 列索引
            
        Returns:
            dict: 列配置字典，包含 mode, fixed_width, min_width, max_width, default
        """
        return self.COLUMN_CONFIG.get(column_index, {})
    
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
        self.result_table.verticalHeader().setMinimumSectionSize(30)
        self.result_table.verticalHeader().setVisible(False)
        
        # 初始化HTML代理
        self.html_delegate = HTMLDelegate(self.result_table)
        self.result_table.setItemDelegate(self.html_delegate)
        
        # 设置列数和列名
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels(['集数', '时间轴', '对应台词', '行号', '文件名'])
        
        # 设置表头
        header = self.result_table.horizontalHeader()
        header.setSectionsMovable(True)  # 允许列拖动
        header.setSectionsClickable(True)  # 允许点击列头排序
        header.setSortIndicatorShown(False)  # 默认不显示排序指示器
        
        # 创建自定义表头
        custom_header = CustomHeaderView(Qt.Orientation.Horizontal, self.result_table)
        self.result_table.setHorizontalHeader(custom_header)
        
        # 确保表头允许调整列宽
        custom_header.setSectionsMovable(True)  # 允许列拖动
        custom_header.setSectionsClickable(True)  # 允许点击列头排序
        custom_header.setHighlightSections(True)  # 高亮选中的列
        custom_header.setCascadingSectionResizes(True)  # 允许级联调整列宽
        
        # 设置列宽
        self.restore_column_settings()
        
        # 设置表格样式，参考搜索历史表格
        self.result_table.setStyleSheet("""
            QTableWidget {
                background-color: #1f1f1f;
                alternate-background-color: #252525;
                color: #ffffff;
                gridline-color: #404040;
                border: none;
                border-radius: 0px;
                font-size: 11pt;
                padding: 0px;
                margin: 0px;
            }
            QTableWidget::item:selected {
                background-color: #005a9e;
                color: white;
            }
            QTableWidget::item:hover {
                background-color: #3d3d3d;
                color: white;
            }
            QTableWidget::item {
                padding: 0px;
                margin: 0px;
            }
            QHeaderView {
                background-color: #505050;
                margin: 0;
                padding: 0;
            }

            QHeaderView::section {
                background-color: #505050;
                color: #ffffff;
                padding: 0px 0px;
                border: none;
                border-right: 1px solid #606060;
                border-bottom: 1px solid #606060;
                font-weight: bold;
                font-size: 10pt;
                margin: 0;
            }
            /* 移除section:first的border-left，避免影响边界对齐 */
        """)
        
        # 确保表格没有内边距，避免最右边留白
        self.result_table.setContentsMargins(0, 0, 0, 0)

        # 确保表头高度固定且没有额外空间
        header = self.result_table.horizontalHeader()
        header.setFixedHeight(30)
        header.setContentsMargins(0, 0, 0, 0)
        
        # 确保表格填满父容器
        self.result_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # 强制更新样式和布局
        self.result_table.updateGeometry()
        self.result_table.resize(self.result_table.parent().size())
        self.result_table.style().unpolish(self.result_table)
        self.result_table.style().polish(self.result_table)
        self.result_table.update()
        
        # 确保父容器布局正确
        if self.result_table.parent() and hasattr(self.result_table.parent(), 'updateGeometry'):
            self.result_table.parent().updateGeometry()
            self.result_table.parent().update()
    
    def restore_column_settings(self):
        """恢复列宽设置"""
        # 从配置文件加载列宽设置
        column_settings = config_manager.get_column_settings('result')
        column_widths = column_settings['widths']
        
        # 获取表头
        header = self.result_table.horizontalHeader()
        
        # 设置每列的调整模式
        for col in range(self.result_table.columnCount()):
            config = self.get_column_config(col)
            mode = config.get('mode', 'interactive')
            if mode == 'fixed':
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
            else:
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)

        # 禁用最后一列自动拉伸，允许手动调整
        header.setStretchLastSection(False)
        
        # 然后设置列宽
        for col in range(self.result_table.columnCount()):
            config = self.get_column_config(col)
            if config.get('mode') == 'fixed':
                # 固定列使用硬编码值，不受配置文件影响
                self.result_table.setColumnWidth(col, config['fixed_width'])
            else:
                # 可调整列：优先使用配置文件中的宽度，否则使用默认值
                width = column_widths[col] if col < len(column_widths) else 0
                if width <= 0:
                    width = config.get('default', 200)
                # 应用宽度限制
                min_width = config.get('min_width')
                max_width = config.get('max_width')
                if min_width is not None and max_width is not None:
                    width = min(max(min_width, width), max_width)
                self.result_table.setColumnWidth(col, width)
        
        # 重新连接sectionResized信号
        header.sectionResized.connect(self.enforce_min_column_width)
        
        # 确保表头高度为30px
        header.setFixedHeight(30)
        header.style().unpolish(header)
        header.style().polish(header)
        header.update()

    def enforce_min_column_width(self, logical_index, old_size, new_size):
        """强制执行列宽限制"""
        config = self.get_column_config(logical_index)
        
        # 检查是否为固定列
        if config.get('mode') == 'fixed':
            # 固定列：恢复为固定宽度
            self.result_table.blockSignals(True)
            self.result_table.setColumnWidth(logical_index, config['fixed_width'])
            self.result_table.blockSignals(False)
            return
        
        # 检查是否有宽度限制
        min_width = config.get('min_width')
        max_width = config.get('max_width')
        if min_width is not None and max_width is not None:
            if new_size < min_width:
                self.result_table.blockSignals(True)
                self.result_table.setColumnWidth(logical_index, min_width)
                self.result_table.blockSignals(False)
            elif new_size > max_width:
                self.result_table.blockSignals(True)
                self.result_table.setColumnWidth(logical_index, max_width)
                self.result_table.blockSignals(False)
    
    def clear_table(self):
        """清空表格"""
        self.result_table.setRowCount(0)
        self.result_table.clearContents()
    
    def set_table_theme(self, theme_mode):
        """设置表格主题
        
        Args:
            theme_mode: 主题模式 ('light' 或 'dark')
        """
        if theme_mode == 'dark':
            # 深色主题
            self.result_table.setStyleSheet("""
                QTableWidget {
                    background-color: #1f1f1f;
                    alternate-background-color: #252525;
                    color: #ffffff;
                    gridline-color: #404040;
                    border: none;
                    border-radius: 0px;
                    font-size: 11pt;
                    padding: 0px;
                    margin: 0px;
                }
                QTableWidget::item:selected {
                    background-color: #005a9e;
                    color: white;
                }
                QTableWidget::item:hover {
                    background-color: #3d3d3d;
                    color: white;
                }
                QTableWidget::item {
                    padding: 0px;
                    margin: 0px;
                }
                QHeaderView {
                    background-color: #505050;
                    margin: 0;
                    padding: 0;
                }
                QHeaderView::section {
                    background-color: #505050;
                    color: #ffffff;
                    padding: 0px 0px;
                    border: none;
                    border-right: 1px solid #606060;
                    border-bottom: 1px solid #606060;
                    font-weight: bold;
                    font-size: 10pt;
                    margin: 0;
                }
            """)
        else:
            # 浅色主题
            self.result_table.setStyleSheet("""
                QTableWidget {
                    background-color: #ffffff;
                    alternate-background-color: #f0f0f0;
                    color: #000000;
                    gridline-color: #d0d0d0;
                    border: none;
                    border-radius: 0px;
                    font-size: 11pt;
                    padding: 0px;
                    margin: 0px;
                }
                QTableWidget::item:selected {
                    background-color: #0078d4;
                    color: white;
                }
                QTableWidget::item:hover {
                    background-color: #e5f3ff;
                    color: black;
                }
                QTableWidget::item {
                    padding: 0px;
                    margin: 0px;
                }
                QHeaderView {
                    background-color: #f0f0f0;
                    margin: 0;
                    padding: 0;
                }
                QHeaderView::section {
                    background-color: #f0f0f0;
                    color: #000000;
                    padding: 0px 0px;
                    border: none;
                    border-right: 1px solid #d0d0d0;
                    border-bottom: 1px solid #d0d0d0;
                    font-weight: bold;
                    font-size: 10pt;
                    margin: 0;
                }
            """)


class CustomHeaderView(QHeaderView):
    """自定义表头，支持右键菜单显示/隐藏列"""
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.setHighlightSections(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # 不在这里连接信号，而是在主窗口类中连接
        
        # 拖拽相关属性
        self.dragging_section = -1
        self.drop_position = -1
        
        # 鼠标悬停相关属性
        self.hovered_section = -1
        
    def mousePressEvent(self, event):
        """处理鼠标按下事件"""
        if self.orientation() == Qt.Orientation.Horizontal:
            pos = event.position()
            
            # 检查鼠标是否在某一列的右边边缘（用于调整列宽）
            section = self.logicalIndexAt(pos.x())
            
            if section != -1:  # 鼠标在某个列上
                section_pos = self.sectionViewportPosition(section)
                section_width = self.sectionSize(section)
                
                # 检查鼠标是否在列的右边边缘（5像素内）
                if pos.x() >= section_pos + section_width - 5:
                    # 检查这一列是否是视觉上最右边的列
                    is_last_visible = True
                    for i in range(self.count()):
                        if not self.isSectionHidden(i) and i != section:
                            i_pos = self.sectionViewportPosition(i)
                            i_width = self.sectionSize(i)
                            if i_pos + i_width > section_pos + section_width:
                                is_last_visible = False
                                break
                    
                    # 如果是最右边的列的右边边缘，禁止拖拽
                    if is_last_visible:
                        return
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """处理鼠标移动事件，跟踪悬停列"""
        if self.orientation() != Qt.Orientation.Horizontal:
            return
        
        # 检查鼠标是否在某一列的右边边缘（用于调整列宽）
        pos = event.position()
        section = self.logicalIndexAt(pos.x())
        
        if section != -1:  # 鼠标在某个列上
            section_pos = self.sectionViewportPosition(section)
            section_width = self.sectionSize(section)
            
            # 检查鼠标是否在列的右边边缘（5像素内）
            if pos.x() >= section_pos + section_width - 5:
                # 检查这一列是否是视觉上最右边的列
                is_last_visible = True
                for i in range(self.count()):
                    if not self.isSectionHidden(i) and i != section:
                        i_pos = self.sectionViewportPosition(i)
                        i_width = self.sectionSize(i)
                        if i_pos + i_width > section_pos + section_width:
                            is_last_visible = False
                            break
                
                # 如果是最右边的列的右边边缘，不显示拖拽光标
                if is_last_visible:
                    self.unsetCursor()
                    return
        
        # 跟踪鼠标悬停的列
        if self.hovered_section != section:
            self.hovered_section = section
            self.update()
        
        super().mouseMoveEvent(event)
    
    def dragMoveEvent(self, event):
        """处理拖拽移动事件，显示插入符号"""
        super().dragMoveEvent(event)
        
        if self.orientation() != Qt.Orientation.Horizontal:
            return
        
        # 获取拖拽位置
        pos = event.position()
        logical_index = self.logicalIndexAt(pos.x())
        
        # 计算插入位置
        if logical_index == -1:
            # 拖拽到最后一列右边
            self.drop_position = self.count()
        else:
            section_pos = self.sectionViewportPosition(logical_index)
            if pos.x() < section_pos + self.sectionSize(logical_index) / 2:
                # 拖拽到列的左半部分，插入到当前列左边
                self.drop_position = self.visualIndex(logical_index)
            else:
                # 拖拽到列的右半部分，插入到当前列右边
                self.drop_position = self.visualIndex(logical_index) + 1
        
        # 更新显示
        self.update()
    
    def dragLeaveEvent(self, event):
        """处理拖拽离开事件，清除插入符号"""
        super().dragLeaveEvent(event)
        self.drop_position = -1
        self.update()
    
    def dropEvent(self, event):
        """处理拖拽放下事件，清除插入符号"""
        super().dropEvent(event)
        self.drop_position = -1
        self.update()
    
    def leaveEvent(self, event):
        """处理鼠标离开事件，清除悬停状态"""
        super().leaveEvent(event)
        if self.hovered_section != -1:
            self.hovered_section = -1
            self.update()
    
    def paintEvent(self, event):
        """绘制表头，包括插入符号和悬浮特效"""
        super().paintEvent(event)
        
        # 检查是否有需要绘制的内容
        if self.orientation() != Qt.Orientation.Horizontal:
            return
        
        # 只在需要绘制悬停特效或插入符号时才创建QPainter
        if self.hovered_section != -1 or self.drop_position != -1:
            # 使用with语句确保painter正确初始化和关闭
            try:
                viewport = self.viewport()
                if viewport is None:
                    return
                
                with QPainter(viewport) as painter:
                    # 绘制悬停特效
                    if self.hovered_section != -1:
                        # 获取悬停列的位置和大小
                        hovered_pos = self.sectionViewportPosition(self.hovered_section)
                        hovered_size = self.sectionSize(self.hovered_section)
                        
                        # 创建渐变背景
                        gradient = QLinearGradient(hovered_pos, 0, hovered_pos + hovered_size, 0)
                        gradient.setColorAt(0, QColor(0, 120, 215, 50))
                        gradient.setColorAt(1, QColor(0, 120, 215, 20))
                        
                        # 绘制渐变背景
                        painter.fillRect(hovered_pos, 0, hovered_size, self.height(), gradient)
                        
                        # 绘制边框
                        painter.setPen(QPen(QColor(0, 120, 215, 150), 2, Qt.PenStyle.SolidLine))
                        painter.drawRect(hovered_pos, 0, hovered_size, self.height())
                    
                    # 绘制插入符号
                    if self.drop_position != -1:
                        # 计算插入符号位置
                        if self.drop_position == 0:
                            # 插入到最左边
                            x = 0
                        elif self.drop_position >= self.count():
                            # 插入到最右边
                            x = self.sectionViewportPosition(self.count() - 1) + self.sectionSize(self.count() - 1)
                        else:
                            # 插入到中间位置
                            logical_index = self.logicalIndex(self.drop_position - 1)
                            x = self.sectionViewportPosition(logical_index) + self.sectionSize(logical_index)
                        
                        # 使用更明显的颜色（亮黄色）
                        indicator_color = QColor(255, 215, 0)  # 金黄色
                        painter.setPen(QPen(indicator_color, 3, Qt.PenStyle.SolidLine))
                        painter.setBrush(indicator_color)
                        
                        # 绘制垂直线
                        painter.drawLine(x, 0, x, self.height())
                        
                        # 绘制顶部箭头（向下指）
                        arrow_size = 12
                        top_arrow = [
                            QPoint(x, 0),
                            QPoint(x - arrow_size, arrow_size),
                            QPoint(x + arrow_size, arrow_size)
                        ]
                        painter.drawPolygon(top_arrow)
                        
                        # 绘制底部箭头（向上指）
                        bottom_arrow = [
                            QPoint(x, self.height()),
                            QPoint(x - arrow_size, self.height() - arrow_size),
                            QPoint(x + arrow_size, self.height() - arrow_size)
                        ]
                        painter.drawPolygon(bottom_arrow)
            except Exception as e:
                # 捕获所有异常，避免程序崩溃
                print(f"paintEvent error: {e}")