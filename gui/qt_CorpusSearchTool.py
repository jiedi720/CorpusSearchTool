#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CorpusSearchTool GUI 模块
仿照 qt_SubtitleToolbox.py 的结构模式
实现语料库检索工具的GUI界面和用户交互功能
"""

import os
import sys
import threading
from pathlib import Path

# PySide6 导入
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QCheckBox, QGroupBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QMenu, QMessageBox, QFileDialog,
    QProgressBar, QStatusBar, QSplitter, QFrame, QStyledItemDelegate,
    QStyleOptionViewItem, QTabWidget, QComboBox
)
from PySide6.QtCore import Qt, QThread, Signal, QPoint, QSettings, QSize
from PySide6.QtGui import QColor, QFont, QAction, QIcon, QCursor, QDragEnterEvent, QDropEvent, QTextDocument

# 功能模块导入
from function.config_manager import config_manager
from function.search_engine_kor import search_engine_kor
from function.search_engine_eng import search_engine_eng
from function.result_processor import result_processor
from function.result_exporter import result_exporter
from function.search_history_manager import search_history_manager
from gui.search_history_gui import SearchHistoryWindow


class SearchThread(QThread):
    """搜索线程"""
    progress_updated = Signal(int)
    search_completed = Signal(list)
    search_failed = Signal(str)
    
    def __init__(self, input_path, keywords, case_sensitive, fuzzy_match, regex_enabled, 
                 corpus_type="english", keyword_type="", exact_match=False):
        super().__init__()
        self.input_path = input_path
        self.keywords = keywords
        self.case_sensitive = case_sensitive
        self.fuzzy_match = fuzzy_match
        self.regex_enabled = regex_enabled
        self.corpus_type = corpus_type  # "english" 或 "korean"
        self.keyword_type = keyword_type  # 关键词类型
        self.exact_match = exact_match  # 是否完全匹配（引号内）
    
    def run(self):
        """执行搜索"""
        try:
            # 获取所有支持的文件
            supported_extensions = ['.md']
            files_to_search = []
            
            if os.path.isfile(self.input_path):
                files_to_search.append(self.input_path)
            elif os.path.isdir(self.input_path):
                for root, dirs, files in os.walk(self.input_path):
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in supported_extensions):
                            files_to_search.append(os.path.join(root, file))
            
            total_files = len(files_to_search)
            if total_files == 0:
                self.search_completed.emit([])
                return
            
            # 韩语模式特殊处理
            if self.corpus_type == "korean":
                # 韩语模式：韩语没有大小写之分，使用 case_sensitive=True
                # 但为了兼容性，我们保留用户的选择，只是不使用模糊匹配
                self.fuzzy_match = False
                results = []  # 初始化 results 变量
                
                # 检查是否需要韩语变形匹配
                import re
                korean_pattern = re.compile(r'[\uac00-\ud7af]')
                contains_korean = bool(korean_pattern.search(self.keywords))
                
                print(f"[DEBUG] 韩语模式搜索:")
                print(f"  关键词: '{self.keywords}'")
                print(f"  关键词类型: '{self.keyword_type}'")
                print(f"  包含韩语: {contains_korean}")
                print(f"  正则表达式: {self.regex_enabled}")
                print(f"  文件总数: {total_files}")
                
                # 判断是否使用变形匹配：关键词类型是"单词"且包含韩语且不是正则表达式
                # 并且关键词以"다"结尾（动词/形容词）
                use_variant_matching = (
                    self.keyword_type == "单词" and 
                    contains_korean and 
                    not self.regex_enabled and
                    self.keywords.endswith('다')
                )
                
                # 判断是否使用惯用语匹配
                use_idiom_matching = (
                    self.keyword_type == "惯用语" and 
                    contains_korean and 
                    not self.regex_enabled and
                    not self.exact_match
                )
                
                # 判断是否使用完全匹配（引号内）
                if self.exact_match:
                    # 使用完全匹配功能
                    print(f"[DEBUG] 使用完全匹配: '{self.keywords}'")
                    for i, file_path in enumerate(files_to_search):
                        file_results = search_engine_kor.search_exact_match(
                            file_path,
                            self.keywords,
                            case_sensitive=True
                        )
                        print(f"[DEBUG] 文件 {file_path}: 找到 {len(file_results)} 个结果")
                        results.extend(file_results)
                        
                        # 更新进度
                        progress = int((i + 1) / total_files * 100)
                        self.progress_updated.emit(progress)
                elif use_idiom_matching:
                    # 使用惯用语匹配功能
                    print(f"[DEBUG] 使用惯用语匹配")
                    for i, file_path in enumerate(files_to_search):
                        file_results = search_engine_kor.search_korean_idiom(
                            file_path,
                            self.keywords,
                            case_sensitive=True
                        )
                        print(f"[DEBUG] 文件 {file_path}: 找到 {len(file_results)} 个结果")
                        results.extend(file_results)
                        
                        # 更新进度
                        progress = int((i + 1) / total_files * 100)
                        self.progress_updated.emit(progress)
                elif use_variant_matching:
                    # 使用韩语变形匹配功能（动词/形容词）
                    print(f"[DEBUG] 使用变形匹配（动词/形容词）")
                    for i, file_path in enumerate(files_to_search):
                        file_results = search_engine_kor.search_korean_variants(
                            file_path,
                            self.keywords.split(),
                            case_sensitive=True  # 韩语使用区分大小写（实际不影响）
                        )
                        print(f"[DEBUG] 文件 {file_path}: 找到 {len(file_results)} 个结果")
                        results.extend(file_results)
                        
                        # 更新进度
                        progress = int((i + 1) / total_files * 100)
                        self.progress_updated.emit(progress)
                else:
                    # 名词/副词类型或非韩语内容：严格匹配
                    print(f"[DEBUG] 使用严格匹配（名词/副词）")
                    keyword_list = self.keywords.split()
                    print(f"[DEBUG] 关键词列表: {keyword_list}")
                    for i, file_path in enumerate(files_to_search):
                        try:
                            file_results = search_engine_kor.search_in_file(
                                file_path,
                                keyword_list,
                                case_sensitive=True,  # 韩语使用区分大小写（实际不影响）
                                fuzzy_match=False,  # 强制不使用模糊匹配
                                regex_enabled=self.regex_enabled
                            )
                            if file_results:
                                print(f"[DEBUG] 文件 {file_path}: 找到 {len(file_results)} 个结果")
                            results.extend(file_results)
                        except Exception as e:
                            print(f"[ERROR] 处理文件 {file_path} 时出错: {str(e)}")
                        
                        # 更新进度
                        progress = int((i + 1) / total_files * 100)
                        self.progress_updated.emit(progress)
                
                print(f"[DEBUG] 搜索完成，共找到 {len(results)} 个结果")
            else:
                # 英语模式：使用用户设置
                # 检查是否需要韩语/英语变形匹配
                import re
                korean_pattern = re.compile(r'[\uac00-\ud7af]')
                contains_korean = bool(korean_pattern.search(self.keywords))
                
                results = []
                
                if contains_korean and not self.regex_enabled:
                    # 使用韩语变形匹配功能
                    for i, file_path in enumerate(files_to_search):
                        file_results = search_engine_eng.search_english_variants(
                            file_path,
                            self.keywords.split(),
                            case_sensitive=self.case_sensitive
                        )
                        results.extend(file_results)
                        
                        # 更新进度
                        progress = int((i + 1) / total_files * 100)
                        self.progress_updated.emit(progress)
                else:
                    # 常规搜索
                    keyword_list = self.keywords.split()
                    
                    for i, file_path in enumerate(files_to_search):
                        try:
                            file_results = search_engine_eng.search_in_file(
                                file_path,
                                keyword_list,
                                case_sensitive=self.case_sensitive,
                                fuzzy_match=self.fuzzy_match,
                                regex_enabled=self.regex_enabled
                            )
                            results.extend(file_results)
                        except Exception as e:
                            print(f"处理文件 {file_path} 时出错: {str(e)}")
                        
                        # 更新进度
                        progress = int((i + 1) / total_files * 100)
                        self.progress_updated.emit(progress)
            
            # 处理结果以供显示
            if results:
                has_time_axis = any('time_axis' in result and result.get('time_axis', 'N/A') != 'N/A' for result in results)
                file_type = 'subtitle' if has_time_axis else 'document'
                formatted_results = result_processor.format_results_for_display(results, file_type)
            else:
                formatted_results = []
            
            self.search_completed.emit(formatted_results)
            
        except Exception as e:
            self.search_failed.emit(str(e))


class CustomHeaderView(QHeaderView):
    """自定义表头，禁止拖拽最后一列的右边"""
    
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsMovable(True)
    
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
        """处理鼠标移动事件"""
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
                    
                    # 如果是最右边的列的右边边缘，不显示拖拽光标
                    if is_last_visible:
                        self.unsetCursor()
                        return
        
        super().mouseMoveEvent(event)


class HTMLDelegate(QStyledItemDelegate):
    """自定义代理类，支持 HTML 渲染"""
    
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
        
        # 设置文本选项，支持 HTML
        option.features |= QStyleOptionViewItem.ViewItemFeature.HasDisplay
        
        # 使用 HTML 渲染
        doc = QTextDocument()
        
        # 设置默认字体大小为 11pt
        font = QFont()
        font.setPointSize(11)
        doc.setDefaultFont(font)
        
        # 检查文本是否已经是HTML格式（包含HTML标签）
        import re
        is_html = bool(re.search(r'<[^>]+>', text))
        
        if not is_html:
            # 如果不是HTML，使用前景色包裹文本
            text = f'<span style="color: {color.name()};">{text}</span>'
        
        doc.setHtml(text)
        # 不设置文本宽度，允许文本自然延伸
        
        painter.save()
        painter.translate(option.rect.topLeft())
        # 不裁剪绘制区域，允许文本超出单元格
        doc.drawContents(painter)
        painter.restore()
    
    def sizeHint(self, option, index):
        """返回单元格大小"""
        model = index.model()
        text = model.data(index, Qt.ItemDataRole.DisplayRole)
        
        doc = QTextDocument()
        
        # 设置默认字体大小为 11pt
        font = QFont()
        font.setPointSize(11)
        doc.setDefaultFont(font)
        
        doc.setHtml(text)
        # 不设置文本宽度，让文档自然计算宽度
        
        # 返回固定高度，宽度使用文档的理想宽度
        return QSize(int(doc.idealWidth()), 30)  # 高度为30，与行高一致


class CorpusSearchToolGUI(QMainWindow):
    """
    语料库检索工具主窗口GUI类
    仿照 qt_SubtitleToolbox.py 的结构模式
    """
    
    def __init__(self, root=None, controller=None):
        """
        初始化主窗口
        
        Args:
            root: 根窗口对象（PySide6中不需要，保留为兼容）
            controller: 应用程序控制器（可选）
        """
        super().__init__()
        self.root = root
        self.app = controller
        
        # 设置接受拖拽
        self.setAcceptDrops(True)
        
        # 定义配色方案
        self.colors = {
            'bg': '#353535',  # 深灰色背景
            'secondary_bg': '#404040',  # 次要背景色
            'dark_bg': '#1f1f1f',
            'dark_secondary_bg': '#2d2d2d',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'dark_text_primary': '#ffffff',
            'accent': '#0078d4',
            'accent_hover': '#006cbd',
            'highlight': '#ff6b35',
        }
        
        # 初始化变量
        self.history_window = None
        self.result_file_paths = []
        self.search_thread = None
        
        # 加载配置
        self.load_settings()
        
        # 设置窗口属性
        self.setup_window()
        
        # 设置样式主题
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 设置样式
        self.setup_styles()
        
        # 标记初始化完成
        self._initialized = True
    
    def load_settings(self):
        """加载配置"""
        self.ui_settings = config_manager.get_ui_settings()
        self.search_settings = config_manager.get_search_settings()
    
    def setup_window(self):
        """设置窗口属性"""
        self.setWindowTitle("字幕语料库检索工具")
        
        # 设置图标
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", "CorpusSearchTool.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 设置窗口大小
        if self.ui_settings:
            self.resize(self.ui_settings.get('width', 1200), self.ui_settings.get('height', 800))
        else:
            self.resize(1200, 800)
        
        # 设置窗口位置
        if self.ui_settings and 'pos_x' in self.ui_settings and 'pos_y' in self.ui_settings:
            self.move(self.ui_settings['pos_x'], self.ui_settings['pos_y'])
        else:
            self.center_window()
    
    def center_window(self):
        """居中窗口"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
    
    def setup_styles(self):
        """设置样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #353535;
            }
            QWidget {
                background-color: #353535;
            }
            QTabWidget::pane {
                background-color: #353535;
                border: 1px solid #505050;
                border-radius: 8px;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #404040;
                color: #cccccc;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 9pt;
            }
            QTabBar::tab:selected {
                background-color: #353535;
                color: #ffffff;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: #4a4a4a;
            }
            QGroupBox {
                background-color: #404040;
                border: 1px solid #505050;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                padding-left: 10px;
                padding-right: 10px;
                padding-bottom: 10px;
                font-weight: bold;
                font-size: 10pt;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: #404040;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #505050;
                border: 1px solid #606060;
                border-radius: 5px;
                padding: 8px 10px;
                font-size: 9pt;
                min-height: 28px;
                color: #ffffff;
            }
            QLineEdit::placeholder {
                color: #999999;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                font-size: 9pt;
                font-weight: bold;
                min-height: 32px;
            }
            QPushButton:hover {
                background-color: #006cbd;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #606060;
                color: #999999;
            }
            QCheckBox {
                font-size: 9pt;
                color: #ffffff;
                spacing: 8px;
                padding: 5px;
            }
            QComboBox {
                background-color: #505050;
                border: 1px solid #606060;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 9pt;
                min-height: 28px;
                color: #ffffff;
            }
            QComboBox:hover {
                border: 1px solid #0078d4;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #cccccc;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #505050;
                border: 1px solid #606060;
                selection-background-color: #0078d4;
                selection-color: white;
                color: #ffffff;
                padding: 5px;
            }
            QLabel {
                font-size: 9pt;
                color: #ffffff;
            }
            QTableWidget {
                background-color: #1f1f1f;
                alternate-background-color: #252525;
                color: #ffffff;
                gridline-color: #404040;
                border: none;
                font-size: 9pt;
            }
            QTableWidget::item:selected {
                background-color: #005a9e;
                color: white;
            }
            QHeaderView::section {
                background-color: #505050;
                color: #ffffff;
                padding: 5px 8px;
                border: none;
                border-right: 1px solid #606060;
                border-bottom: 1px solid #606060;
                font-weight: bold;
                font-size: 9pt;
                min-height: 30px;
            }
            QHeaderView::section:first {
                border-left: 1px solid #606060;
            }
            QScrollBar:vertical {
                background-color: #1f1f1f;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background-color: #404040;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QProgressBar {
                border: 1px solid #606060;
                border-radius: 5px;
                text-align: center;
                background-color: #505050;
                min-height: 25px;
                font-size: 8pt;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 4px;
            }
            QStatusBar {
                background-color: #404040;
                color: #cccccc;
                border-top: 1px solid #505050;
                padding: 8px 15px;
                font-size: 8pt;
            }
            QMenu {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 3px;
                color: #ffffff;
            }
            QMenu::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background-color: #404040;
                margin: 5px 10px;
            }
        """)
    
    def create_widgets(self):
        """创建界面元素"""
        # 主控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 创建搜索输入区域
        self.create_search_area(main_layout)
        
        # 创建搜索结果区域
        self.create_result_area(main_layout)
        
        # 创建状态栏
        self.create_status_bar()
    
    def create_search_area(self, parent_layout):
        """创建搜索输入区域"""
        # 创建标签页控件
        tab_widget = QTabWidget()
        
        # 创建英语语料库标签页
        english_tab = QWidget()
        english_layout = QVBoxLayout(english_tab)
        english_layout.setSpacing(12)
        
        # 创建韩语语料库标签页
        korean_tab = QWidget()
        korean_layout = QVBoxLayout(korean_tab)
        korean_layout.setSpacing(12)
        
        # 为两个标签页创建相同的布局
        self.create_corpus_tab(english_layout, "english")
        self.create_corpus_tab(korean_layout, "korean")
        
        # 添加标签页
        tab_widget.addTab(english_tab, "英语语料库")
        tab_widget.addTab(korean_tab, "韩语语料库")
        
        # 恢复上次选择的标签页
        last_tab = config_manager.get_current_tab()
        tab_widget.setCurrentIndex(last_tab)
        
        # 保存当前选中的标签页
        self.current_corpus_tab = tab_widget.currentIndex()
        tab_widget.currentChanged.connect(self.on_corpus_tab_changed)
        
        parent_layout.addWidget(tab_widget)
    
    def create_corpus_tab(self, parent_layout, corpus_type):
        """创建语料库标签页内容"""
        # 加载该语料库的配置
        corpus_config = config_manager.get_corpus_config(corpus_type)
        
        # 第一行：输入路径
        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)
        
        path_label = QLabel("输入路径:")
        path_label.setMinimumWidth(80)
        
        # 创建独立的输入路径编辑框
        input_path_edit = QLineEdit()
        input_path_edit.setText(corpus_config['input_dir'])
        input_path_edit.setPlaceholderText("选择文件或目录...")
        
        # 创建独立的浏览按钮
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self.browse_input_path)
        browse_btn.setMinimumWidth(80)
        
        # 保存到实例变量，便于后续访问
        if corpus_type == "english":
            self.english_input_path_edit = input_path_edit
            self.english_browse_btn = browse_btn
        else:
            self.korean_input_path_edit = input_path_edit
            self.korean_browse_btn = browse_btn
        
        path_layout.addWidget(path_label)
        path_layout.addWidget(input_path_edit)
        path_layout.addWidget(browse_btn)
        parent_layout.addLayout(path_layout)
        
        # 第二行：关键词 + 按钮布局
        keyword_button_layout = QHBoxLayout()
        keyword_button_layout.setSpacing(15)
        
        # 左侧：关键词
        keyword_container = QWidget()
        keyword_layout = QHBoxLayout(keyword_container)
        keyword_layout.setContentsMargins(0, 0, 0, 0)
        
        keyword_label = QLabel("关键词:")
        keyword_label.setMinimumWidth(80)
        
        # 创建关键词类型下拉列表
        if corpus_type == "english":
            # 英语语料库关键词类型选项
            keyword_combo = QComboBox()
            keyword_combo.addItems(["名词 & 副词", "动词", "形容词", "词组"])
            keyword_combo.setMinimumWidth(150)
            # 从配置中获取关键词类型文本并设置
            keyword_type_text = corpus_config['keyword_type']
            if keyword_type_text:
                index = keyword_combo.findText(keyword_type_text)
                if index >= 0:
                    keyword_combo.setCurrentIndex(index)
            
            # 创建英语关键词输入框
            keyword_edit = QLineEdit()
            keyword_edit.setPlaceholderText("输入搜索关键词...")
            
            # 保存到实例变量
            self.english_keyword_combo = keyword_combo
            self.english_keyword_edit = keyword_edit
        else:
            # 韩语语料库关键词类型选项
            keyword_combo = QComboBox()
            keyword_combo.addItems(["单词", "惯用语"])
            keyword_combo.setMinimumWidth(150)
            # 从配置中获取关键词类型文本并设置
            keyword_type_text = corpus_config['keyword_type']
            if keyword_type_text:
                index = keyword_combo.findText(keyword_type_text)
                if index >= 0:
                    keyword_combo.setCurrentIndex(index)
            
            # 创建韩语关键词输入框
            keyword_edit = QLineEdit()
            keyword_edit.setPlaceholderText("输入搜索关键词...")
            
            # 保存到实例变量
            self.korean_keyword_combo = keyword_combo
            self.korean_keyword_edit = keyword_edit
        
        keyword_layout.addWidget(keyword_label)
        keyword_layout.addWidget(keyword_combo)
        keyword_layout.addWidget(keyword_edit)
        
        # 右侧：按钮
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(15)
        
        # 创建独立的搜索按钮
        search_btn = QPushButton("🔍 开始搜索")
        search_btn.clicked.connect(self.start_search)
        search_btn.setMinimumWidth(140)
        search_btn.setMaximumWidth(140)
        
        # 创建独立的历史按钮
        history_btn = QPushButton("📜 搜索历史")
        history_btn.clicked.connect(self.show_search_history)
        history_btn.setMinimumWidth(140)
        history_btn.setMaximumWidth(140)
        
        # 保存到实例变量
        if corpus_type == "english":
            self.english_search_btn = search_btn
            self.english_history_btn = history_btn
        else:
            self.korean_search_btn = search_btn
            self.korean_history_btn = history_btn
        
        button_layout.addWidget(search_btn)
        button_layout.addWidget(history_btn)
        
        keyword_button_layout.addWidget(keyword_container, 1)
        keyword_button_layout.addWidget(button_container, 0)
        parent_layout.addLayout(keyword_button_layout)
        
        # 第三行：搜索选项
        options_layout = QHBoxLayout()
        options_layout.setSpacing(20)
        
        # 根据语料库类型创建不同的搜索选项
        if corpus_type == "english":
            # 英语模式：显示完整选项
            case_sensitive_check = QCheckBox("区分大小写")
            case_sensitive_check.setChecked(corpus_config['case_sensitive'])
            
            fuzzy_match_check = QCheckBox("模糊匹配")
            fuzzy_match_check.setChecked(corpus_config['fuzzy_match'])
            
            regex_check = QCheckBox("正则表达式")
            regex_check.setChecked(corpus_config['regex_enabled'])
            
            # 保存到实例变量
            self.english_case_sensitive_check = case_sensitive_check
            self.english_fuzzy_match_check = fuzzy_match_check
            self.english_regex_check = regex_check
            
            options_layout.addWidget(case_sensitive_check)
            options_layout.addWidget(fuzzy_match_check)
            options_layout.addWidget(regex_check)
        else:
            # 韩语模式：只显示正则表达式选项
            regex_check = QCheckBox("正则表达式")
            regex_check.setChecked(corpus_config['regex_enabled'])
            
            # 保存到实例变量
            self.korean_regex_check = regex_check
            
            options_layout.addWidget(regex_check)
        
        options_layout.addStretch()
        
        parent_layout.addLayout(options_layout)
    
    def on_corpus_tab_changed(self, index):
        """标签页切换事件"""
        # 保存当前标签页的配置
        self.save_current_tab_config()
        
        # 更新当前标签页索引
        self.current_corpus_tab = index
        print(f"切换到标签页: {index}")
    
    def save_current_tab_config(self):
        """保存当前标签页的配置"""
        if self.current_corpus_tab == 0:  # 英语语料库
            corpus_type = "english"
            input_path = self.english_input_path_edit.text().strip()
            keyword_type = self.english_keyword_combo.currentText()  # 获取实际选项文本
            case_sensitive = self.english_case_sensitive_check.isChecked()
            fuzzy_match = self.english_fuzzy_match_check.isChecked()
            regex_enabled = self.english_regex_check.isChecked()
        else:  # 韩语语料库
            corpus_type = "korean"
            input_path = self.korean_input_path_edit.text().strip()
            keyword_type = self.korean_keyword_combo.currentText()  # 获取实际选项文本
            case_sensitive = False  # 韩语不区分大小写
            fuzzy_match = False  # 韩语不使用模糊匹配
            regex_enabled = self.korean_regex_check.isChecked()
        
        # 保存配置
        config_manager.set_corpus_config(
            corpus_type=corpus_type,
            input_dir=input_path,
            keyword_type=keyword_type,
            case_sensitive=case_sensitive,
            fuzzy_match=fuzzy_match,
            regex_enabled=regex_enabled
        )
        config_manager.save_config()
    
    def get_current_keyword(self):
        """获取当前标签页的关键词"""
        if self.current_corpus_tab == 0:  # 英语语料库
            return self.english_keyword_edit.text()
        else:  # 韩语语料库
            return self.korean_keyword_edit.text()
    
    def get_current_keyword_type(self):
        """获取当前标签页的关键词类型"""
        if self.current_corpus_tab == 0:  # 英语语料库
            return self.english_keyword_combo.currentText()
        else:  # 韩语语料库
            return self.korean_keyword_combo.currentText()
    
    def create_result_area(self, parent_layout):
        """创建搜索结果区域"""
        result_group = QGroupBox("📋 搜索结果")
        result_layout = QVBoxLayout(result_group)
        result_layout.setSpacing(10)
        result_layout.setContentsMargins(10, 15, 10, 10)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumHeight(25)
        result_layout.addWidget(self.progress_bar)
        
        # 表格
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels(['文件名', '行号', '集数', '时间轴', '对应台词'])
        
        # 设置表格属性
        self.result_table.setAlternatingRowColors(True)
        self.result_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.result_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.result_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.result_table.setWordWrap(False)  # 禁止文字换行
        self.result_table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)  # 像素级横向滚动
        self.result_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # 需要时显示横向滚动条
        
        # 启用 HTML 格式渲染
        self.result_table.setItemDelegate(HTMLDelegate(self.result_table))
        
        # 设置列宽
        header = CustomHeaderView(Qt.Orientation.Horizontal, self.result_table)
        self.result_table.setHorizontalHeader(header)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # 最右边的列自动拉伸
        # 设置初始列宽
        self.result_table.setColumnWidth(0, 200)
        self.result_table.setColumnWidth(1, 80)
        self.result_table.setColumnWidth(2, 150)
        self.result_table.setColumnWidth(3, 120)
        header.setFixedHeight(30)  # 设置表头高度与表格行高一致
        
        # 启用列拖拽和右键菜单
        header.setSectionsMovable(True)  # 允许列拖拽调整顺序
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self.show_header_context_menu)
        
        # 恢复列宽和顺序
        self.restore_column_settings()
        
        # 设置行高
        self.result_table.verticalHeader().setDefaultSectionSize(30)
        self.result_table.verticalHeader().setVisible(False)
        
        # 设置右键菜单
        self.result_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.result_table.customContextMenuRequested.connect(self.show_context_menu)
        
        # 设置表格样式
        self.result_table.setStyleSheet("""
            QTableWidget {
                background-color: #1f1f1f;
                alternate-background-color: #252525;
                gridline-color: #404040;
                border: 1px solid #404040;
                border-radius: 5px;
                font-size: 11pt;
            }
            QTableWidget::item:selected {
                background-color: #005a9e;
                color: white;
            }
            QTableWidget::item:hover {
                background-color: #2d2d2d;
            }
            QHeaderView::section {
                background-color: #505050;
                color: #ffffff;
                padding: 5px 8px;
                border: none;
                border-right: 1px solid #606060;
                border-bottom: 1px solid #606060;
                font-weight: bold;
                font-size: 10pt;
                min-height: 30px;
            }
            QHeaderView::section:first {
                border-left: 1px solid #606060;
            }
        """)
        
        result_layout.addWidget(self.result_table)
        
        parent_layout.addWidget(result_group)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("✓ 准备就绪")
        self.setStatusBar(self.status_bar)
    
    def browse_input_path(self):
        """浏览输入路径"""
        # 获取当前标签页的输入框路径作为默认路径
        if self.current_corpus_tab == 0:  # 英语语料库
            current_path = self.english_input_path_edit.text().strip()
        else:  # 韩语语料库
            current_path = self.korean_input_path_edit.text().strip()
        
        # 如果当前路径为空或不存在，使用当前工作目录
        if not current_path or not os.path.exists(current_path):
            current_path = os.getcwd()
        
        # 使用 QFileDialog.getExistingDirectory 选择文件夹
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "选择语料库文件夹",
            current_path,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if dir_path:
            # 获取当前标签页的输入框
            if self.current_corpus_tab == 0:  # 英语语料库
                self.english_input_path_edit.setText(dir_path)
            else:  # 韩语语料库
                self.korean_input_path_edit.setText(dir_path)
    
    def start_search(self):
        """开始搜索"""
        # 获取当前标签页的控件值
        if self.current_corpus_tab == 0:  # 英语语料库
            input_path = self.english_input_path_edit.text().strip()
            keywords = self.english_keyword_edit.text().strip()
            case_sensitive = self.english_case_sensitive_check.isChecked()
            fuzzy_match = self.english_fuzzy_match_check.isChecked()
            regex_enabled = self.english_regex_check.isChecked()
        else:  # 韩语语料库
            input_path = self.korean_input_path_edit.text().strip()
            keywords = self.korean_keyword_edit.text().strip()
            case_sensitive = False  # 韩语不区分大小写
            fuzzy_match = False  # 韩语不使用模糊匹配
            regex_enabled = self.korean_regex_check.isChecked()
        
        if not input_path:
            QMessageBox.warning(self, "❌ 错误", "请输入输入路径")
            return
        
        if not keywords:
            QMessageBox.warning(self, "❌ 错误", "请输入关键词")
            return
        
        # 检查是否是引号内的完全匹配
        exact_match = False
        if keywords.startswith('"') and keywords.endswith('"'):
            exact_match = True
            keywords = keywords[1:-1]  # 去掉引号
            print(f"[DEBUG] 检测到引号内完全匹配: '{keywords}'")
        
        # 保存搜索参数到实例变量，用于保存历史记录
        self.current_search_params = {
            'keywords': keywords,
            'input_path': input_path,
            'case_sensitive': case_sensitive,
            'fuzzy_match': fuzzy_match,
            'regex_enabled': regex_enabled,
            'exact_match': exact_match
        }
        
        # 更新配置
        config_manager.set_input_dir(input_path)
        config_manager.set_search_settings(
            case_sensitive=case_sensitive,
            fuzzy_match=fuzzy_match,
            regex_enabled=regex_enabled
        )
        
        # 获取语料库类型和关键词类型
        if self.current_corpus_tab == 0:  # 英语语料库
            corpus_type = "english"
            keyword_type = self.english_keyword_combo.currentText()
        else:  # 韩语语料库
            corpus_type = "korean"
            keyword_type = self.korean_keyword_combo.currentText()
        
        # 保存关键词类型到参数中
        self.current_search_params['keyword_type'] = keyword_type
        
        # 禁用当前标签页的搜索按钮
        if self.current_corpus_tab == 0:  # 英语语料库
            self.english_search_btn.setEnabled(False)
        else:  # 韩语语料库
            self.korean_search_btn.setEnabled(False)
        self.status_bar.showMessage("⏳ 正在搜索...")
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 创建并启动搜索线程
        self.search_thread = SearchThread(
            input_path,
            keywords,
            case_sensitive,
            fuzzy_match,
            regex_enabled,
            corpus_type=corpus_type,
            keyword_type=keyword_type,
            exact_match=exact_match
        )
        self.search_thread.progress_updated.connect(self.update_progress)
        self.search_thread.search_completed.connect(self.search_completed)
        self.search_thread.search_failed.connect(self.search_failed)
        self.search_thread.start()
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
        self.status_bar.showMessage(f"⏳ 正在搜索... {value}%")
    
    def search_completed(self, results):
        """搜索完成"""
        # 隐藏进度条
        self.progress_bar.setVisible(False)
        
        # 启用搜索按钮
        if self.current_corpus_tab == 0:  # 英语语料库
            self.english_search_btn.setEnabled(True)
        else:  # 韩语语料库
            self.korean_search_btn.setEnabled(True)
        
        # 清空表格
        self.result_table.setRowCount(0)
        self.result_file_paths = []
        
        if not results:
            self.status_bar.showMessage("✓ 搜索完成，未找到结果")
            QMessageBox.information(self, "✓ 搜索完成", "未找到匹配结果")
            return
        
        # 填充表格
        self.result_table.setRowCount(len(results))
        for row, result in enumerate(results):
            # 处理不同类型的结果
            if isinstance(result, dict):
                # 字典类型
                filename = result.get('filename', '')
                lineno = result.get('lineno', '')
                episode = result.get('episode', '')
                time_axis = result.get('time_axis', '')
                text = result.get('text', '')
                filepath = result.get('filepath', '')
            elif isinstance(result, list) and len(result) >= 5:
                # 列表类型 [filename, lineno, episode, time_axis, text, filepath]
                filename = result[0] if len(result) > 0 else ''
                lineno = result[1] if len(result) > 1 else ''
                episode = result[2] if len(result) > 2 else ''
                time_axis = result[3] if len(result) > 3 else ''
                text = result[4] if len(result) > 4 else ''
                filepath = result[5] if len(result) > 5 else ''
            else:
                # 未知类型，跳过
                continue
            
            # 文件名
            filename_item = QTableWidgetItem(str(filename))
            filename_item.setForeground(QColor('#4ec9b0'))
            self.result_table.setItem(row, 0, filename_item)
            
            # 行号
            lineno_item = QTableWidgetItem(str(lineno))
            lineno_item.setForeground(QColor('#ce9178'))
            self.result_table.setItem(row, 1, lineno_item)
            
            # 集数
            episode_item = QTableWidgetItem(str(episode))
            episode_item.setForeground(QColor('#dcdcaa'))
            self.result_table.setItem(row, 2, episode_item)
            
            # 时间轴
            time_item = QTableWidgetItem(str(time_axis))
            time_item.setForeground(QColor('#569cd6'))
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # 居中对齐
            self.result_table.setItem(row, 3, time_item)
            
            # 对应台词
            text_item = QTableWidgetItem(str(text))
            text_item.setForeground(QColor('#ffffff'))
            self.result_table.setItem(row, 4, text_item)
            
            # 保存文件路径
            self.result_file_paths.append(filepath)
        
        # 保存搜索历史到对应的文件
        if hasattr(self, 'current_search_params'):
            corpus_type = "eng" if self.current_corpus_tab == 0 else "kor"
            search_history_manager.set_corpus_type(corpus_type)
            search_history_manager.add_record(
                keywords=self.current_search_params['keywords'],
                input_path=self.current_search_params['input_path'],
                case_sensitive=self.current_search_params['case_sensitive'],
                fuzzy_match=self.current_search_params['fuzzy_match'],
                regex_enabled=self.current_search_params['regex_enabled'],
                result_count=len(results),
                keyword_type=self.current_search_params.get('keyword_type', '')
            )
        
        self.status_bar.showMessage(f"✓ 搜索完成，找到 {len(results)} 条结果")
    
    def search_failed(self, error_message):
        """搜索失败"""
        # 隐藏进度条
        self.progress_bar.setVisible(False)
        
        # 启用搜索按钮
        if self.current_corpus_tab == 0:  # 英语语料库
            self.english_search_btn.setEnabled(True)
        else:  # 韩语语料库
            self.korean_search_btn.setEnabled(True)
        
        self.status_bar.showMessage("❌ 搜索失败")
        QMessageBox.critical(self, "❌ 搜索失败", error_message)
    
    def show_search_history(self):
        """显示搜索历史"""
        # 根据当前标签页设置语料库类型
        corpus_type = "eng" if self.current_corpus_tab == 0 else "kor"
        search_history_manager.set_corpus_type(corpus_type)
        
        # 检查是否有历史记录
        history = search_history_manager.get_recent_records(100)
        if not history:
            corpus_name = "英语" if corpus_type == "eng" else "韩语"
            QMessageBox.information(self, "📜 搜索历史", f"{corpus_name}语料库暂无搜索历史")
            return
        
        # 如果历史窗口已存在且未关闭，则直接显示
        if self.history_window is not None and not self.history_window.isHidden():
            self.history_window.raise_()
            self.history_window.activateWindow()
            return
        
        # 创建并显示历史窗口
        self.history_window = SearchHistoryWindow(corpus_type, self)
        
        # 连接双击事件
        self.history_window.history_table.cellDoubleClicked.connect(
            lambda row, col: self._load_history_keyword(row)
        )
        
        self.history_window.show()
    
    def _load_history_keyword(self, row: int):
        """
        从历史记录加载关键词到搜索框
        
        Args:
            row: 表格行号
        """
        keyword = self.history_window.load_to_search(row)
        if keyword:
            # 加载关键词到当前标签页的输入框
            if self.current_corpus_tab == 0:  # 英语语料库
                self.english_keyword_edit.setText(keyword)
            else:  # 韩语语料库
                self.korean_keyword_edit.setText(keyword)
            
            self.history_window = None
            self.status_bar.showMessage(f"✓ 已加载关键词: {keyword}")
    
    def show_context_menu(self, pos):
        """显示右键菜单"""
        item = self.result_table.itemAt(pos)
        if not item:
            return
        
        row = item.row()
        col = item.column()
        
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 3px;
                color: #ffffff;
            }
            QMenu::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background-color: #404040;
                margin: 5px 10px;
            }
        """)
        
        copy_cell_action = menu.addAction("📋 复制单元格")
        menu.addSeparator()
        copy_action = menu.addAction("📋 复制选中行")
        open_action = menu.addAction("📂 打开文件")
        export_action = menu.addAction("📤 导出选中行")
        
        action = menu.exec(self.result_table.mapToGlobal(pos))
        
        if action == copy_cell_action:
            self.copy_selected_cell(row, col)
        elif action == copy_action:
            self.copy_selected_row(row)
        elif action == open_action:
            self.open_file(row)
        elif action == export_action:
            self.export_selected_row(row)
    
    def show_header_context_menu(self, pos):
        """显示表头右键菜单"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 3px;
                color: #ffffff;
            }
            QMenu::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background-color: #404040;
                margin: 5px 10px;
            }
        """)
        
        # 添加显示/隐藏列的子菜单
        columns_menu = menu.addMenu("📊 显示列")
        columns_menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 3px;
                color: #ffffff;
            }
            QMenu::item:selected {
                background-color: #0078d4;
                color: white;
            }
        """)
        
        # 列名称列表
        column_names = ['文件名', '行号', '集数', '时间轴', '对应台词']
        
        # 为每列创建复选框动作
        for col in range(self.result_table.columnCount()):
            action = columns_menu.addAction(column_names[col])
            action.setCheckable(True)
            action.setChecked(not self.result_table.isColumnHidden(col))
            action.triggered.connect(lambda checked, c=col: self.toggle_column_visibility(c, checked))
        
        menu.addSeparator()
        reset_action = menu.addAction("🔄 重置列宽")
        
        action = menu.exec(self.result_table.horizontalHeader().mapToGlobal(pos))
        
        if action == reset_action:
            self.reset_column_widths()
    
    def toggle_column_visibility(self, col_index, checked):
        """切换列的显示/隐藏状态"""
        self.result_table.setColumnHidden(col_index, not checked)
        
        # 更新状态栏提示
        column_names = ['文件名', '行号', '集数', '时间轴', '对应台词']
        status = "显示" if checked else "隐藏"
        self.status_bar.showMessage(f"📊 已{status}列: {column_names[col_index]}")
    
    def copy_selected_cell(self, row, col):
        """复制选中单元格（纯文本，不含HTML标签）"""
        item = self.result_table.item(row, col)
        if item:
            # 获取文本并去除HTML标签
            raw_text = item.text()
            clean_text = self._remove_html_tags(raw_text)
            QApplication.clipboard().setText(clean_text)
            self.status_bar.showMessage("📋 已复制单元格内容")
    
    def copy_selected_row(self, row):
        """复制选中行（纯文本，不含HTML标签）"""
        text = ""
        for col in range(self.result_table.columnCount()):
            item = self.result_table.item(row, col)
            if item:
                # 获取文本并去除HTML标签
                raw_text = item.text()
                clean_text = self._remove_html_tags(raw_text)
                text += clean_text + "\t"
        
        QApplication.clipboard().setText(text.strip())
        self.status_bar.showMessage("📋 已复制到剪贴板")
    
    def _remove_html_tags(self, text: str) -> str:
        """
        去除HTML标签，只保留纯文本
        
        Args:
            text: 包含HTML标签的文本
            
        Returns:
            纯文本
        """
        import re
        # 去除所有HTML标签
        clean_text = re.sub(r'<[^>]+>', '', text)
        # 去除多余的空白字符
        clean_text = ' '.join(clean_text.split())
        return clean_text
    
    def open_file(self, row):
        """打开文件"""
        if row < 0 or row >= len(self.result_file_paths):
            return
        
        filepath = self.result_file_paths[row]
        if os.path.exists(filepath):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(filepath)
                elif os.name == 'posix':  # macOS和Linux
                    os.system(f'open "{filepath}"')
                self.status_bar.showMessage(f"📂 已打开文件: {os.path.basename(filepath)}")
            except Exception as e:
                QMessageBox.critical(self, "❌ 错误", f"打开文件失败: {str(e)}")
        else:
            QMessageBox.warning(self, "❌ 错误", f"文件不存在: {filepath}")
    
    def export_selected_row(self, row):
        """导出选中行"""
        text = ""
        for col in range(self.result_table.columnCount()):
            item = self.result_table.item(row, col)
            if item:
                text += item.text() + "\t"
        
        # 保存文件
        output_dir = self.english_input_path_edit.text().strip() if self.current_corpus_tab == 0 else self.korean_input_path_edit.text().strip()
        if not output_dir or not os.path.exists(output_dir):
            output_dir = os.getcwd()
        
        output_file = os.path.join(output_dir, "selected_result.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text.strip())
        
        QMessageBox.information(self, "✅ 成功", f"结果已导出到 {output_file}")
    
    def reset_column_widths(self):
        """重置列宽"""
        self.result_table.setColumnWidth(0, 200)
        self.result_table.setColumnWidth(1, 80)
        self.result_table.setColumnWidth(2, 150)
        self.result_table.setColumnWidth(3, 120)
    
    def restore_column_settings(self):
        """恢复列宽和顺序"""
        # TODO: 从配置文件恢复列宽和顺序
        pass
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 保存当前标签页的配置
        self.save_current_tab_config()
        
        # 保存窗口设置
        config_manager.set_ui_settings(
            width=self.width(),
            height=self.height(),
            x=self.x(),
            y=self.y()
        )
        
        # 保存当前标签页索引
        config_manager.set_current_tab(self.current_corpus_tab)
        
        config_manager.save_config()
        
        event.accept()
    
    def dragEnterEvent(self, event):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """拖拽放下事件"""
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            # 获取当前标签页的输入框
            if self.current_corpus_tab == 0:  # 英语语料库
                self.english_input_path_edit.setText(files[0])
            else:  # 韩语语料库
                self.korean_input_path_edit.setText(files[0])
            self.status_bar.showMessage(f"✓ 已选择: {files[0]}")