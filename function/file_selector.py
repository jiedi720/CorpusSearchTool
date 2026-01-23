"""
文件选择模块
实现文件拖拽选择和传统文件选择功能
"""

import os
import tkinter as tk
from tkinter import filedialog
from typing import List, Callable


class FileSelector:
    """文件选择器类"""
    
    def __init__(self, widget, on_files_selected: Callable[[List[str]], None]):
        """
        初始化文件选择器
        
        Args:
            widget: 要添加拖拽功能的部件
            on_files_selected: 文件选择回调函数
        """
        self.widget = widget
        self.on_files_selected = on_files_selected
        
        # 绑定拖拽事件
        self.setup_drag_drop()
    
    def setup_drag_drop(self):
        """设置拖拽功能"""
        # 启用拖拽目标
        self.widget.drop_target_register(tk.DND_FILES)
        self.widget.dnd_bind('<<Drop>>', self.on_drop)
    
    def on_drop(self, event):
        """处理文件拖拽事件"""
        # 获取拖拽的文件路径
        files = self.widget.tk.splitlist(event.data)
        
        # 过滤有效文件
        valid_files = [f for f in files if os.path.exists(f)]
        
        if valid_files:
            self.on_files_selected(valid_files)
    
    @staticmethod
    def select_files(multiple: bool = True) -> List[str]:
        """
        传统文件选择对话框
        
        Args:
            multiple: 是否允许多选
            
        Returns:
            选择的文件路径列表
        """
        if multiple:
            return list(filedialog.askopenfilenames(
                title="选择文件",
                filetypes=[
                    ("支持的文件", "*.srt *.ass *.ssa *.vtt *.txt *.md *.docx *.pdf"),
                    ("字幕文件", "*.srt *.ass *.ssa *.vtt"),
                    ("文档文件", "*.txt *.md *.docx *.pdf"),
                    ("所有文件", "*.*")
                ]
            ))
        else:
            file_path = filedialog.askopenfilename(
                title="选择文件",
                filetypes=[
                    ("支持的文件", "*.srt *.ass *.ssa *.vtt *.txt *.md *.docx *.pdf"),
                    ("字幕文件", "*.srt *.ass *.ssa *.vtt"),
                    ("文档文件", "*.txt *.md *.docx *.pdf"),
                    ("所有文件", "*.*")
                ]
            )
            return [file_path] if file_path else []
    
    @staticmethod
    def select_directory() -> str:
        """选择目录对话框
        
        Returns:
            选择的目录路径
        """
        return filedialog.askdirectory(title="选择目录")


# 示例使用方法：
# 在GUI中使用时，可以这样初始化：
# file_selector = FileSelector(widget, callback_function)