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
    QStyleOptionViewItem, QTabWidget, QComboBox, QSizePolicy
)
from PySide6.QtCore import Qt, QThread, Signal, QPoint, QSettings, QSize, QTimer
from PySide6.QtGui import QColor, QFont, QAction, QIcon, QCursor, QDragEnterEvent, QDropEvent, QTextDocument

# 导入生成的UI类
from .ui_CorpusSearchTool import Ui_CorpusSearchTool

# 主题模块导入
from .theme import apply_theme, refresh_all_widget_styles

# 搜索结果表格模块导入
from .search_result_table_gui import SearchResultTableManager, HTMLDelegate

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
    search_completed = Signal(list, str, list, str, list, list)  # results, lemma, actual_variant_set, pos_full, target_variant_set, matched_terms_set
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
        self.lemma = ""  # 系统判定的词典形
        self.actual_variant_set = []  # 基于词典形实际命中的所有变体形式列表
        self.matched_terms_set = []  # 所有实际匹配到的词（包括词干和变体）
        self._stop_flag = False  # 停止标志
    
    def stop(self):
        """停止搜索"""
        self._stop_flag = True
    
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
                self.search_completed.emit([], "", [], "", [], [])
                return
            
            # 韩语模式特殊处理
            if self.corpus_type == "korean":
                # 韩语模式：韩语没有大小写之分，使用 case_sensitive=True
                # 但为了兼容性，我们保留用户的选择，只是不使用模糊匹配
                self.fuzzy_match = False
                all_results = []  # 初始化 results 变量
                all_search_records = []  # 保存所有搜索记录
                
                # 检查是否包含韩语
                import re
                korean_pattern = re.compile(r'[\uac00-\ud7af]')
                contains_korean = bool(korean_pattern.search(self.keywords))
                
                # 使用新的高级韩语搜索方法
                
                # 保存生成的变体列表
                self.target_variant_set = []
                
                for i, file_path in enumerate(files_to_search):
                    # 检查是否需要停止
                    if self._stop_flag:
                        return
                    
                    try:
                        # 使用新的 search_korean_advanced 方法
                        search_record = search_engine_kor.search_korean_advanced(
                            file_path,
                            self.keywords,
                            case_sensitive=True
                        )
                        
                        # 提取搜索结果
                        file_results = search_record['search_results']
                        if file_results:
                            all_results.extend(file_results)
                        
                        # 保存搜索记录
                        all_search_records.append(search_record)
                        
                        # 获取生成的变体列表（使用第一个搜索记录的变体列表）
                        if not self.target_variant_set and 'target_variant_set' in search_record:
                            self.target_variant_set = search_record['target_variant_set']

                        # 收集所有实际匹配到的词
                        if 'matched_terms_set' in search_record:
                            if not hasattr(self, 'matched_terms_set_all'):
                                self.matched_terms_set_all = set()
                            self.matched_terms_set_all.update(search_record['matched_terms_set'])

                        # 更新进度
                        progress = int((i + 1) / total_files * 100)
                        self.progress_updated.emit(progress)
                    except Exception as e:
                        print(f"[ERROR] 处理文件 {file_path} 时出错: {str(e)}")
                        import traceback
                        traceback.print_exc()
                        continue
                
                # 提取词典形和实际变体形式列表
                pos_full = ""
                if all_search_records:
                    # 使用第一个搜索记录的词典形
                    self.lemma = all_search_records[0]['lemma']

                    # 提取具体词典型
                    pos_full = all_search_records[0].get('pos', '')

                    # 合并所有搜索记录的实际变体形式，去重
                    all_variants = set()
                    for record in all_search_records:
                        all_variants.update(record['actual_variant_set'])
                    self.actual_variant_set = list(all_variants)

                    # 合并所有搜索记录的匹配词集合，去重
                    if hasattr(self, 'matched_terms_set_all'):
                        self.matched_terms_set = list(self.matched_terms_set_all)
                    else:
                        self.matched_terms_set = []
                
                # 保存完整的搜索记录
                import json
                import datetime
                
                # 创建搜索记录文件
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                record_filename = f"search_record_{timestamp}.json"
                
                # 保存到搜索历史
                if hasattr(self, 'current_search_params'):
                    # 这里可以扩展，将搜索记录保存到历史文件
                    pass
                
                # 使用 all_results 作为最终结果
                results = all_results
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
                        # 检查是否需要停止
                        if self._stop_flag:
                            return
                        
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
                        # 检查是否需要停止
                        if self._stop_flag:
                            return
                        
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
            
            # 发送搜索完成信号，包含lemma、actual_variant_set、pos_full、生成的变体列表和matched_terms_set
            self.search_completed.emit(formatted_results, self.lemma, self.actual_variant_set, pos_full, self.target_variant_set if hasattr(self, 'target_variant_set') else [], self.matched_terms_set if hasattr(self, 'matched_terms_set') else [])
            
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





class CorpusSearchToolGUI(QMainWindow, Ui_CorpusSearchTool):
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
        
        # 使用生成的UI类创建界面
        self.setupUi(self)
        
        # 重置进度条初始值，覆盖UI文件中的默认设置
        self.ProgressBar.setValue(0)
        self.ProgressBar.setVisible(False)
        
        # 初始化搜索结果表格管理器
        self.table_manager = SearchResultTableManager(self.result_table)
        self.table_manager.initialize_table()
        
        # 获取HTML代理
        self.html_delegate = self.table_manager.html_delegate
        
        # 移除旧的列宽限制信号连接，改用表格管理器的实现
        # self.result_table.horizontalHeader().sectionResized.connect(self.enforce_min_column_width)
        
        # 连接列宽变化信号，重新计算行高
        self.result_table.horizontalHeader().sectionResized.connect(self.on_column_resized)
        
        # 连接列顺序变化信号，保存列顺序
        self.result_table.horizontalHeader().sectionMoved.connect(self.on_section_moved)
        
        # 连接表头右键菜单信号
        header = self.result_table.horizontalHeader()
        header.customContextMenuRequested.connect(self.show_header_context_menu)
        
        # 为表格设置右键菜单
        self.result_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.result_table.customContextMenuRequested.connect(self.show_context_menu)
        
        # 连接标签页切换信号
        self.corpus_tab_widget.currentChanged.connect(self.on_corpus_tab_changed)
        
        # 连接更新目录按钮点击事件
        self.ReadPathSet.clicked.connect(self.update_input_directory)
        # 连接浏览按钮点击事件
        self.ReadPathSelect.clicked.connect(self.browse_input_path)
        # 连接打开目录按钮点击事件
        self.ReadPathOpen.clicked.connect(self.open_input_directory)
        # 连接路径输入框的回车事件
        self.ReadPathInput.returnPressed.connect(self.update_input_directory)
        
        # 连接搜索按钮点击事件
        self.search_btn.clicked.connect(self.start_search)
        
        # 连接搜索历史按钮点击事件
        self.history_btn.clicked.connect(self.show_search_history)
        
        # 连接生成变体表按钮点击事件
        self.lemmalist_btn.clicked.connect(self.generate_lemmalist)
        
        # 连接停止搜索按钮点击事件
        self.stop_search_btn.clicked.connect(self.stop_search)
        
        # 初始化变量
        self.current_corpus_tab = self.corpus_tab_widget.currentIndex()
        
        # 根据当前标签页类型设置ReadPathInput初始值
        corpus_type = "english" if self.current_corpus_tab == 0 else "korean"
        corpus_config = config_manager.get_corpus_config(corpus_type)
        self.ReadPathInput.setText(corpus_config['input_dir'])
        
        # 恢复列宽和顺序设置
        self.restore_column_settings()
        
        # 设置样式主题
        self.setup_styles()

        # 重新设置表头高度为30px，确保样式设置后仍然保持
        header = self.result_table.horizontalHeader()
        header.setFixedHeight(30)
        header.style().unpolish(header)
        header.style().polish(header)
        header.update()

        # 初始设置可调整列的最小宽度为80，跳过固定宽度的列
        for i in range(self.result_table.columnCount()):
            if i not in [1, 3]:  # 跳过时间轴列和行号列（固定宽度）
                if self.result_table.columnWidth(i) < 80:
                    self.result_table.setColumnWidth(i, 80)
        
        # 连接主题菜单项的信号
        self.actionlight.triggered.connect(lambda: self.change_theme("Light"))
        self.actionDark.triggered.connect(lambda: self.change_theme("Dark"))
        
        # 连接加载历史记录菜单项的信号
        self.actionLoad.triggered.connect(self.load_search_results_from_html)
        
        # 重新设置图标路径，确保图标正确加载
        self.set_icon_paths()

        # 为变体列表显示控件启用文字换行
        if hasattr(self, 'english_lemmalist_display'):
            self.english_lemmalist_display.setWordWrap(True)
        if hasattr(self, 'korean_lemmalist_display'):
            self.korean_lemmalist_display.setWordWrap(True)

        # 标记初始化完成
        self._initialized = True
    
    def format_lemma_display(self, pos_full, lemma):
        """
        格式化词典形显示文本（共享方法）
        
        Args:
            pos_full: 完整的词性描述
            lemma: 词典形
            
        Returns:
            格式化后的文本：[词性]：词典形
        """
        return f"[{pos_full}]：{lemma}"
    
    def generate_lemmalist(self):
        """
        生成变体表
        """
        try:
            # 获取当前标签页和关键词
            if self.current_corpus_tab == 0:  # 英语语料库
                keywords = self.english_keyword_edit.text().strip()
                if not keywords:
                    QMessageBox.warning(self, "错误", "请输入关键词")
                    return
                
                # 生成英语变体表（简化版）
                # 这里可以扩展，实现更复杂的英语变体表生成逻辑
                lemmalist_text = f"关键词: {keywords}\n\n变体表生成功能正在开发中..."
                
                # 更新显示
                self.english_lemmalist_display.setText(lemmalist_text)
            else:  # 韩语语料库
                keywords = self.korean_keyword_edit.text().strip()
                if not keywords:
                    QMessageBox.warning(self, "错误", "请输入关键词")
                    return
                
                # 使用韩语搜索引擎生成变体表
                from function.search_engine_kor import search_engine_kor
                
                # 1. 使用kiwipiepy分析原始关键词
                analyzed_words = search_engine_kor.kiwi.analyze(keywords)
                
                # 提取第一个分析结果的主要词（假设只有一个关键词）
                main_word = None
                for token in analyzed_words[0][0]:
                    if token.form.strip() == keywords.strip():
                        main_word = token
                        break
                
                if not main_word:
                    # 如果直接匹配失败，尝试取第一个非标点的词
                    for token in analyzed_words[0][0]:
                        if token.tag not in ['SF', 'SP', 'SS', 'SE', 'SO', 'SW']:
                            main_word = token
                            break
                
                # 后处理：修正kiwipiepy的常见分析错误
                should_fix = False
                if main_word and keywords.endswith('다') and main_word.tag == 'MAG':
                    tokens = analyzed_words[0][0]
                    if len(tokens) >= 2:
                        if tokens[-1].form == '다':
                            combined_lemma = ''.join([t.form for t in tokens])
                            pos = 'VV'
                            lemma = combined_lemma
                            should_fix = True
                
                if not main_word:
                    lemma = keywords
                    pos = 'Noun'
                else:
                    if not should_fix:
                        lemma = main_word.lemma
                        pos = main_word.tag
                
                # 词性标签映射
                pos_map = {
                    'VV': '规则动词 (Regular Verb)',
                    'VV-I': '不规则动词 (Irregular Verb)',
                    'VA': '规则形容词 (Regular Adjective)',
                    'VA-I': '不规则形容词 (Irregular Adjective)',
                    'VX': '辅助用言 (Auxiliary Verb)',
                    'VCP': '肯定体词谓词 (Positive Copula)',
                    'VCN': '否定体词谓词 (Negative Copula)',
                    'XSV': '动词性派生词 (Verb Derivative)',
                    'XSA': '形容词性派生词 (Adjective Derivative)',
                    'NNG': '一般名词 (Common Noun)',
                    'NNP': '专有名词 (Proper Noun)',
                    'NNB': '依存名词 (Dependent Noun)',
                    'NR': '数词 (Numeral)',
                    'NP': '代名词 (Pronoun)',
                    'MAG': '一般副词 (General Adverb)',
                    'MAJ': '接续副词 (Conjunctive Adverb)',
                }
                pos_full = pos_map.get(pos, pos)
                
                # 2. 更新词典形显示框（使用共享的格式化方法）
                self.korean_lemma_display.setText(self.format_lemma_display(pos_full, lemma))
                
                # 3. 判定词性并生成变体
                verb_adj_tags = ['VV', 'VV-I', 'VA', 'VA-I', 'VX', 'VCP', 'VCN', 'XSV', 'XSA']
                is_verb_adj = pos in verb_adj_tags
                
                noun_adv_tags = ['NNG', 'NNP', 'NNB', 'NR', 'NP', 'MAG', 'MAJ']
                is_noun_adv = pos in noun_adv_tags
                
                if is_noun_adv:
                    variant_set = [keywords]
                else:
                    variant_set = search_engine_kor._generate_korean_variants(lemma)
                    if lemma not in variant_set:
                        variant_set.append(lemma)
                    if keywords not in variant_set:
                        variant_set.append(keywords)
                
                # 4. 更新变体列表显示框（用逗号分隔，与搜索功能一致）
                variant_text = ", ".join(variant_set)
                self.korean_lemmalist_display.setText(variant_text)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成变体表失败: {str(e)}")
    
    def stop_search(self):
        """
        停止当前搜索
        """
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.stop()
            QMessageBox.information(self, "提示", "搜索已停止")
        else:
            QMessageBox.information(self, "提示", "当前没有正在运行的搜索")
    
    def set_icon_paths(self):
        """
        重新设置图标路径，确保图标正确加载
        """
        import os
        # 获取图标目录的绝对路径
        icon_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons")
        
        # 重新设置图标
        # ReadPathSet 按钮使用 refresh 图标
        self.ReadPathSet.setIcon(QIcon(os.path.join(icon_dir, "refresh.png")))
        
        # ReadPathSelect 按钮使用 search2 图标
        self.ReadPathSelect.setIcon(QIcon(os.path.join(icon_dir, "search2.png")))
        
        # ReadPathOpen 按钮使用 open-folder2 图标
        self.ReadPathOpen.setIcon(QIcon(os.path.join(icon_dir, "open-folder2.png")))
        
        # history_btn 按钮使用 history 图标
        self.history_btn.setIcon(QIcon(os.path.join(icon_dir, "history.png")))
        
        # search_btn 按钮使用 search 图标
        self.search_btn.setIcon(QIcon(os.path.join(icon_dir, "search.png")))
        
        # lemmalist_btn 按钮使用 start-up 图标
        self.lemmalist_btn.setIcon(QIcon(os.path.join(icon_dir, "start-up.png")))
        
        # stop_search_btn 按钮使用 stop 图标
        self.stop_search_btn.setIcon(QIcon(os.path.join(icon_dir, "stop.png")))
    
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

        # 设置窗口大小为固定值，不再从配置加载
        self.resize(1200, 800)

        # 居中显示窗口
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
        # 从配置文件加载主题设置，如果没有则使用默认值"Light"
        theme = config_manager.get_theme()
        # 应用主题
        self.change_theme(theme)
        
        # 设置字体
        self._setup_fonts()
    
    def _setup_fonts(self):
        """设置字体"""
        from gui.font import FontConfig
        
        # 为韩语变体列表显示设置韩语字体
        if hasattr(self, 'korean_lemmalist_display'):
            self.korean_lemmalist_display.setFont(FontConfig.get_korean_font())
        
    def change_theme(self, mode):
        """
        处理主题切换事件
        
        Args:
            mode: 主题模式，可选值: "Light" 或 "Dark"
        """
        apply_theme(mode)
        # 刷新所有控件样式，确保主题选择器生效
        refresh_all_widget_styles()
        # 更新UI元素的主题属性
        self.update_theme_properties(mode)
        # 保存主题设置到配置文件
        config_manager.set_theme(mode)
        config_manager.save_config()
    
    def update_theme_properties(self, mode):
        """
        更新UI元素的主题属性，确保[theme="light"]和[theme="dark"]选择器生效
        
        Args:
            mode: 主题模式，可选值: "Light" 或 "Dark"
        """
        from .theme import update_widget_theme_properties
        
        # 获取主题模式字符串
        theme_mode = "light" if mode == "Light" else "dark"
        
        # 设置主题属性到主窗口
        self.setProperty("theme", theme_mode)
        
        # 特别为menuBar设置theme属性
        if hasattr(self, 'menuBar'):
            self.menuBar.setProperty("theme", theme_mode)
            # 强制刷新menuBar的样式
            self.menuBar.style().unpolish(self.menuBar)
            self.menuBar.style().polish(self.menuBar)
            self.menuBar.update()
        
        # 特别为corpus_tab_widget设置theme属性
        self.corpus_tab_widget.setProperty("theme", theme_mode)
        
        # 特别处理corpus_tab_widget的tabBar
        tab_bar = self.corpus_tab_widget.tabBar()
        if tab_bar:
            tab_bar.setProperty("theme", theme_mode)
        
        # 注释掉：不重新设置表格主题，保持表格背景颜色不变
        # self.table_manager.set_table_theme(theme_mode)
        
        # 特别处理四个显示控件
        display_widgets = [
            self.korean_lemma_display,
            self.english_lemma_display,
            self.english_lemmalist_display,
            self.korean_lemmalist_display
        ]
        for widget in display_widgets:
            if widget:
                widget.setProperty("theme", theme_mode)
                # 为变体列表显示控件启用文字换行
                if widget in [self.english_lemmalist_display, self.korean_lemmalist_display]:
                    widget.setWordWrap(True)
                # 强制刷新显示控件样式
                widget.style().unpolish(widget)
                widget.style().polish(widget)
                widget.update()
        
        # 使用theme.py中定义的update_widget_theme_properties函数更新主题属性
        update_widget_theme_properties(self, theme_mode)
        
        # 强制刷新corpus_tab_widget的样式
        self.corpus_tab_widget.style().unpolish(self.corpus_tab_widget)
        self.corpus_tab_widget.style().polish(self.corpus_tab_widget)
        self.corpus_tab_widget.update()
        
        # 强制刷新result_table的样式
        self.result_table.style().unpolish(self.result_table)
        self.result_table.style().polish(self.result_table)
        self.result_table.update()
        
        # 处理事件，确保所有更新都生效
        QApplication.processEvents()
    
    def create_widgets(self):
        """创建界面元素（已被setupUi方法取代）"""
        pass
    
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
        keyword_layout.setSpacing(5)  # 减小控件之间的间距，让词典型标签和显示框更近
        
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
            keyword_edit.setMaximumWidth(200)  # 缩小关键词输入框宽度
            
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
            keyword_edit.setMaximumWidth(200)  # 缩小关键词输入框宽度
            
            # 保存到实例变量
            self.korean_keyword_combo = keyword_combo
            self.korean_keyword_edit = keyword_edit
        
        # 添加词典型显示区域
        lemma_label = QLabel("词典型:")
        lemma_label.setMinimumWidth(60)
        
        lemma_display = QLabel("N/A")
        # 使用与开始搜索按钮相同的高度（32px）
        lemma_display.setStyleSheet("background-color: rgba(50, 50, 50, 0.5); border: 1px solid rgba(100, 100, 100, 0.5); border-radius: 5px; padding: 8px 10px; height: 32px; font-size: 9pt; line-height: 32px;")
        lemma_display.setMinimumWidth(150)
        lemma_display.setMaximumWidth(200)
        lemma_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lemma_display.setWordWrap(False)
        
        # 保存到实例变量
        if corpus_type == "english":
            self.english_lemma_display = lemma_display
        else:
            self.korean_lemma_display = lemma_display
        
        keyword_layout.addWidget(keyword_label)
        keyword_layout.addWidget(keyword_combo)
        keyword_layout.addWidget(keyword_edit)
        keyword_layout.addWidget(lemma_label)
        keyword_layout.addWidget(lemma_display)
        
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
        history_btn = QPushButton("搜索历史")
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
        
        # 更新搜索历史管理器的语料库类型
        corpus_type = "eng" if index == 0 else "kor"
        search_history_manager.set_corpus_type(corpus_type)
        
        # 根据新标签页类型更新ReadPathInput
        corpus_type_config = "english" if index == 0 else "korean"
        corpus_config = config_manager.get_corpus_config(corpus_type_config)
        self.ReadPathInput.setText(corpus_config['input_dir'])
    
    def save_current_tab_config(self):
        """保存当前标签页的配置"""
        if self.current_corpus_tab == 0:  # 英语语料库
            corpus_type = "english"
            input_path = self.ReadPathInput.text().strip()
            keyword_type = self.english_keyword_combo.currentText()  # 获取实际选项文本
            case_sensitive = self.english_case_sensitive_check.isChecked() if hasattr(self, 'english_case_sensitive_check') else False
            fuzzy_match = self.english_fuzzy_match_check.isChecked() if hasattr(self, 'english_fuzzy_match_check') else False
            regex_enabled = self.english_regex_check.isChecked() if hasattr(self, 'english_regex_check') else False
        else:  # 韩语语料库
            corpus_type = "korean"
            input_path = self.ReadPathInput.text().strip()
            keyword_type = self.korean_keyword_combo.currentText()  # 获取实际选项文本
            case_sensitive = False  # 韩语不区分大小写
            fuzzy_match = False  # 韩语不使用模糊匹配
            regex_enabled = False  # 韩语不支持正则表达式
        
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
        

        
        # 设置表格属性
        self.result_table.setAlternatingRowColors(True)
        self.result_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.result_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.result_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.result_table.setWordWrap(False)  # 禁用文字换行，避免影响右键菜单
        self.result_table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)  # 像素级横向滚动
        self.result_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # 确保表格可以接收焦点
        self.result_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # 需要时显示横向滚动条
        
        # 启用 HTML 格式渲染
        self.result_table.setItemDelegate(HTMLDelegate(self.result_table))
        
        # 设置列宽
        header = CustomHeaderView(Qt.Orientation.Horizontal, self.result_table)
        self.result_table.setHorizontalHeader(header)
        # 所有列都使用可调整模式
        for i in range(5):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)
        # 设置初始列宽
        self.result_table.setColumnWidth(0, 200)
        self.result_table.setColumnWidth(1, 80)
        self.result_table.setColumnWidth(2, 150)
        self.result_table.setColumnWidth(3, 120)
        self.result_table.setColumnWidth(4, 200)
        header.setFixedHeight(30)  # 设置表头固定高度为30px
        
        # 启用列拖拽和右键菜单
        header.setSectionsMovable(True)  # 允许列拖拽调整顺序
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self.show_header_context_menu)

        # 恢复列宽和顺序
        self.restore_column_settings()
        
        # 设置行高为自动调整
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.resizeRowsToContents()
        

        
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
        
        result_layout.addWidget(self.result_table)
        
        parent_layout.addWidget(result_group)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("✓ 准备就绪")
        self.setStatusBar(self.status_bar)
    

    
    def update_input_directory(self):
        """
        更新目录：将当前路径输入框里的目录更新为输入路径，等同于回车操作
        即将当前路径输入框的路径保存到当前标签页的配置中
        """
        # 获取当前路径输入框里的目录
        input_path = self.ReadPathInput.text().strip()
        
        if input_path and os.path.exists(input_path):
            # 保存当前标签页的配置，包括输入路径
            self.save_current_tab_config()
            # 同时更新标签页内独立的输入路径编辑框
            if self.current_corpus_tab == 0 and hasattr(self, 'english_input_path_edit'):
                self.english_input_path_edit.setText(input_path)
            elif self.current_corpus_tab == 1 and hasattr(self, 'korean_input_path_edit'):
                self.korean_input_path_edit.setText(input_path)
            
            # 更新配置管理器中的输入路径
            config_manager.set_input_dir(input_path)
            
            # 成功：绿色边框闪烁1次
            self.flash_border(success=True, flash_count=1)
        else:
            # 失败：红色边框闪烁2次
            self.flash_border(success=False, flash_count=2)
            
            # 如果输入路径无效，显示提示信息
            QMessageBox.information(
                self,
                "提示",
                "请先输入有效的目录路径",
                QMessageBox.StandardButton.Ok
            )
    
    def browse_input_path(self):
        """浏览输入路径"""
        # 获取当前输入框路径作为默认路径
        current_path = self.ReadPathInput.text().strip()
        
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
            # 设置统一的输入框
            self.ReadPathInput.setText(dir_path)
    
    def flash_border(self, success=True, flash_count=1):
        """
        为路径输入框添加边框闪烁效果
        
        Args:
            success: 是否成功，True为绿色，False为红色
            flash_count: 闪烁次数
        """
        # 获取原始样式
        original_style = self.ReadPathInput.styleSheet()
        
        # 设置闪烁颜色和次数
        color = "#2ecc71" if success else "#e74c3c"  # 绿色或红色
        current_flash = 0
        
        # 创建闪烁定时器
        flash_timer = QTimer(self)
        flash_timer.setInterval(200)  # 闪烁间隔200毫秒
        
        def toggle_border():
            nonlocal current_flash
            
            if current_flash < flash_count * 2:
                # 切换边框样式
                if current_flash % 2 == 0:
                    # 显示彩色边框
                    new_style = f"{original_style}" if original_style else ""
                    if "border:" in new_style:
                        # 如果已有边框样式，替换颜色
                        import re
                        new_style = re.sub(r"border:\s*(\d+px\s+)?solid\s+#[0-9a-fA-F]+;", f"border: 2px solid {color};", new_style)
                    else:
                        # 否则添加边框样式
                        new_style += f"border: 2px solid {color};"
                else:
                    # 恢复原始样式
                    new_style = original_style
                
                self.ReadPathInput.setStyleSheet(new_style)
                current_flash += 1
            else:
                # 闪烁结束，恢复原始样式
                self.ReadPathInput.setStyleSheet(original_style)
                flash_timer.stop()
                flash_timer.deleteLater()
        
        # 连接定时器信号
        flash_timer.timeout.connect(toggle_border)
        # 启动定时器
        flash_timer.start()
    
    def open_input_directory(self):
        """
        打开路径输入框中指定的目录
        """
        # 获取路径输入框中的目录路径
        dir_path = self.ReadPathInput.text().strip()
        
        # 检查目录是否存在
        if not dir_path or not os.path.exists(dir_path):
            # 如果目录不存在，显示错误信息
            QMessageBox.warning(
                self,
                "错误",
                f"目录不存在：{dir_path}",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # 使用系统命令打开目录
        if sys.platform == "win32":
            # Windows 系统
            os.startfile(dir_path)
        elif sys.platform == "darwin":
            # macOS 系统
            os.system(f"open '{dir_path}'")
        else:
            # Linux 系统
            os.system(f"xdg-open '{dir_path}'")
    
    def start_search(self):
        """开始搜索"""
        # 获取当前标签页的控件值
        input_path = self.ReadPathInput.text().strip()
        
        if self.current_corpus_tab == 0:  # 英语语料库
            keywords = self.english_keyword_edit.text().strip()
            case_sensitive = self.english_case_sensitive_check.isChecked() if hasattr(self, 'english_case_sensitive_check') else False
            fuzzy_match = self.english_fuzzy_match_check.isChecked() if hasattr(self, 'english_fuzzy_match_check') else False
            regex_enabled = self.english_regex_check.isChecked() if hasattr(self, 'english_regex_check') else False
        else:  # 韩语语料库
            keywords = self.korean_keyword_edit.text().strip()
            case_sensitive = False  # 韩语不区分大小写
            fuzzy_match = False  # 韩语不使用模糊匹配
            regex_enabled = False  # 韩语不支持正则表达式
        
        if not input_path:
            QMessageBox.warning(self, "错误", "请输入输入路径")
            return
        
        if not os.path.exists(input_path):
            QMessageBox.warning(self, "错误", f"输入路径不存在: {input_path}")
            return
        
        if not os.path.isfile(input_path) and not os.path.isdir(input_path):
            QMessageBox.warning(self, "错误", f"输入路径无效: {input_path}")
            return
        
        if not keywords:
            QMessageBox.warning(self, "错误", "请输入关键词")
            return
        
        # 获取语料库类型
        if self.current_corpus_tab == 0:  # 英语语料库
            corpus_type = "english"
        else:  # 韩语语料库
            corpus_type = "korean"
        
        # 检查是否是引号内的完全匹配
        exact_match = False
        if keywords.startswith('"') and keywords.endswith('"'):
            exact_match = True
            keywords = keywords[1:-1]  # 去掉引号

        
        # 保存搜索参数到实例变量，用于保存历史记录
        self.current_search_params = {
            'keywords': keywords,
            'input_path': input_path,
            'case_sensitive': case_sensitive,
            'fuzzy_match': fuzzy_match,
            'regex_enabled': regex_enabled,
            'exact_match': exact_match,
            'corpus_type': corpus_type
        }
        
        # 更新配置
        config_manager.set_input_dir(input_path)
        config_manager.set_search_settings(
            case_sensitive=case_sensitive,
            fuzzy_match=fuzzy_match,
            regex_enabled=regex_enabled
        )
        
        # 获取关键词类型
        if self.current_corpus_tab == 0:  # 英语语料库
            keyword_type = self.english_keyword_combo.currentText()
        else:  # 韩语语料库
            keyword_type = self.korean_keyword_combo.currentText()
        
        # 保存关键词类型到参数中
        self.current_search_params['keyword_type'] = keyword_type
        
        # 分析关键词词典型并显示
        # 对于韩语，先调用 generate_lemmalist 生成变体列表
        if self.current_corpus_tab == 0:  # 英语语料库
            # 英语词典型显示（简化版）
            lemma_text = "N/A"  # 英语暂不实现词典型分析
            self.english_lemma_display.setText(lemma_text)
        else:  # 韩语语料库
            # 调用 generate_lemmalist 方法生成词典形和变体列表
            from function.search_engine_kor import search_engine_kor
            try:
                # 1. 使用kiwipiepy分析原始关键词
                analyzed_words = search_engine_kor.kiwi.analyze(keywords)
                
                # 提取第一个分析结果的主要词
                main_word = None
                for token in analyzed_words[0][0]:
                    if token.form.strip() == keywords.strip():
                        main_word = token
                        break
                
                if not main_word:
                    for token in analyzed_words[0][0]:
                        if token.tag not in ['SF', 'SP', 'SS', 'SE', 'SO', 'SW']:
                            main_word = token
                            break
                
                # 后处理：修正kiwipiepy的常见分析错误
                should_fix = False
                if main_word and keywords.endswith('다') and main_word.tag == 'MAG':
                    tokens = analyzed_words[0][0]
                    if len(tokens) >= 2:
                        if tokens[-1].form == '다':
                            combined_lemma = ''.join([t.form for t in tokens])
                            pos = 'VV'
                            lemma = combined_lemma
                            should_fix = True
                
                if not main_word:
                    lemma = keywords
                    pos = 'Noun'
                else:
                    if not should_fix:
                        lemma = main_word.lemma
                        pos = main_word.tag
                
                # 词性标签映射
                pos_map = {
                    'VV': '规则动词 (Regular Verb)',
                    'VV-I': '不规则动词 (Irregular Verb)',
                    'VA': '规则形容词 (Regular Adjective)',
                    'VA-I': '不规则形容词 (Irregular Adjective)',
                    'VX': '辅助用言 (Auxiliary Verb)',
                    'VCP': '肯定体词谓词 (Positive Copula)',
                    'VCN': '否定体词谓词 (Negative Copula)',
                    'XSV': '动词性派生词 (Verb Derivative)',
                    'XSA': '形容词性派生词 (Adjective Derivative)',
                    'NNG': '一般名词 (Common Noun)',
                    'NNP': '专有名词 (Proper Noun)',
                    'NNB': '依存名词 (Dependent Noun)',
                    'NR': '数词 (Numeral)',
                    'NP': '代名词 (Pronoun)',
                    'MAG': '一般副词 (General Adverb)',
                    'MAJ': '接续副词 (Conjunctive Adverb)',
                }
                pos_full = pos_map.get(pos, pos)
                
                # 2. 更新词典形显示框
                self.korean_lemma_display.setText(self.format_lemma_display(pos_full, lemma))
                
                # 3. 判定词性并生成变体
                verb_adj_tags = ['VV', 'VV-I', 'VA', 'VA-I', 'VX', 'VCP', 'VCN', 'XSV', 'XSA']
                is_verb_adj = pos in verb_adj_tags
                
                noun_adv_tags = ['NNG', 'NNP', 'NNB', 'NR', 'NP', 'MAG', 'MAJ']
                is_noun_adv = pos in noun_adv_tags
                
                if is_noun_adv:
                    variant_set = [keywords]
                else:
                    variant_set = search_engine_kor._generate_korean_variants(lemma)
                    if lemma not in variant_set:
                        variant_set.append(lemma)
                    if keywords not in variant_set:
                        variant_set.append(keywords)
                
                # 4. 更新变体列表显示框
                variant_text = ", ".join(variant_set)
                self.korean_lemmalist_display.setText(variant_text)
                
                # 5. 保存变体列表到实例变量，供搜索使用
                self.korean_variant_set = variant_set
            except Exception as e:
                print(f"分析韩语关键词出错: {e}")
                self.korean_lemma_display.setText("分析错误")
                self.korean_variant_set = [keywords]  # 出错时使用原始关键词
        
        # 禁用搜索按钮
        self.search_btn.setEnabled(False)
        self.status_bar.showMessage("⏳ 正在搜索...")
        
        # 显示进度条
        self.ProgressBar.setVisible(True)
        self.ProgressBar.setValue(0)
        
        # 创建并启动搜索线程
        # 使用原始关键词进行搜索
        # 对于韩语，搜索线程内部的 search_korean_advanced 方法会自动生成变体列表
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
        self.ProgressBar.setValue(value)
        self.status_bar.showMessage(f"⏳ 正在搜索... {value}%")
    
    def search_completed(self, results, lemma="", actual_variant_set=[], pos_full="", target_variant_set=[], matched_terms_set=[]):
        """搜索完成"""
        # 隐藏进度条
        self.ProgressBar.setVisible(False)
        
        # 启用搜索按钮
        self.search_btn.setEnabled(True)
        
        # 清空表格
        self.result_table.setRowCount(0)
        self.result_file_paths = []
        
        if not results:
            self.status_bar.showMessage("✓ 搜索完成，未找到结果")
            QMessageBox.information(self, "✓ 搜索完成", "未找到匹配结果")
            return
        
        # 将搜索参数和变体传递给HTML代理
        # 合并 target_variant_set 和 matched_terms_set，确保所有匹配的词都能高亮
        highlight_set = set(target_variant_set)
        if matched_terms_set:
            highlight_set.update(matched_terms_set)

        if hasattr(self, 'html_delegate') and hasattr(self, 'current_search_params'):
            self.html_delegate.set_search_params(self.current_search_params, list(highlight_set))
        
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
            
            # 集数
            episode_item = QTableWidgetItem(str(episode))
            episode_item.setForeground(QColor('#FFC209'))
            # 设置为不可编辑
            episode_item.setFlags(episode_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.result_table.setItem(row, 0, episode_item)
            
            # 时间轴
            time_item = QTableWidgetItem(str(time_axis))
            time_item.setForeground(QColor('#4ec9b0'))
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # 居中对齐
            # 设置为不可编辑
            time_item.setFlags(time_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.result_table.setItem(row, 1, time_item)
            
            # 对应台词：完全处理HTML标签，只保留纯文本
            import re
            
            # 提取原始文本，移除所有HTML标签
            text_str = str(text)
            # 移除所有HTML标签
            plain_text = re.sub(r'<[^>]+>', '', text_str)
            
            # 创建纯文本项，不包含任何HTML标签
            text_item = QTableWidgetItem(plain_text)
            text_item.setForeground(QColor('#ffffff'))
            # 设置为不可编辑
            text_item.setFlags(text_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.result_table.setItem(row, 2, text_item)
            
            # 行号
            lineno_item = QTableWidgetItem(str(lineno))
            lineno_item.setForeground(QColor('#979a98'))
            lineno_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # 居中对齐
            # 设置为不可编辑
            lineno_item.setFlags(lineno_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.result_table.setItem(row, 3, lineno_item)
            
            # 文件名
            filename_item = QTableWidgetItem(str(filename))
            filename_item.setForeground(QColor('#149acd'))
            # 设置为不可编辑
            filename_item.setFlags(filename_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.result_table.setItem(row, 4, filename_item)
            
            # 保存文件路径
            self.result_file_paths.append(filepath)
        
        # 保存变体集和匹配词集到实例变量，以便在导出时使用
        self.target_variant_set = target_variant_set
        self.matched_terms_set = matched_terms_set

        # 更新变体型列表显示
        if target_variant_set:
            # 将生成的变体列表转换为字符串，用逗号分隔（横着显示）
            variant_text = ", ".join(target_variant_set)
            # 根据当前语料库类型更新对应的变体型列表显示
            if self.current_corpus_tab == 0:  # 英语语料库
                if hasattr(self, 'english_lemmalist_display'):
                    self.english_lemmalist_display.setText(variant_text)
            else:  # 韩语语料库
                if hasattr(self, 'korean_lemmalist_display'):
                    self.korean_lemmalist_display.setText(variant_text)
        else:
            # 如果没有生成变体列表，显示默认文本
            default_text = "无变体"
            if self.current_corpus_tab == 0:  # 英语语料库
                if hasattr(self, 'english_lemmalist_display'):
                    self.english_lemmalist_display.setText(default_text)
            else:  # 韩语语料库
                if hasattr(self, 'korean_lemmalist_display'):
                    self.korean_lemmalist_display.setText(default_text)

        # 确保表格不可编辑，在填充完成后再次设置
        self.result_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # 重新设置列宽，确保固定列保持固定宽度
        self.restore_column_settings()

        # 确保表头高度为30px
        header = self.result_table.horizontalHeader()
        header.setFixedHeight(30)
        header.style().unpolish(header)
        header.style().polish(header)
        header.update()

        # 自动调整行高以适应内容
        self.result_table.resizeRowsToContents()

        # 保存搜索历史到对应的文件
        if hasattr(self, 'current_search_params'):
            corpus_type = "eng" if self.current_corpus_tab == 0 else "kor"
            search_history_manager.set_corpus_type(corpus_type)

            # 使用具体词典型作为关键词类型
            keyword_type_to_save = pos_full if pos_full else self.current_search_params.get('keyword_type', '')

            search_history_manager.add_record(
                keywords=self.current_search_params['keywords'],
                input_path=self.current_search_params['input_path'],
                case_sensitive=self.current_search_params['case_sensitive'],
                fuzzy_match=self.current_search_params['fuzzy_match'],
                regex_enabled=self.current_search_params['regex_enabled'],
                result_count=len(results),
                keyword_type=keyword_type_to_save,
                lemma=lemma,
                actual_variant_set=actual_variant_set,
                target_variant_set=target_variant_set
            )

        self.status_bar.showMessage(f"✓ 搜索完成，找到 {len(results)} 条结果")

        # 自动导出搜索结果
        self.auto_export_results(results)

    def auto_export_results(self, results):
        """自动导出搜索结果到HTML文件，保留高亮加粗特效"""
        try:
            import os
            import re
            from datetime import datetime

            # 获取当前时间戳用于文件命名（精确到分钟）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")

            # 获取关键词用于文件名（只保留字母数字和下划线，避免文件名问题）
            keywords = self.current_search_params["keywords"]
            # 清理关键词，只保留字母数字和下划线
            clean_keywords = re.sub(r'[^\w\u4e00-\u9fff\uac00-\ud7af]', '_', keywords)
            # 限制长度
            clean_keywords = clean_keywords[:50] if len(clean_keywords) > 50 else clean_keywords

            # 确定输出目录 - 使用输入目录作为输出目录
            output_dir = self.ReadPathInput.text().strip()
            if not output_dir or not os.path.exists(output_dir):
                output_dir = os.getcwd()

            # 创建输出文件名
            corpus_name = "English" if self.current_corpus_tab == 0 else "Korean"
            output_filename = f"search_results_{corpus_name}_{timestamp}_{clean_keywords}.html"
            output_path = os.path.join(output_dir, output_filename)

            # 准备HTML内容
            html_content = []
            html_content.append('<!DOCTYPE html>')
            html_content.append('<html lang="zh-CN">')
            html_content.append('<head>')
            html_content.append('<meta charset="UTF-8">')
            html_content.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
            html_content.append(f'<title>搜索结果 - {corpus_name} - {timestamp}</title>')
            html_content.append('<style>')
            html_content.append('body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }')
            html_content.append('table { border-collapse: collapse; width: 100%; background-color: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }')
            html_content.append('th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }')
            html_content.append('th { background-color: #4CAF50; color: white; }')
            html_content.append('tr:nth-child(even) { background-color: #f2f2f2; }')
            html_content.append('tr:hover { background-color: #f5f5f5; }')
            html_content.append('.highlight { background-color: yellow; font-weight: bold; }')
            html_content.append('.episode { color: #FFC209; }')
            html_content.append('.time-axis { color: #4ec9b0; text-align: center; }')
            # 移除白色字体颜色设定
            html_content.append('.content { }')
            html_content.append('.line-number { color: #979a98; text-align: center; }')
            html_content.append('.filename { color: #149acd; }')
            html_content.append('</style>')
            html_content.append('</head>')
            html_content.append('<body>')
            # 添加搜索信息
            html_content.append(f'<h1>搜索结果 - {corpus_name}语料库</h1>')
            html_content.append(f'<p>搜索时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>')
            html_content.append(f'<p>搜索关键词: {self.current_search_params["keywords"]}</p>')
            html_content.append(f'<p>搜索路径: {self.current_search_params["input_path"]}</p>')
            html_content.append(f'<p>结果数量: {len(results)}</p>')
            
            # 添加lemma和lemmalist信息（隐藏字段，用于恢复显示）
            if corpus_name == "Korean":
                # 获取韩语相关显示内容
                lemma_text = self.korean_lemma_display.text() if hasattr(self, 'korean_lemma_display') else ""
                lemmalist_text = self.korean_lemmalist_display.text() if hasattr(self, 'korean_lemmalist_display') else ""
                html_content.append(f'<p style="display:none" id="lemma_text">{lemma_text}</p>')
                html_content.append(f'<p style="display:none" id="lemmalist_text">{lemmalist_text}</p>')
            else:
                # 获取英语相关显示内容
                lemma_text = self.english_lemma_display.text() if hasattr(self, 'english_lemma_display') else ""
                lemmalist_text = self.english_lemmalist_display.text() if hasattr(self, 'english_lemmalist_display') else ""
                html_content.append(f'<p style="display:none" id="lemma_text">{lemma_text}</p>')
                html_content.append(f'<p style="display:none" id="lemmalist_text">{lemmalist_text}</p>')
            html_content.append('<table>')
            html_content.append('<thead>')
            html_content.append('<tr>')
            html_content.append('<th>集数</th>')
            html_content.append('<th>时间轴</th>')
            html_content.append('<th>对应台词</th>')
            html_content.append('<th>行号</th>')
            html_content.append('<th>文件名</th>')
            html_content.append('</tr>')
            html_content.append('</thead>')
            html_content.append('<tbody>')

            # 添加搜索结果行
            for row, result in enumerate(results):
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

                # 获取当前搜索的关键词和变体，用于高亮
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
                        if hasattr(self, 'korean_variant_set') and self.korean_variant_set:
                            current_keywords.extend(self.korean_variant_set)

                        # 添加目标变体集和匹配词集
                        if hasattr(self, 'target_variant_set') and self.target_variant_set:
                            current_keywords.extend(self.target_variant_set)
                        if hasattr(self, 'matched_terms_set') and self.matched_terms_set:
                            current_keywords.extend(self.matched_terms_set)

                        # 去重并过滤空字符串
                        current_keywords = [k for k in list(set(current_keywords)) if k]

                # 处理文本，添加关键词高亮
                processed_text = str(text)

                # 移除所有现有的颜色样式（包括前景色和HTML标签中的颜色样式）
                import re
                # 移除所有包含颜色定义的span标签
                processed_text = re.sub(r'<span[^>]*style[^>]*color[^>]*>', '', processed_text)
                # 移除所有剩余的span闭合标签
                processed_text = processed_text.replace('</span>', '')

                # 如果有关键词，添加高亮
                if current_keywords:
                    # 确保关键词按长度降序排列，避免短关键词匹配长关键词的一部分
                    current_keywords.sort(key=lambda x: len(x), reverse=True)

                    for keyword in current_keywords:
                        if keyword:
                            # 使用正则表达式替换，不使用单词边界（适用于韩语）
                            regex_pattern = re.escape(keyword)
                            processed_text = re.sub(
                                rf'({regex_pattern})',
                                r'<span class="highlight">\1</span>',
                                processed_text,
                                flags=re.IGNORECASE
                            )

                html_content.append('<tr>')
                html_content.append(f'<td class="episode">{episode}</td>')
                html_content.append(f'<td class="time-axis">{time_axis}</td>')
                html_content.append(f'<td class="content">{processed_text}</td>')
                html_content.append(f'<td class="line-number">{lineno}</td>')
                html_content.append(f'<td class="filename">{filename}</td>')
                # 添加隐藏的文件路径字段
                html_content.append(f'<td style="display:none">{filepath}</td>')
                html_content.append('</tr>')

            html_content.append('</tbody>')
            html_content.append('</table>')
            html_content.append('</body>')
            html_content.append('</html>')

            # 写入HTML文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(html_content))

            self.status_bar.showMessage(f"✓ 搜索结果已自动导出到: {output_filename}")

        except Exception as e:
            print(f"自动导出搜索结果时出错: {e}")
            import traceback
            traceback.print_exc()

    def search_failed(self, error_message):
        """搜索失败"""
        # 隐藏进度条
        self.ProgressBar.setVisible(False)
        
        # 启用搜索按钮
        self.search_btn.setEnabled(True)
        
        self.status_bar.showMessage("❌ 搜索失败")
        QMessageBox.critical(self, "❌ 搜索失败", error_message)
    
    def load_search_results_from_html(self):
        """
        从HTML文件加载搜索结果到表格中
        """
        # 使用QFileDialog选择HTML文件，默认从输入路径文件夹开始浏览
        default_dir = self.ReadPathInput.text().strip()
        if not default_dir or not os.path.exists(default_dir):
            default_dir = os.getcwd()
            
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择搜索结果HTML文件",
            default_dir,
            "HTML Files (*.html);;All Files (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            # 读取HTML文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 解析HTML内容，提取表格数据
            from bs4 import BeautifulSoup
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 查找表格
            table = soup.find('table')
            if not table:
                QMessageBox.warning(self, "错误", "HTML文件中未找到搜索结果表格")
                return
            
            # 初始化搜索信息字典
            search_info = {}
            
            # 从HTML中提取搜索信息
            import re
            
            # 查找搜索关键词
            keyword_p = soup.find('p', string=re.compile(r'搜索关键词:'))
            if keyword_p:
                search_info['keywords'] = keyword_p.text.split('搜索关键词:')[-1].strip()
            
            # 查找搜索路径，判断是否为韩语语料库
            path_p = soup.find('p', string=re.compile(r'搜索路径:'))
            if path_p:
                search_path = path_p.text.split('搜索路径:')[-1].strip()
                # 检查语料库类型
                is_korean = '韩语' in search_path or 'Korean' in search_path
                search_info['corpus_type'] = 'korean' if is_korean else 'english'
            
            # 获取表格行
            rows = table.find_all('tr')
            if len(rows) <= 1:  # 只有表头
                QMessageBox.warning(self, "错误", "HTML文件中未找到搜索结果数据")
                return
            
            # 清空当前表格
            self.result_table.setRowCount(0)
            self.result_file_paths = []
            
            # 提取数据行（跳过表头）
            data_rows = rows[1:]
            
            # 设置表格行数
            self.result_table.setRowCount(len(data_rows))
            
            for row_idx, row in enumerate(data_rows):
                cells = row.find_all('td')
                if len(cells) < 5:
                    continue
                
                # 提取各列数据（同时保留原始HTML内容）
                episode_text = cells[0].get_text(strip=True)
                time_axis_text = cells[1].get_text(strip=True)
                content_text = cells[2].get_text(strip=True)
                line_number_text = cells[3].get_text(strip=True)
                filename_text = cells[4].get_text(strip=True)
                
                # 提取原始HTML内容
                episode_html = str(cells[0])
                time_axis_html = str(cells[1])
                content_html = str(cells[2])
                line_number_html = str(cells[3])
                filename_html = str(cells[4])
                
                # 提取文件路径（如果有第六列）
                filepath = ""
                if len(cells) >= 6:
                    filepath = cells[5].get_text(strip=True)
                
                # 设置集数列
                episode_item = QTableWidgetItem(episode_text)
                episode_item.setForeground(QColor('#FFC209'))
                episode_item.setFlags(episode_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                # 保存原始HTML内容到UserRole
                episode_item.setData(Qt.ItemDataRole.UserRole, episode_html)
                self.result_table.setItem(row_idx, 0, episode_item)
                
                # 设置时间轴列
                time_item = QTableWidgetItem(time_axis_text)
                time_item.setForeground(QColor('#4ec9b0'))
                time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                time_item.setFlags(time_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                # 保存原始HTML内容到UserRole
                time_item.setData(Qt.ItemDataRole.UserRole, time_axis_html)
                self.result_table.setItem(row_idx, 1, time_item)
                
                # 设置对应台词列
                content_item = QTableWidgetItem(content_text)
                content_item.setForeground(QColor('#ffffff'))
                content_item.setFlags(content_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                # 保存原始HTML内容到UserRole
                content_item.setData(Qt.ItemDataRole.UserRole, content_html)
                self.result_table.setItem(row_idx, 2, content_item)
                
                # 设置行号列
                line_item = QTableWidgetItem(line_number_text)
                line_item.setForeground(QColor('#979a98'))
                line_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                line_item.setFlags(line_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                # 保存原始HTML内容到UserRole
                line_item.setData(Qt.ItemDataRole.UserRole, line_number_html)
                self.result_table.setItem(row_idx, 3, line_item)
                
                # 设置文件名
                filename_item = QTableWidgetItem(filename_text)
                filename_item.setForeground(QColor('#149acd'))
                filename_item.setFlags(filename_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                # 保存原始HTML内容到UserRole
                filename_item.setData(Qt.ItemDataRole.UserRole, filename_html)
                self.result_table.setItem(row_idx, 4, filename_item)
                
                # 保存文件路径
                self.result_file_paths.append(filepath)
            
            # 从HTML中提取lemma和lemmalist信息，恢复显示内容
            lemma_p = soup.find('p', id='lemma_text')
            lemmalist_p = soup.find('p', id='lemmalist_text')
            
            if lemma_p and lemmalist_p:
                lemma_text = lemma_p.get_text(strip=True)
                lemmalist_text = lemmalist_p.get_text(strip=True)
                
                # 根据语料库类型更新对应显示控件
                if search_info.get('corpus_type') == 'korean':
                    # 切换到韩语标签页
                    self.corpus_tab_widget.setCurrentIndex(1)
                    # 更新韩语显示内容
                    if hasattr(self, 'korean_lemma_display'):
                        self.korean_lemma_display.setText(lemma_text)
                    if hasattr(self, 'korean_lemmalist_display'):
                        self.korean_lemmalist_display.setText(lemmalist_text)
                else:
                    # 切换到英语标签页
                    self.corpus_tab_widget.setCurrentIndex(0)
                    # 更新英语显示内容
                    if hasattr(self, 'english_lemma_display'):
                        self.english_lemma_display.setText(lemma_text)
                    if hasattr(self, 'english_lemmalist_display'):
                        self.english_lemmalist_display.setText(lemmalist_text)
            
            # 自动调整行高
            self.result_table.resizeRowsToContents()
            
            # 更新状态栏
            self.status_bar.showMessage(f"✓ 成功加载 {len(data_rows)} 条搜索结果")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载搜索结果失败: {str(e)}")
    
    def show_search_history(self):
        """
        显示搜索历史
        """
        # 根据当前标签页设置语料库类型
        corpus_type = "eng" if self.current_corpus_tab == 0 else "kor"
        search_history_manager.set_corpus_type(corpus_type)
        
        # 检查是否有历史记录
        history = search_history_manager.get_recent_records(100)
        
        if not history:
            corpus_name = "英语" if corpus_type == "eng" else "韩语"
            QMessageBox.information(self, "搜索历史", f"{corpus_name}语料库暂无搜索历史")
            return
        
        # 如果历史窗口已存在且未关闭，且语料库类型匹配，则直接显示
        if (self.history_window is not None and 
            not self.history_window.isHidden() and 
            hasattr(self.history_window, 'corpus_type') and 
            self.history_window.corpus_type == corpus_type):
            self.history_window.raise_()
            self.history_window.activateWindow()
            return
        
        # 关闭旧的历史窗口（如果存在且语料库类型不匹配）
        if (self.history_window is not None and 
            hasattr(self.history_window, 'corpus_type') and 
            self.history_window.corpus_type != corpus_type):
            self.history_window.close()
            self.history_window = None
        
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
        # 获取当前选中的单元格
        selected_items = self.result_table.selectedItems()
        has_selection = len(selected_items) > 0
        
        # 保存选中的行列号
        selected_row = -1
        selected_col = -1
        if selected_items:
            selected_row = selected_items[0].row()
            selected_col = selected_items[0].column()
        
        # 检查表格是否有数据
        has_data = self.result_table.rowCount() > 0
        
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
        export_all_action = menu.addAction("📤 导出所有行")
        
        # 设置菜单项的启用状态
        # 复制单元格：必须有选中的单元格
        copy_cell_action.setEnabled(has_selection and selected_row >= 0 and selected_col >= 0)
        
        # 复制选中行：必须有选中的行
        copy_action.setEnabled(has_selection)
        
        # 打开文件：必须有选中的行
        open_action.setEnabled(has_selection)
        
        # 导出选中行：必须有选中的行
        export_action.setEnabled(has_selection)
        
        # 导出所有行：只要有数据就启用
        export_all_action.setEnabled(has_data)
        
        action = menu.exec(self.result_table.mapToGlobal(pos))
        
        if has_selection and action == copy_cell_action:
            # 复制当前选中的单元格
            if selected_row >= 0 and selected_col >= 0:
                self.copy_selected_cell(selected_row, selected_col)
        elif has_selection and action == copy_action:
            self.copy_selected_row(selected_row)
        elif has_selection and action == open_action:
            self.open_file(selected_row)
        elif has_selection and action == export_action:
            self.export_selected_row(selected_row)
        elif action == export_all_action:
            self.export_all_rows()
    
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
            QMenu::item:disabled {
                color: #888888;
            }
            QMenu::item:disabled:selected {
                background-color: #004080;
                color: #aaaaaa;
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
        column_names = ['出处', '时间轴', '对应台词', '行号', '文件名']
        
        # 为每列创建复选框动作
        for col in range(self.result_table.columnCount()):
            action = columns_menu.addAction(column_names[col])
            action.setCheckable(True)
            action.setChecked(not self.result_table.isColumnHidden(col))
            action.triggered.connect(lambda checked, c=col: self.toggle_column_visibility(c, checked))
        
        menu.addSeparator()
        reset_action = menu.addAction("🔄 重置表格")
        
        action = menu.exec(self.result_table.horizontalHeader().mapToGlobal(pos))
        
        if action == reset_action:
            self.reset_table()
    
    def enforce_min_column_width(self, logicalIndex, oldSize, newSize):
        """确保列宽在配置的限制范围内"""
        config = self.table_manager.get_column_config(logicalIndex)

        # 检查是否为固定列
        if config.get('mode') == 'fixed':
            # 固定列：强制恢复为固定宽度
            self.result_table.blockSignals(True)
            self.result_table.setColumnWidth(logicalIndex, config['fixed_width'])
            self.result_table.blockSignals(False)

            # 检查最后一个可见列是否是固定列，如果是则不启用拉伸
            header = self.result_table.horizontalHeader()
            last_visible_col = None
            for visual_idx in range(header.count()):
                logical_idx = header.logicalIndex(visual_idx)
                if not self.result_table.isColumnHidden(logical_idx):
                    last_visible_col = logical_idx
            if last_visible_col is not None:
                last_col_config = self.table_manager.get_column_config(last_visible_col)
                if last_col_config.get('mode') == 'fixed':
                    header.setStretchLastSection(False)
                else:
                    header.setStretchLastSection(True)
            return

        # 检查是否有宽度限制
        min_width = config.get('min_width')
        max_width = config.get('max_width')
        if min_width is not None and max_width is not None:
            if newSize < min_width:
                self.result_table.setColumnWidth(logicalIndex, min_width)
            elif newSize > max_width:
                self.result_table.setColumnWidth(logicalIndex, max_width)
    
    def _restore_fixed_width(self):
        """恢复固定宽度列的宽度"""
        if hasattr(self, '_fixed_column_to_restore'):
            logicalIndex = self._fixed_column_to_restore
            fixed_width = self.table_manager.get_fixed_width(logicalIndex)
            if fixed_width is not None:
                self.result_table.blockSignals(True)
                self.result_table.setColumnWidth(logicalIndex, fixed_width)
                self.result_table.blockSignals(False)
    
    def on_column_resized(self, logicalIndex, oldSize, newSize):
        """列宽变化时重新计算行高"""
        # 延迟执行，避免频繁更新
        if hasattr(self, '_resize_timer'):
            self._resize_timer.stop()
        
        self._resize_timer = QTimer()
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self.update_row_heights)
        self._resize_timer.start(100)  # 100ms 后执行
    
    def update_row_heights(self):
        """更新所有行的行高"""
        from PySide6.QtWidgets import QStyleOptionViewItem

        # 恢复固定列的宽度
        for col in range(self.result_table.columnCount()):
            config = self.table_manager.get_column_config(col)
            if config.get('mode') == 'fixed':
                self.result_table.blockSignals(True)
                self.result_table.setColumnWidth(col, config['fixed_width'])
                self.result_table.blockSignals(False)

        for row in range(self.result_table.rowCount()):
            # 触发 sizeHint 重新计算
            index = self.result_table.model().index(row, 2)  # 对应台词列

            # 创建正确的 option 参数
            option = QStyleOptionViewItem()
            option.initFrom(self.result_table)
            option.rect = self.result_table.visualRect(index)

            size_hint = self.result_table.itemDelegate(index).sizeHint(option, index)
            self.result_table.setRowHeight(row, size_hint.height())

        # 根据最后一个可见列是否为固定列来设置拉伸属性
        header = self.result_table.horizontalHeader()
        last_visible_col = None
        for visual_idx in range(header.count()):
            logical_idx = header.logicalIndex(visual_idx)
            if not self.result_table.isColumnHidden(logical_idx):
                last_visible_col = logical_idx
        if last_visible_col is not None:
            last_col_config = self.table_manager.get_column_config(last_visible_col)
            if last_col_config.get('mode') == 'fixed':
                header.setStretchLastSection(False)
            else:
                header.setStretchLastSection(True)

        # 强制更新表头布局，确保固定列宽设置生效
        header.doItemsLayout()
        self.result_table.updateGeometry()
        self.result_table.viewport().update()
    
    def toggle_column_visibility(self, col_index, checked):
        """切换列的显示/隐藏状态"""
        # 获取表格容器宽度
        table_width = self.result_table.viewport().width()
        
        # 记录当前所有列的宽度，用于后续计算
        current_widths = [self.result_table.columnWidth(col) for col in range(self.result_table.columnCount())]
        
        # 执行列隐藏/显示操作
        self.result_table.setColumnHidden(col_index, not checked)

        # 保存列显示配置
        visibility = []
        for col in range(self.result_table.columnCount()):
            visibility.append(not self.result_table.isColumnHidden(col))

        # 获取当前的列设置
        column_settings = config_manager.get_column_settings('result')
        # 只更新 visibility，保持 widths 和 order 不变
        config_manager.set_column_settings('result', column_settings['widths'], column_settings['order'], visibility)

        # 重新设置列的调整模式和拉伸属性
        header = self.result_table.horizontalHeader()

        # 计算可见列的总宽度和弹性列信息
        visible_width = 0
        flexible_columns = []  # 存储弹性列索引
        fixed_columns = []     # 存储固定列索引
        
        for col in range(self.result_table.columnCount()):
            if not self.result_table.isColumnHidden(col):
                config = self.table_manager.get_column_config(col)
                if config.get('mode') == 'fixed':
                    visible_width += config['fixed_width']
                    fixed_columns.append(col)
                else:
                    visible_width += self.result_table.columnWidth(col)
                    flexible_columns.append(col)
        
        # 计算可用宽度和需要分配的额外宽度
        available_width = table_width
        extra_width = available_width - visible_width
        
        # 如果有额外宽度需要分配，且存在弹性列
        if extra_width > 0 and flexible_columns:
            # 计算每个弹性列当前宽度占弹性列总宽度的比例
            total_flexible_width = 0
            for col in flexible_columns:
                total_flexible_width += self.result_table.columnWidth(col)
            
            # 按照比例分配额外宽度
            for col in flexible_columns:
                current_width = self.result_table.columnWidth(col)
                if total_flexible_width > 0:
                    # 计算该列应分配的额外宽度
                    col_extra = int(extra_width * (current_width / total_flexible_width))
                    new_width = current_width + col_extra
                    
                    # 应用宽度限制
                    config = self.table_manager.get_column_config(col)
                    min_width = config.get('min_width', 0)
                    max_width = config.get('max_width', float('inf'))
                    new_width = max(min_width, min(max_width, new_width))
                    
                    self.result_table.setColumnWidth(col, new_width)
        
        # 先设置所有列的ResizeMode
        for col in range(self.result_table.columnCount()):
            config = self.table_manager.get_column_config(col)
            if config.get('mode') == 'fixed':
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
            else:  # 其他可调整列
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)

        # 检查最后一个可见列是否是固定列，如果是则不启用拉伸
        last_visible_col = None
        for visual_idx in range(header.count()):
            logical_idx = header.logicalIndex(visual_idx)
            if not self.result_table.isColumnHidden(logical_idx):
                last_visible_col = logical_idx
        if last_visible_col is not None:
            last_col_config = self.table_manager.get_column_config(last_visible_col)
            if last_col_config.get('mode') == 'fixed':
                header.setStretchLastSection(False)
            else:
                header.setStretchLastSection(True)

        # 移除了强制移动行号列的逻辑，保留用户自定义的列顺序

        # 强制重新布局，确保隐藏列后其他列正确填充空间
        header.doItemsLayout()
        self.result_table.updateGeometry()
        self.result_table.viewport().update()

        # 强制整个表格重新布局
        self.result_table.doItemsLayout()

        # 移除了强制移动行号列的逻辑，保留用户自定义的列顺序

        # 更新状态栏提示
        column_names = ['出处', '时间轴', '对应台词', '行号', '文件名']
        status = "显示" if checked else "隐藏"
        self.status_bar.showMessage(f"📊 已{status}列: {column_names[col_index]}")

    def _ensure_row_number_column_at_end(self):
        """确保行号列保持在表格的最右边 - 已移除强制移动逻辑，保留用户自定义的列顺序"""
        pass

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
                QMessageBox.critical(self, "错误", f"打开文件失败: {str(e)}")
        else:
            QMessageBox.warning(self, "错误", f"文件不存在: {filepath}")
    
    def export_selected_row(self, row):
        """导出选中行（CSV格式）"""
        import csv
        import re
        import datetime

        # 获取输出目录
        output_dir = self.ReadPathInput.text().strip()
        if not output_dir or not os.path.exists(output_dir):
            output_dir = os.getcwd()

        # 获取关键词用于文件名（只保留字母数字和下划线，避免文件名问题）
        keywords = self.current_search_params["keywords"] if hasattr(self, 'current_search_params') and 'keywords' in self.current_search_params else "unknown"
        # 清理关键词，只保留字母数字和下划线
        clean_keywords = re.sub(r'[^\w\u4e00-\u9fff\uac00-\ud7af]', '_', keywords)
        # 限制长度
        clean_keywords = clean_keywords[:50] if len(clean_keywords) > 50 else clean_keywords

        # 生成文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")  # 精确到分钟
        output_file = os.path.join(output_dir, f"selected_row_{timestamp}_{clean_keywords}.csv")

        # 写入 CSV 文件
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)

            # 写入表头
            headers = []
            for col in range(self.result_table.columnCount()):
                headers.append(self.result_table.horizontalHeaderItem(col).text())
            writer.writerow(headers)

            # 写入数据行
            row_data = []
            for col in range(self.result_table.columnCount()):
                item = self.result_table.item(row, col)
                if item:
                    # 去除HTML标签
                    raw_text = item.text()
                    clean_text = self._remove_html_tags(raw_text)
                    row_data.append(clean_text)
                else:
                    row_data.append("")
            writer.writerow(row_data)

        QMessageBox.information(self, "✅ 成功", f"结果已导出到 {output_file}")
    
    def export_all_rows(self):
        """导出所有行（CSV格式）"""
        import csv
        import re
        import datetime

        if self.result_table.rowCount() == 0:
            QMessageBox.warning(self, "❌ 警告", "表格中没有数据可导出")
            return

        # 获取输出目录
        output_dir = self.ReadPathInput.text().strip()
        if not output_dir or not os.path.exists(output_dir):
            output_dir = os.getcwd()

        # 获取关键词用于文件名（只保留字母数字和下划线，避免文件名问题）
        keywords = self.current_search_params["keywords"] if hasattr(self, 'current_search_params') and 'keywords' in self.current_search_params else "unknown"
        # 清理关键词，只保留字母数字和下划线
        clean_keywords = re.sub(r'[^\w\u4e00-\u9fff\uac00-\ud7af]', '_', keywords)
        # 限制长度
        clean_keywords = clean_keywords[:50] if len(clean_keywords) > 50 else clean_keywords

        # 生成文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")  # 精确到分钟
        output_file = os.path.join(output_dir, f"all_rows_{timestamp}_{clean_keywords}.csv")

        try:
            # 写入 CSV 文件
            with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)

                # 写入表头
                headers = []
                for col in range(self.result_table.columnCount()):
                    headers.append(self.result_table.horizontalHeaderItem(col).text())
                writer.writerow(headers)

                # 写入所有数据行
                for row in range(self.result_table.rowCount()):
                    row_data = []
                    for col in range(self.result_table.columnCount()):
                        item = self.result_table.item(row, col)
                        if item:
                            # 去除HTML标签
                            raw_text = item.text()
                            clean_text = self._remove_html_tags(raw_text)
                            row_data.append(clean_text)
                        else:
                            row_data.append("")
                    writer.writerow(row_data)

            QMessageBox.information(self, "✅ 成功", f"已导出 {self.result_table.rowCount()} 行数据到 {output_file}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
    
    def reset_column_widths(self):
        """重置列宽"""
        self.result_table.setColumnWidth(0, 200)  # 出处列
        self.result_table.setColumnWidth(1, 80)   # 时间轴列（固定，80像素）
        self.result_table.setColumnWidth(2, 600)  # 对应台词列
        self.result_table.setColumnWidth(3, 60)   # 行号列（固定，60像素）
        self.result_table.setColumnWidth(4, 200)  # 文件名列
    
    def reset_table(self):
        """重置表格：重置列宽、列顺序和列显示状态"""
        header = self.result_table.horizontalHeader()
        
        # 1. 重置列宽
        self.reset_column_widths()
        
        # 2. 重置列顺序到默认顺序（0, 1, 2, 3, 4）
        # 先重置所有列到默认顺序
        for logical_index in range(self.result_table.columnCount()):
            current_visual_index = header.visualIndex(logical_index)
            if current_visual_index != logical_index:
                header.moveSection(current_visual_index, logical_index)
        
        # 3. 重置所有列为显示状态（不隐藏任何列）
        for col in range(self.result_table.columnCount()):
            if self.result_table.isColumnHidden(col):
                self.result_table.setColumnHidden(col, False)
        
        # 4. 更新配置文件
        # 保存默认列顺序和可见性
        default_order = [0, 1, 2, 3, 4]
        default_visibility = [True, True, True, True, True]
        
        # 获取当前列宽
        all_widths = [self.result_table.columnWidth(col) for col in range(self.result_table.columnCount())]
        
        # 保存到配置文件
        config_manager.set_column_settings('result', all_widths, default_order, default_visibility)
    
    def restore_column_settings(self):
        """恢复列宽和顺序"""
        # 从配置文件获取列设置
        column_settings = config_manager.get_column_settings('result')
        widths = column_settings['widths']
        visibility = column_settings['visibility']
        order = column_settings['order']

        # 设置列宽调整模式
        header = self.result_table.horizontalHeader()

        # 确保宽度列表至少有5个元素
        while len(widths) < 5:
            widths.append(0)

        # 确保可见性列表至少有5个元素
        while len(visibility) < 5:
            visibility.append(True)

        # 恢复列的显示/隐藏状态
        for col in range(self.result_table.columnCount()):
            self.result_table.setColumnHidden(col, not visibility[col])

        # 恢复列顺序
        if order and len(order) == self.result_table.columnCount():
            # 先重置所有列到默认顺序
            for logical_index in range(self.result_table.columnCount()):
                current_visual_index = header.visualIndex(logical_index)
                if current_visual_index != logical_index:
                    header.moveSection(current_visual_index, logical_index)

            # 然后按照配置的顺序移动列
            for visual_index, logical_index in enumerate(order):
                current_visual_index = header.visualIndex(logical_index)
                if current_visual_index != visual_index:
                    header.moveSection(current_visual_index, visual_index)

        # 先设置所有列的ResizeMode
        for col in range(self.result_table.columnCount()):
            config = self.table_manager.get_column_config(col)
            if config.get('mode') == 'fixed':
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
            else:  # 其他可调整列
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)

        # 检查最后一个可见列是否是固定列，如果是则不启用拉伸
        last_visible_col = None
        for visual_idx in range(header.count()):
            logical_idx = header.logicalIndex(visual_idx)
            if not self.result_table.isColumnHidden(logical_idx):
                last_visible_col = logical_idx
        if last_visible_col is not None:
            last_col_config = self.table_manager.get_column_config(last_visible_col)
            if last_col_config.get('mode') == 'fixed':
                header.setStretchLastSection(False)
            else:
                header.setStretchLastSection(True)

        # 然后设置列宽
        # 临时禁用sectionResized信号，防止信号处理影响列宽
        # 不再需要断开连接，因为已经使用表格管理器的实现

        for col in range(self.result_table.columnCount()):
            config = self.table_manager.get_column_config(col)
            if config.get('mode') == 'fixed':
                # 固定列使用硬编码值，不受配置文件影响
                self.result_table.setColumnWidth(col, config['fixed_width'])
            else:  # 可调整列
                # 直接使用配置文件中的宽度，覆盖初始值
                width = widths[col]
                # 如果配置文件中该列有宽度设置，则使用配置文件中的值，否则使用默认值
                if width > 0:
                    # 应用宽度限制
                    min_width = config.get('min_width')
                    max_width = config.get('max_width')
                    if min_width is not None and max_width is not None:
                        width = min(max(min_width, width), max_width)
                else:
                    # 如果配置文件中该列没有宽度设置，则使用默认值
                    width = config.get('default', 200)

                # 强制设置列宽，覆盖初始值
                self.result_table.setColumnWidth(col, width)

        # 重新启用sectionResized信号
        header.sectionResized.connect(self.enforce_min_column_width)

        # 强制刷新表头，确保列宽设置生效
        header.doItemsLayout()
        self.result_table.updateGeometry()
        self.result_table.update()
        self.result_table.updateGeometry()
        self.result_table.update()
        self.result_table.viewport().update()

        # 强制刷新表头样式，确保高度设置生效
        header.style().unpolish(header)
        header.style().polish(header)
        header.update()
    
    def on_section_moved(self, logicalIndex, oldVisualIndex, newVisualIndex):
        """当列顺序变化时，保存新的列顺序"""
        # 恢复固定列的宽度
        for col in range(self.result_table.columnCount()):
            config = self.table_manager.get_column_config(col)
            if config.get('mode') == 'fixed':
                self.result_table.blockSignals(True)
                self.result_table.setColumnWidth(col, config['fixed_width'])
                self.result_table.blockSignals(False)

        # 保存列设置
        self.save_column_settings()

        # 根据最后一个可见列是否为固定列来设置拉伸属性
        header = self.result_table.horizontalHeader()
        last_visible_col = None
        for visual_idx in range(header.count()):
            logical_idx = header.logicalIndex(visual_idx)
            if not self.result_table.isColumnHidden(logical_idx):
                last_visible_col = logical_idx
        if last_visible_col is not None:
            last_col_config = self.table_manager.get_column_config(last_visible_col)
            if last_col_config.get('mode') == 'fixed':
                header.setStretchLastSection(False)
            else:
                header.setStretchLastSection(True)

        # 强制更新表头布局，确保固定列宽设置生效
        header.doItemsLayout()
        self.result_table.updateGeometry()
        self.result_table.viewport().update()
    
    def save_column_settings(self):
        """保存列宽和列顺序到配置文件"""
        # 获取所有列的宽度
        all_widths = [0] * self.result_table.columnCount()
        
        for col in range(self.result_table.columnCount()):
            config = self.table_manager.get_column_config(col)
            if config.get('mode') == 'fixed':
                # 固定列使用硬编码值
                all_widths[col] = config['fixed_width']
            else:
                # 可调整列获取当前宽度并应用限制
                width = self.result_table.columnWidth(col)
                min_width = config.get('min_width')
                max_width = config.get('max_width')
                if min_width is not None and max_width is not None:
                    width = min(max(min_width, width), max_width)
                all_widths[col] = width
        
        # 获取当前列顺序
        header = self.result_table.horizontalHeader()
        column_order = []
        for visual_index in range(header.count()):
            logical_index = header.logicalIndex(visual_index)
            column_order.append(logical_index)
        
        # 保存所有列的宽度和顺序
        config_manager.set_column_settings('result', all_widths, column_order) 
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 保存列宽和顺序
        self.save_column_settings()

        # 保存当前标签页的配置
        self.save_current_tab_config()

        # 保存当前标签页索引
        config_manager.set_current_tab(self.current_corpus_tab)

        # 保存UI设置（仅主题等，不包括窗口位置和大小）
        config_manager.set_ui_settings()

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
            # 使用统一的ReadPathInput输入框
            self.ReadPathInput.setText(files[0])
            self.status_bar.showMessage(f"✓ 已选择: {files[0]}")