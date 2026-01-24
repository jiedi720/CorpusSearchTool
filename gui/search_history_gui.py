#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
搜索历史窗口GUI模块
独立管理搜索历史窗口的显示和交互
"""

from PySide6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, 
    QHeaderView, QMenu, QMessageBox, QApplication
)
from PySide6.QtCore import Qt
from function.search_history_manager import search_history_manager


class CustomHeaderView(QHeaderView):
    """自定义表头，支持右键菜单显示/隐藏列"""
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.parent_table = parent
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_header_context_menu)
    
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
        """)
        
        for i in range(self.count()):
            action = menu.addAction(self.model().headerData(i, self.orientation()))
            action.setCheckable(True)
            action.setChecked(not self.isSectionHidden(i))
            action.triggered.connect(lambda checked, col=i: self.toggle_column_visibility(col))
        
        menu.exec(self.mapToGlobal(pos))
    
    def toggle_column_visibility(self, column):
        """切换列的可见性"""
        if self.isSectionHidden(column):
            self.showSection(column)
        else:
            self.hideSection(column)


class SearchHistoryWindow(QMainWindow):
    """搜索历史窗口"""
    
    def __init__(self, corpus_type: str, parent=None):
        """
        初始化搜索历史窗口
        
        Args:
            corpus_type: 语料库类型 ('eng' 或 'kor')
            parent: 父窗口
        """
        super().__init__(parent)
        self.corpus_type = corpus_type
        self.corpus_name = "英语" if corpus_type == "eng" else "韩语"
        
        # 设置窗口属性
        self.setWindowTitle(f"📜 {self.corpus_name}语料库搜索历史")
        self.resize(800, 600)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #353535;
            }
        """)
        
        # 创建表格
        self.history_table = self._create_table()
        self.setCentralWidget(self.history_table)
        
        # 加载数据
        self._load_history_data()
    
    def _create_table(self) -> QTableWidget:
        """创建历史记录表格"""
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['时间', '关键词', '关键词类型', '路径', '结果数'])
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setWordWrap(False)
        table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        
        # 设置自定义表头
        header = CustomHeaderView(Qt.Orientation.Horizontal, table)
        table.setHorizontalHeader(header)
        header.setSectionsMovable(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        
        # 设置初始列宽
        table.setColumnWidth(0, 150)
        table.setColumnWidth(1, 150)
        table.setColumnWidth(2, 120)
        table.setColumnWidth(3, 250)
        table.setColumnWidth(4, 80)
        header.setFixedHeight(30)
        
        # 设置行高
        table.verticalHeader().setDefaultSectionSize(30)
        table.verticalHeader().setVisible(False)
        
        # 设置右键菜单
        table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        table.customContextMenuRequested.connect(self._show_context_menu)
        
        # 设置表格样式
        table.setStyleSheet("""
            QTableWidget {
                background-color: #1f1f1f;
                alternate-background-color: #252525;
                color: #ffffff;
                gridline-color: #404040;
                border: 1px solid #404040;
                border-radius: 5px;
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
            }
        """)
        
        return table
    
    def _load_history_data(self):
        """加载历史记录数据"""
        search_history_manager.set_corpus_type(self.corpus_type)
        history = search_history_manager.get_recent_records(100)
        
        self.history_table.setRowCount(len(history))
        
        for row, record in enumerate(history):
            # 格式化时间戳
            timestamp = record.get('timestamp', '')
            if timestamp:
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(timestamp)
                    timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
            
            self.history_table.setItem(row, 0, QTableWidgetItem(timestamp))
            self.history_table.setItem(row, 1, QTableWidgetItem(record.get('keywords', '')))
            self.history_table.setItem(row, 2, QTableWidgetItem(record.get('keyword_type', '')))
            self.history_table.setItem(row, 3, QTableWidgetItem(record.get('input_path', '')))
            self.history_table.setItem(row, 4, QTableWidgetItem(str(record.get('result_count', 0))))
    
    def _show_context_menu(self, pos):
        """显示右键菜单"""
        item = self.history_table.itemAt(pos)
        if not item:
            return
        
        # 获取选中的行
        selected_rows = set()
        for item in self.history_table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            selected_rows.add(item.row())
        
        selected_count = len(selected_rows)
        
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
        
        load_action = menu.addAction("📥 加载到搜索框")
        menu.addSeparator()
        copy_action = menu.addAction("📋 复制关键词")
        copy_path_action = menu.addAction("📋 复制路径")
        menu.addSeparator()
        delete_action = menu.addAction(f"🗑️ 删除选中记录 ({selected_count}条)")
        menu.addSeparator()
        clear_all_action = menu.addAction("🗑️ 清除全部历史")
        
        action = menu.exec(self.history_table.mapToGlobal(pos))
        
        if action == load_action:
            first_row = sorted(selected_rows)[0]
            self.load_to_search(first_row)
        elif action == copy_action:
            self.copy_keywords(selected_rows)
        elif action == copy_path_action:
            self.copy_paths(selected_rows)
        elif action == delete_action:
            self.delete_records(selected_rows)
        elif action == clear_all_action:
            self.clear_all_history()
    
    def load_to_search(self, row: int) -> str:
        """
        加载历史记录到搜索框
        
        Returns:
            关键词字符串
        """
        try:
            keyword_item = self.history_table.item(row, 1)
            if keyword_item:
                keyword = keyword_item.text()
                self.close()
                return keyword
        except Exception as e:
            print(f"加载历史记录失败: {e}")
        return ""
    
    def copy_keywords(self, rows: set):
        """复制关键词到剪贴板"""
        try:
            keywords = []
            for row in sorted(rows):
                keyword_item = self.history_table.item(row, 1)
                if keyword_item:
                    keywords.append(keyword_item.text())
            if keywords:
                QApplication.clipboard().setText('\n'.join(keywords))
        except Exception as e:
            print(f"复制关键词失败: {e}")
    
    def copy_paths(self, rows: set):
        """复制路径到剪贴板"""
        try:
            paths = []
            for row in sorted(rows):
                path_item = self.history_table.item(row, 3)
                if path_item:
                    paths.append(path_item.text())
            if paths:
                QApplication.clipboard().setText('\n'.join(paths))
        except Exception as e:
            print(f"复制路径失败: {e}")
    
    def delete_records(self, rows: set):
        """删除选中的历史记录"""
        try:
            search_history_manager.set_corpus_type(self.corpus_type)
            history = search_history_manager.get_recent_records(100)
            
            timestamps_to_delete = []
            for row in sorted(rows):
                if row < len(history):
                    record = history[row]
                    timestamps_to_delete.append(record['timestamp'])
            
            if timestamps_to_delete:
                search_history_manager.remove_records_by_timestamp(timestamps_to_delete)
                self._load_history_data()
        except Exception as e:
            print(f"删除历史记录失败: {e}")
    
    def clear_all_history(self):
        """清除全部历史记录"""
        try:
            # 确认对话框
            reply = QMessageBox.question(
                self,
                "确认清除",
                "确定要清除全部搜索历史吗？此操作不可撤销。",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                search_history_manager.set_corpus_type(self.corpus_type)
                search_history_manager.clear_history()
                self._load_history_data()
        except Exception as e:
            print(f"清除历史记录失败: {e}")
    
    def refresh(self):
        """刷新历史记录"""
        self._load_history_data()