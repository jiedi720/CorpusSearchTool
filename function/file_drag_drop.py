"""
文件拖拽模块
使用tkinterdnd2库实现tkinter的文件拖拽功能
"""

import tkinter as tk
from typing import List, Callable
import os


class FileDragDrop:
    """文件拖拽功能类"""

    def __init__(self, widget: tk.Widget, on_files_dropped: Callable[[List[str]], None]):
        """
        初始化文件拖拽功能

        Args:
            widget: 要添加拖拽功能的部件
            on_files_dropped: 文件拖拽回调函数
        """
        self.widget = widget
        self.on_files_dropped = on_files_dropped

        # 使用tkinterdnd2库设置拖拽功能
        self._setup_tkinterdnd2()

    def _setup_tkinterdnd2(self):
        """使用tkinterdnd2库设置拖拽功能"""
        try:
            import tkinterdnd2
            # 确保窗口支持拖拽
            if not hasattr(self.widget, 'dnd_bind'):
                # 如果不是tkinterdnd2窗口，需要特殊处理
                print("警告：需要使用tkinterdnd2.Tk()创建窗口才能完全支持拖拽")
                return

            # 注册文件拖拽目标
            self.widget.drop_target_register(tkinterdnd2.DND_FILES)

            # 绑定拖拽事件
            self.widget.dnd_bind('<<Drop>>', self._on_drop_tkinterdnd2)

        except ImportError:
            print("错误：需要安装tkinterdnd2库来支持文件拖拽功能")
            print("请运行: pip install tkinterdnd2")
        except Exception as e:
            print(f"设置拖拽功能失败: {e}")

    def _on_drop_tkinterdnd2(self, event):
        """tkinterdnd2拖拽事件处理"""
        try:
            # 获取拖拽的文件路径
            files = self.widget.tk.splitlist(event.data)

            # 过滤有效文件
            valid_files = [f for f in files if os.path.exists(f)]

            if valid_files:
                self.on_files_dropped(valid_files)
        except Exception as e:
            print(f"处理拖拽事件失败: {e}")


def enable_drag_drop_for_window(window: tk.Tk, on_files_dropped: Callable[[List[str]], None]):
    """
    为整个窗口启用拖拽功能

    注意：要完全支持拖拽，需要使用tkinterdnd2.Tk()而不是普通的tk.Tk()

    Args:
        window: Tkinter窗口
        on_files_dropped: 文件拖拽回调函数
    """
    try:
        import tkinterdnd2
        # 检查窗口是否支持拖拽
        if hasattr(window, 'dnd_bind'):
            # 为窗口启用拖拽
            drag_drop = FileDragDrop(window, on_files_dropped)
            return drag_drop
        else:
            print("提示：当前窗口不支持拖拽功能，请使用tkinterdnd2.Tk()创建窗口")
            return None
    except ImportError:
        print("提示：需要安装tkinterdnd2库来支持拖拽功能")
        return None


def create_drag_drop_window(title="拖拽窗口"):
    """
    创建一个支持拖拽的窗口（使用tkinterdnd2）

    Args:
        title: 窗口标题

    Returns:
        支持拖拽的窗口对象
    """
    try:
        import tkinterdnd2
        window = tkinterdnd2.Tk()
        window.title(title)
        return window
    except ImportError:
        print("错误：需要安装tkinterdnd2库")
        print("请运行: pip install tkinterdnd2")
        return tk.Tk()  # 返回普通窗口