from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHeaderView, QTabWidget, QComboBox, QTableWidget
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt
import sys
import io

# 设置标准输出为 UTF-8（只在非打包环境下）
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 全局变量：保存程序启动时的默认样式名称
_original_style = None


def apply_theme(mode):
    """
    应用主题设置到整个应用程序
    
    Args:
        mode: 主题模式，可选值: 
              - "System": 系统默认主题
              - "Light": 浅色主题
              - "Dark": 深色主题
    """
    global _original_style
    
    # 获取当前运行的QApplication实例
    app = QApplication.instance()
    
    # 首次调用时保存原始样式名称
    if _original_style is None:
        _original_style = app.style().objectName()
    
    # 创建全新的调色板
    palette = QPalette()
    
    # 根据传入的主题模式应用不同的主题设置
    if mode == "System":
        # 应用系统默认主题
        app.setStyle(None)  # 清除自定义样式，使用系统默认样式
        app.setPalette(palette)  # 应用默认调色板
        app.setStyleSheet("")  # 清除应用程序级别的样式表
    elif mode == "Light":
        # 应用浅色主题
        app.setStyle(None)  # 使用系统默认样式
        
        # 设置浅色调色板
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))  # 窗口背景色
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)  # 窗口文本色
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))  # 基础背景色
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))  # 交替基础色
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 222))  # 工具提示背景色
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)  # 工具提示文本色
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)  # 文本色
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))  # 按钮背景色
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)  # 按钮文本色
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.white)  # 高亮文本色
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))  # 链接色
        palette.setColor(QPalette.ColorRole.Highlight, QColor(51, 153, 255))  # 高亮色
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)  # 高亮文本色
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(128, 128, 128))  # 占位符文本色
        
        app.setPalette(palette)  # 应用浅色调色板
        
        # 设置应用程序级别的样式表，确保浅色模式下所有控件都显示正确
        app.setStyleSheet("""
            /* 修复tooltip样式 */
            QToolTip {
                background-color: #ffffde;
                color: black;
                border: 1px solid #7953B1;
                border-radius: 4px;
                padding: 5px 10px;
            }
            
            QMessageBox {
                background-color: #ffffff;
                color: #000000;
            }
            QMessageBox QLabel {
                color: #000000;
            }
            QMessageBox QPushButton {
                background-color: #f0f0f0;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #e0e0e0;
            }
            QMessageBox QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
    elif mode == "Dark":
        # 应用深色主题
        app.setStyle(None)  # 使用系统默认样式
        
        # 设置深色主题的各种颜色
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))  # 窗口背景色
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)  # 窗口文本色
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))  # 基础背景色
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))  # 交替基础色
        # 修复tooltip样式：确保深色背景和白色文字
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(53, 53, 53))  # 工具提示背景色
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)  # 工具提示文本色
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)  # 文本色
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))  # 按钮背景色
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)  # 按钮文本色
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)  # 高亮文本色
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))  # 链接色
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))  # 高亮色
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)  # 高亮文本色
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(180, 180, 180))  # 占位符文本色
        
        app.setPalette(palette)  # 应用深色调色板
        
        # 设置应用程序级别的样式表，确保深色模式下所有控件都显示正确
        app.setStyleSheet("""
            /* 修复tooltip样式 */
            QToolTip {
                background-color: #353535;
                color: white;
                border: 1px solid #7953B1;
                border-radius: 4px;
                padding: 5px 10px;
            }
            
            QMessageBox {
                background-color: #353535;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
            QMessageBox QPushButton {
                background-color: #353535;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #454545;
            }
            QMessageBox QPushButton:pressed {
                background-color: #555555;
            }
        """)
    
    # 强制刷新所有控件，确保主题更改立即生效
    app.processEvents()
    widget_count = 0
    for widget in QApplication.allWidgets():
        widget_count += 1
        
        # 特殊处理：跳过 result_table 表格的样式设置，保持其背景颜色不变
        if isinstance(widget, QTableWidget):
            widget_name = widget.objectName() if hasattr(widget, 'objectName') else ''
            if widget_name == 'result_table':
                # 跳过 result_table 的样式设置，保持其原有的样式
                continue
        
        # 特殊处理菜单栏
        if hasattr(widget, 'objectName') and widget.objectName() == 'menuBar':
            widget.setPalette(palette)
            # 设置menuBar的样式表，根据主题模式调整背景色和文本色
            if mode == "Dark":
                widget.setStyleSheet("""
                    QMenuBar {
                        background-color: #353535;
                        color: white;
                    }
                    QMenuBar::item {
                        background-color: #353535;
                        color: white;
                    }
                    QMenuBar::item:selected {
                        background-color: #454545;
                        color: white;
                    }
                    QMenu {
                        background-color: #353535;
                        color: white;
                    }
                    QMenu::item {
                        background-color: #353535;
                        color: white;
                    }
                    QMenu::item:selected {
                        background-color: #FFC209; /* 黄色选中效果，更符合主流审美 */
                        color: black;              /* 确保选中时文字依然清晰 */
                    }
                """)
            else:  # Light 或 System 模式
                widget.setStyleSheet("""
                    QMenuBar {
                        background-color: #f0f0f0;
                        color: black;
                    }
                    QMenuBar::item {
                        background-color: #f0f0f0;
                        color: black;
                    }
                    QMenuBar::item:selected {
                        background-color: #e0e0e0;
                        color: black;
                    }
                    QMenu {
                        background-color: white;
                        color: black;
                    }
                    QMenu::item {
                        background-color: white;
                        color: black;
                    }
                    QMenu::item:selected {
                        background-color: #FFC209; /* 黄色选中效果，更符合主流审美 */
                        color: black;              /* 确保选中时文字依然清晰 */
                    }
                """)
            widget.update()
        # 特殊处理结果表格表头
        if isinstance(widget, QHeaderView):
            widget.setPalette(palette)
            # 设置QHeaderView的样式表，根据主题模式调整背景色和文本色
            if mode == "Dark":
                widget.setStyleSheet("""
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
            else:  # Light 或 System 模式
                widget.setStyleSheet("""
                    QHeaderView::section {
                        background-color: #e0e0e0;
                        color: #333333;
                        padding: 5px 8px;
                        border: none;
                        border-right: 1px solid #d0d0d0;
                        border-bottom: 1px solid #d0d0d0;
                        font-weight: bold;
                        font-size: 10pt;
                        min-height: 30px;
                    }
                    QHeaderView::section:first {
                        border-left: 1px solid #d0d0d0;
                    }
                """)
            widget.update()
        # 特殊处理QTabWidget
        if isinstance(widget, QTabWidget):
            # 确保QTabWidget及其所有子控件都应用了正确的主题属性
            widget.setProperty("theme", "light" if mode == "Light" else "dark")
            # 特殊处理QTabWidget的子控件
            for child in widget.findChildren(QWidget):
                # 特殊处理QTabBar
                if child.metaObject().className() == 'QTabBar':
                    # 为QTabBar设置主题属性，但不修改其palette，确保QTabBar::tab的颜色保持UI文件中的设定
                    child.setProperty("theme", "light" if mode == "Light" else "dark")
                    # 设置QTabBar::tab的样式，确保非选中时背景色为黄色，文字色为黑色，不跟随主题变化
                    child.setStyleSheet("""
                        /* 所有标签（默认色）：黄色 */
                        /* 注意：这里作为默认值，会被 first 和 last 覆盖 */
                        QTabBar::tab {
                            color: rgb(0, 0, 0);
                            background-color: #FFC209;
                            padding: 2px 1px;
                            min-width: 150px;
                            margin-right: 1px;
                            /* 核心修改：分别设置四个角的弧度 顺序为：左上, 右上, 右下, 左下 */
                            border-top-left-radius: 9px;
                            border-top-right-radius: 9px;
                            border-bottom-left-radius: 1px;
                            border-bottom-right-radius: 1px;
                        }
                        /* 选中状态 */
                        QTabBar::tab:selected {
                            font-weight: bold;
                            color: rgb(255, 255, 255);
                            background-color: #7953B1;
                            margin-top: 0px;
                            /* 再次明确圆角，确保不被默认样式覆盖 */
                            border-top-left-radius: 9px;
                            border-top-right-radius: 9px;
                        }
                    """)
        
        # 特殊处理四个显示控件：korean_lemma_display, english_lemma_display, english_lemmalist_display, korean_lemmalist_display
        display_widget_names = ['korean_lemma_display', 'english_lemma_display', 'english_lemmalist_display', 'korean_lemmalist_display']
        if hasattr(widget, 'objectName') and widget.objectName() in display_widget_names:
            widget.setPalette(palette)
            # 设置显示控件的样式表，根据主题模式调整背景色和文本色
            # 对于 lemmalist_display，使用更对称的 padding
            is_lemmalist = 'lemmalist_display' in widget.objectName()
            padding_value = '5px 10px' if is_lemmalist else '5px 15px'
            
            if mode == "Dark":
                widget.setStyleSheet(f"""
                    /* 默认样式 (你的基础样式) */
                    QLabel {{
                        color: #ffffff;
                        background-color: #3a3a3a;
                        border: 2px solid #7953B1;
                        border-radius: 9px;
                        padding: {padding_value};
                    }}
                    /* 拖拽悬浮时的特效样式 */
                    QLabel[active="true"] {{
                        background-color: #4a3f5e;  /* 背景变成浅紫色，暗示可放入 */
                        border: 3px solid #9b72cf;  /* 边框加粗并亮化 */
                    }}
                """)
            else:  # Light 或 System 模式
                widget.setStyleSheet(f"""
                    /* 默认样式 (你的基础样式) */
                    QLabel {{
                        color: rgb(0, 0, 0);
                        background-color: #f0f0f0;
                        border: 2px solid #7953B1;
                        border-radius: 9px;
                        padding: {padding_value};
                    }}
                    /* 拖拽悬浮时的特效样式 */
                    QLabel[active="true"] {{
                        background-color: #e0d4f7;  /* 背景变成浅紫色，暗示可放入 */
                        border: 3px solid #9b72cf;  /* 边框加粗并亮化 */
                    }}
                """)
            widget.update()
        
        # 修复深色模式下QComboBox的样式，但english_keyword_combo和korean_keyword_combo使用ui_CorpusSearchTool.py里的设定
        if isinstance(widget, QComboBox):
            # 检查控件名称，如果是关键词下拉框，则跳过自定义样式处理
            widget_name = widget.objectName() if hasattr(widget, 'objectName') else ''
            if widget_name in ['english_keyword_combo', 'korean_keyword_combo']:
                # 使用ui_CorpusSearchTool.py里的设定，不应用自定义样式
                pass
            else:
                if mode == "Dark":
                    # 修复QComboBox下拉列表和选项样式，保留UI设计中的圆角和边框样式
                    for child in widget.findChildren(QWidget):
                        if child.metaObject().className() == 'QComboBoxListView' or 'QAbstractItemView' in child.metaObject().className():
                            # 修复下拉列表背景和文字颜色，保持UI设计的圆角和边框
                            child.setStyleSheet("""
                                QAbstractItemView {
                                    background-color: #353535;
                                    border: 1px solid #7953B1;
                                    border-radius: 9px;
                                    outline: 0px;
                                }
                                QAbstractItemView::item {
                                    color: white;
                                    background-color: #353535;
                                    height: 30px;
                                    padding-left: 10px;
                                }
                                QAbstractItemView::item:hover {
                                    background-color: #454545;
                                    color: white;
                                }
                                QAbstractItemView::item:selected {
                                    background-color: #7953B1;
                                    color: white;
                                    border-radius: 5px;
                                }
                            """)
                            child.update()
                        
                    # 修复QComboBox本身的hover样式，保持与UI设计一致
                    widget.setStyleSheet("""
                        QComboBox:hover {
                            border: 2px solid #7953B1;
                        }
                        QComboBox QAbstractItemView {
                            background-color: #353535;
                            border: 1px solid #7953B1;
                            border-radius: 9px;
                            outline: 0px;
                        }
                        QComboBox QAbstractItemView::item {
                            color: white;
                            background-color: #353535;
                            height: 30px;
                            padding-left: 10px;
                        }
                        QComboBox QAbstractItemView::item:hover {
                            background-color: #454545;
                            color: white;
                        }
                        QComboBox QAbstractItemView::item:selected {
                            background-color: #7953B1;
                            color: white;
                            border-radius: 5px;
                        }
                        /* 移除下拉箭头，保持UI设计一致 */
                        QComboBox::drop-down {
                            width: 0px;
                            border: none;
                        }
                        QComboBox::down-arrow {
                            image: none;
                        }
                    """)
                else:
                    # 浅色模式下，移除我们添加的样式，恢复UI设计中的原始样式
                    widget.setStyleSheet("")
                    for child in widget.findChildren(QWidget):
                        if child.metaObject().className() == 'QComboBoxListView' or 'QAbstractItemView' in child.metaObject().className():
                            child.setStyleSheet("")
                            child.update()
                widget.update()
        # 保存当前的样式表
        current_stylesheet = widget.styleSheet()
        # 移除旧样式
        widget.style().unpolish(widget)  # 移除旧样式
        # 应用新样式
        widget.style().polish(widget)  # 应用新样式
        # 如果有样式表，重新应用它（确保样式表优先级高于调色板）
        if current_stylesheet:
            widget.setStyleSheet(current_stylesheet)
        # 更新控件
        widget.update()  # 更新控件
    
    # 再次处理事件，确保所有更新都完成
    app.processEvents()
    
    # 根据当前主题模式设置完整的样式表，包括QToolTip和QMessageBox
    if mode == "Dark":
        app.setStyleSheet("""
            QToolTip {
                background-color: #353535;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 5px;
            }
            QMessageBox {
                background-color: #353535;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
            QMessageBox QPushButton {
                background-color: #353535;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #454545;
            }
            QMessageBox QPushButton:pressed {
                background-color: #555555;
            }
        """)
    else:  # Light or System mode
        app.setStyleSheet("""
            QToolTip {
                background-color: #ffffde;
                color: black;
                border: none;
                border-radius: 4px;
                padding: 5px 5px;
            }
            QMessageBox {
                background-color: #ffffff;
                color: #000000;
            }
            QMessageBox QLabel {
                color: #000000;
            }
            QMessageBox QPushButton {
                background-color: #f0f0f0;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #e0e0e0;
            }
            QMessageBox QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
    
    # 更新所有主窗口的主题属性
    for main_window in QApplication.topLevelWidgets():
        if isinstance(main_window, QMainWindow):
            main_window.setProperty("theme", "light" if mode == "Light" else "dark")
    
    # 刷新所有控件样式，确保[theme="light"]和[theme="dark"]选择器正确应用
    refresh_all_widget_styles()
    
    # 特殊处理：更新硬编码颜色的标签（在所有模式下都执行）
    fixed_labels = 0
    for widget in QApplication.allWidgets():
        if hasattr(widget, 'objectName'):
            current_style = widget.styleSheet()
            if current_style:
                # 移除硬编码的颜色，让它跟随主题
                if 'color: rgb(0, 0, 0);' in current_style:
                    widget.setStyleSheet(current_style.replace('color: rgb(0, 0, 0);', 'color: palette(text);'))
                    fixed_labels += 1
                if 'color: white;' in current_style:
                    widget.setStyleSheet(current_style.replace('color: white;', 'color: palette(text);'))
                    fixed_labels += 1
    
    # 最后再次处理事件，确保所有更新都完成
    app.processEvents()



def refresh_all_widget_styles():
    """
    通用函数：刷新所有控件的样式，确保 [theme="light"] 和 [theme="dark"] 选择器正确应用
    """
    app = QApplication.instance()
    
    # 遍历所有控件，设置主题属性
    for widget in QApplication.allWidgets():
        # 获取当前主题模式
        # 从主窗口获取主题属性，或者默认使用浅色主题
        theme_mode = "light"
        main_window = None
        for w in QApplication.topLevelWidgets():
            if isinstance(w, QMainWindow):
                main_window = w
                break
        if main_window:
            theme_mode = main_window.property("theme") or "light"
        
        # 设置主题属性
        widget.setProperty("theme", theme_mode)
        
        # 特殊处理QComboBox：跳过english_keyword_combo和korean_keyword_combo
        if isinstance(widget, QComboBox):
            widget_name = widget.objectName() if hasattr(widget, 'objectName') else ''
            if widget_name in ['english_keyword_combo', 'korean_keyword_combo']:
                # 使用ui_CorpusSearchTool.py里的设定，不应用自定义样式
                continue
        
        # 特殊处理QTabWidget
        if isinstance(widget, QTabWidget):
            # 设置主题属性到QTabWidget
            widget.setProperty("theme", theme_mode)
            # 确保QTabWidget的所有子控件都应用了正确的主题属性
            for child in widget.findChildren(QWidget):
                # 设置主题属性到子控件
                child.setProperty("theme", theme_mode)
                # 特殊处理QTabBar
                if child.metaObject().className() == 'QTabBar':
                    # 设置QTabBar::tab的样式，确保非选中时背景色为黄色，文字色为黑色，不跟随主题变化
                    child.setStyleSheet("""
                        /* 所有标签（默认色）：黄色 */
                        /* 注意：这里作为默认值，会被 first 和 last 覆盖 */
                        QTabBar::tab {
                            color: rgb(0, 0, 0);
                            background-color: #FFC209;
                            padding: 2px 1px;
                            min-width: 150px;
                            margin-right: 1px;
                            /* 核心修改：分别设置四个角的弧度 顺序为：左上, 右上, 右下, 左下 */
                            border-top-left-radius: 9px;
                            border-top-right-radius: 9px;
                            border-bottom-left-radius: 1px;
                            border-bottom-right-radius: 1px;
                        }
                        /* 选中状态 */
                        QTabBar::tab:selected {
                            font-weight: bold;
                            color: rgb(255, 255, 255);
                            background-color: #7953B1;
                            margin-top: 0px;
                            /* 再次明确圆角，确保不被默认样式覆盖 */
                            border-top-left-radius: 9px;
                            border-top-right-radius: 9px;
                        }
                    """)
                # 移除旧样式
                child.style().unpolish(child)
                # 应用新样式
                child.style().polish(child)
                # 更新控件
                child.update()
            # 移除旧样式
            widget.style().unpolish(widget)
            # 应用新样式
            widget.style().polish(widget)
            # 更新控件
            widget.update()
        
        # 特殊处理菜单栏
        if hasattr(widget, 'objectName') and widget.objectName() == 'menuBar':
            # 根据主题模式重新设置menuBar的样式表
            if theme_mode == "dark":
                widget.setStyleSheet("""
                    QMenuBar {
                        background-color: #353535;
                        color: white;
                    }
                    QMenuBar::item {
                        background-color: #353535;
                        color: white;
                    }
                    QMenuBar::item:selected {
                        background-color: #454545;
                        color: white;
                    }
                    QMenu {
                        background-color: #353535;
                        color: white;
                    }
                    QMenu::item {
                        background-color: #353535;
                        color: white;
                    }
                    QMenu::item:selected {
                        background-color: #FFC209; /* 黄色选中效果，更符合主流审美 */
                        color: black;              /* 确保选中时文字依然清晰 */
                    }
                """)
            else:  # light 模式
                widget.setStyleSheet("""
                    QMenuBar {
                        background-color: #f0f0f0;
                        color: black;
                    }
                    QMenuBar::item {
                        background-color: #f0f0f0;
                        color: black;
                    }
                    QMenuBar::item:selected {
                        background-color: #e0e0e0;
                        color: black;
                    }
                    QMenu {
                        background-color: white;
                        color: black;
                    }
                    QMenu::item {
                        background-color: white;
                        color: black;
                    }
                    QMenu::item:selected {
                        background-color: #FFC209; /* 黄色选中效果，更符合主流审美 */
                        color: black;              /* 确保选中时文字依然清晰 */
                    }
                """)
        
        # 移除旧样式
        widget.style().unpolish(widget)
        # 应用新样式
        widget.style().polish(widget)
        
        # 更新控件
        widget.update()
    
    # 处理事件，确保所有更改都生效
    app.processEvents()


def update_widget_theme_properties(widget, theme_mode):
    """
    更新指定控件及其所有子控件的主题属性
    
    Args:
        widget: 要更新的控件
        theme_mode: 主题模式，可选值: "light" 或 "dark"
    """
    # 设置控件的主题属性
    widget.setProperty("theme", theme_mode)
    
    # 递归更新所有子控件
    for child in widget.findChildren(QWidget):
        child.setProperty("theme", theme_mode)
        # 移除旧样式
        child.style().unpolish(child)
        # 应用新样式
        child.style().polish(child)
        # 更新控件
        child.update()
    
    # 特殊处理QTabWidget：确保其QTabBar也应用了正确的主题
    if isinstance(widget, QTabWidget):
        # 直接访问QTabBar并应用主题
        tab_bar = widget.tabBar()
        if tab_bar:
            tab_bar.setProperty("theme", theme_mode)
            tab_bar.style().unpolish(tab_bar)
            tab_bar.style().polish(tab_bar)
            tab_bar.update()
    
    # 移除旧样式
    widget.style().unpolish(widget)
    # 应用新样式
    widget.style().polish(widget)
    # 更新控件
    widget.update()
