"""
GUI主窗口模块
实现应用程序的主界面和用户交互功能
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from function.config_manager import config_manager
from function.search_engine import search_engine
from function.result_processor import result_processor
from function.result_exporter import result_exporter
from function.search_history_manager import search_history_manager
from function.file_drag_drop import enable_drag_drop_for_window
import fnmatch


class MainWindow:
    """主窗口类"""
    
    def __init__(self):
        """初始化主窗口"""
        # 尝试使用tkinterdnd2创建窗口以支持拖拽
        try:
            import tkinterdnd2
            self.root = tkinterdnd2.Tk()
        except ImportError:
            print("提示：安装tkinterdnd2以获得更好的拖拽支持")
            print("运行: pip install tkinterdnd2")
            self.root = tk.Tk()

        self.root.title("字幕语料库检索工具")
        self.root.iconbitmap()  # 设置图标（如果有的话）

        # 设置整体背景颜色
        self.root.configure(bg='#1f1f1f')

        # 加载配置
        self.load_window_settings()

        # 设置窗口属性
        self.setup_window()

        # 创建界面元素
        self.create_widgets()

        # 绑定事件
        self.bind_events()

        # 初始化文件选择器
        self.init_file_drag_drop()
    
    def load_window_settings(self):
        """加载窗口设置"""
        self.ui_settings = config_manager.get_ui_settings()
    
    def setup_window(self):
        """设置窗口属性"""
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 获取配置的窗口尺寸
        window_width = self.ui_settings['width']
        window_height = self.ui_settings['height']
        
        # 计算窗口位置
        if self.ui_settings['x'] == -1 or self.ui_settings['y'] == -1:
            # 居中显示
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
        else:
            x = self.ui_settings['x']
            y = self.ui_settings['y']
        
        # 设置窗口大小和位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 设置最小窗口尺寸
        self.root.minsize(600, 400)
        
        # 设置窗口协议
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 创建菜单栏
        self.create_menu()

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="导出结果(CSV)", command=self.export_to_csv)
        file_menu.add_command(label="导出结果(TXT)", command=self.export_to_txt)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_closing)

        # 搜索菜单
        search_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="搜索", menu=search_menu)
        search_menu.add_command(label="搜索历史", command=self.show_search_history)
        search_menu.add_command(label="导出历史(Markdown)", command=self.export_search_history_md)
        search_menu.add_command(label="清除历史", command=self.clear_search_history)

    def create_widgets(self):
        """创建界面元素"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建输入区域
        self.create_input_section(main_frame)
        
        # 创建搜索区域
        self.create_search_section(main_frame)
        
        # 创建结果区域
        self.create_result_section(main_frame)
        
        # 创建状态栏
        self.create_status_bar()
    
    def create_input_section(self, parent):
        """创建输入区域"""
        input_frame = ttk.LabelFrame(parent, text="输入设置", padding=(10, 5))
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 输入文件/文件夹选择
        ttk.Label(input_frame, text="输入路径:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.input_path_var = tk.StringVar(value=config_manager.get_input_dir())
        self.input_path_entry = ttk.Entry(input_frame, textvariable=self.input_path_var, width=50)
        self.input_path_entry.grid(row=0, column=1, sticky=tk.EW, padx=(0, 5))
        ttk.Button(input_frame, text="浏览", command=self.browse_input_path).grid(row=0, column=2)
        
        # 输出文件夹选择
        ttk.Label(input_frame, text="输出路径:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.output_path_var = tk.StringVar(value=config_manager.get_output_dir())
        self.output_path_entry = ttk.Entry(input_frame, textvariable=self.output_path_var, width=50)
        self.output_path_entry.grid(row=1, column=1, sticky=tk.EW, padx=(0, 5), pady=(5, 0))
        ttk.Button(input_frame, text="浏览", command=self.browse_output_path).grid(row=1, column=2, pady=(5, 0))
        
        # 配置行权重
        input_frame.columnconfigure(1, weight=1)
    
    def create_search_section(self, parent):
        """创建搜索区域"""
        search_frame = ttk.LabelFrame(parent, text="搜索设置", padding=(10, 5))
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 关键词输入
        ttk.Label(search_frame, text="关键词:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.keyword_var = tk.StringVar()
        self.keyword_entry = ttk.Entry(search_frame, textvariable=self.keyword_var, width=50)
        self.keyword_entry.grid(row=0, column=1, sticky=tk.EW, padx=(0, 5))
        self.keyword_entry.bind('<Return>', lambda event: self.start_search())
        
        # 搜索按钮
        self.search_button = ttk.Button(search_frame, text="开始搜索", command=self.start_search)
        self.search_button.grid(row=0, column=2)
        
        # 搜索选项
        options_frame = ttk.Frame(search_frame)
        options_frame.grid(row=1, column=0, columnspan=3, sticky=tk.EW, pady=(10, 0))
        
        self.case_sensitive_var = tk.BooleanVar(value=config_manager.get_search_settings()['case_sensitive'])
        self.fuzzy_match_var = tk.BooleanVar(value=config_manager.get_search_settings()['fuzzy_match'])
        self.regex_var = tk.BooleanVar(value=config_manager.get_search_settings()['regex_enabled'])
        
        ttk.Checkbutton(options_frame, text="区分大小写", variable=self.case_sensitive_var).pack(side=tk.LEFT)
        ttk.Checkbutton(options_frame, text="模糊匹配", variable=self.fuzzy_match_var).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Checkbutton(options_frame, text="正则表达式", variable=self.regex_var).pack(side=tk.LEFT, padx=(10, 0))
        
        # 配置行权重
        search_frame.columnconfigure(1, weight=1)
    
    def create_result_section(self, parent):
        """创建结果区域"""
        result_frame = ttk.LabelFrame(parent, text="搜索结果", padding=(10, 5))
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建树形视图
        columns = ('文件名', '行号', '集数', '时间轴', '内容')
        self.tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)

        # 设置列标题
        for col in columns:
            self.tree.heading(col, text=col)
            if col == '内容':
                self.tree.column(col, width=300)  # 内容列更宽
            elif col == '时间轴':
                self.tree.column(col, width=60, anchor='center')  # 时间轴列，居中显示
            elif col == '行号':
                self.tree.column(col, width=40)  # 行号列，刚好显示1234567
            elif col == '集数':
                self.tree.column(col, width=160)  # 集数列，增加宽度
            else:
                self.tree.column(col, width=120)  # 文件名列，增加宽度

        # 配置样式
        self.style = ttk.Style()
        self.style.theme_use('default')

        # 配置Treeview样式
        self.style.configure('Treeview',
                           background='#1f1f1f',  # 背景颜色
                           foreground='white',    # 文字颜色
                           fieldbackground='#1f1f1f',
                           rowheight=25)

        # 配置选中行的样式
        self.style.map('Treeview',
                      background=[('selected', '#3a3a3a')],
                      foreground=[('selected', 'white')])

        # 配置Treeview Heading样式
        self.style.configure('Treeview.Heading',
                           background='#2d2d2d',
                           foreground='white',
                           font=('TkDefaultFont', 9, 'bold'))
        
        # 添加滚动条
        v_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(result_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # 创建右键菜单
        self.create_context_menu()

        # 绑定右键点击事件
        self.tree.bind("<Button-3>", self.show_context_menu)  # Windows/Linux
        self.tree.bind("<Button-2>", self.show_context_menu)  # macOS (有时右键是Button-2)

        # 有些系统可能需要使用<ButtonRelease-3>来确保选择已更新
        self.tree.bind("<ButtonRelease-3>", self.show_context_menu)

        # 绑定键盘快捷键
        self.tree.bind("<Control-a>", self.select_all_items)
        self.tree.bind("<Control-c>", self.copy_selected_items)

        # 确保Treeview可以获得焦点以响应键盘事件
        self.tree.focus_set()

        # 布局
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        v_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        h_scrollbar.grid(row=1, column=0, sticky=tk.EW)

        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
    
    def create_context_menu(self):
        """创建右键菜单"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="复制选中行", command=self.copy_selected_row)
        self.context_menu.add_command(label="复制全部结果", command=self.copy_all_results)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="导出选中行", command=self.export_selected_rows)
        self.context_menu.add_command(label="导出为Markdown", command=self.export_results_markdown)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="清除结果", command=self.clear_results)

    def show_context_menu(self, event):
        """显示右键菜单"""
        try:
            # 获取点击位置的行
            item = self.tree.identify_row(event.y)
            if item:
                # 检查是否按住Ctrl键进行多选
                if self.root.focus_get() and self.root.focus_get() == self.tree:
                    # 不取消现有的选择，保持多选状态
                    if item not in self.tree.selection():
                        # 如果点击的行不在当前选择中，添加到选择中
                        self.tree.selection_add(item)
                else:
                    # 如果没有多选，选择当前行
                    self.tree.selection_set(item)
            else:
                # 如果没有点击到具体行，保持当前选择
                pass

            # 显示菜单
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def copy_selected_row(self):
        """复制选中行到剪贴板"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("提示", "请先选择要复制的行")
            return

        # 获取所有选中行的数据
        all_rows_text = []
        for item in selection:
            item_values = self.tree.item(item)['values']
            # 将数据格式化为制表符分隔的字符串
            row_text = '\t'.join(str(v) for v in item_values)
            all_rows_text.append(row_text)

        # 将所有选中行合并为一个字符串
        combined_text = '\n'.join(all_rows_text)

        # 复制到剪贴板
        self.root.clipboard_clear()
        self.root.clipboard_append(combined_text)
        self.status_var.set(f"已复制 {len(selection)} 行到剪贴板")

    def copy_all_results(self):
        """复制所有结果到剪贴板"""
        items = self.tree.get_children()
        if not items:
            messagebox.showinfo("提示", "没有结果可复制")
            return

        all_text = ""
        for item in items:
            item_values = self.tree.item(item)['values']
            row_text = '\t'.join(str(v) for v in item_values)
            all_text += row_text + '\n'

        # 复制到剪贴板
        self.root.clipboard_clear()
        self.root.clipboard_append(all_text.rstrip('\n'))
        self.status_var.set("已复制所有结果到剪贴板")

    def select_all_items(self, event=None):
        """全选所有项目"""
        # 获取所有项目并选择它们
        for item in self.tree.get_children():
            self.tree.selection_add(item)
        return "break"  # 防止事件传播

    def copy_selected_items(self, event=None):
        """复制选中的项目到剪贴板"""
        selection = self.tree.selection()
        if not selection:
            # 如果没有选中任何项目，复制所有项目
            items = self.tree.get_children()
        else:
            items = selection

        if not items:
            messagebox.showinfo("提示", "没有结果可复制")
            return

        all_text = ""
        for item in items:
            item_values = self.tree.item(item)['values']
            row_text = '\t'.join(str(v) for v in item_values)
            all_text += row_text + '\n'

        # 复到剪贴板
        self.root.clipboard_clear()
        self.root.clipboard_append(all_text.rstrip('\n'))
        self.status_var.set(f"已复制 {len(items)} 个项目到剪贴板")
        return "break"  # 防止事件传播

    def copy_all_results(self):
        """复制所有结果到剪贴板"""
        items = self.tree.get_children()
        if not items:
            messagebox.showinfo("提示", "没有结果可复制")
            return

        all_text = ""
        for item in items:
            item_values = self.tree.item(item)['values']
            row_text = '\t'.join(str(v) for v in item_values)
            all_text += row_text + '\n'

        # 复制到剪贴板
        self.root.clipboard_clear()
        self.root.clipboard_append(all_text.rstrip('\n'))
        self.status_var.set("已复制所有结果到剪贴板")

    def select_all_items(self, event=None):
        """全选所有项目"""
        # 获取所有项目并选择它们
        for item in self.tree.get_children():
            self.tree.selection_add(item)
        return "break"  # 防止事件传播

    def copy_selected_items(self, event=None):
        """复制选中的项目到剪贴板"""
        selection = self.tree.selection()
        if not selection:
            # 如果没有选中任何项目，复制所有项目
            items = self.tree.get_children()
        else:
            items = selection

        if not items:
            messagebox.showinfo("提示", "没有结果可复制")
            return

        all_text = ""
        for item in items:
            item_values = self.tree.item(item)['values']
            row_text = '\t'.join(str(v) for v in item_values)
            all_text += row_text + '\n'

        # 复到剪贴板
        self.root.clipboard_clear()
        self.root.clipboard_append(all_text.rstrip('\n'))
        self.status_var.set(f"已复制 {len(items)} 个项目到剪贴板")
        return "break"  # 防止事件传播

    def export_selected_rows(self):
        """导出选中行"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("提示", "请先选择要导出的行")
            return

        output_dir = self.output_path_var.get()
        if not output_dir:
            output_dir = filedialog.askdirectory(title="选择导出目录")
            if not output_dir:
                return

        try:
            # 获取选中行的数据
            selected_results = []
            for item in selection:
                item_values = self.tree.item(item)['values']
                selected_results.append(item_values)

            # 使用结果导出器导出
            result_exporter.export_to_csv(selected_results, output_dir, "selected_results.csv")
            messagebox.showinfo("成功", f"选中结果已导出到 {output_dir}/selected_results.csv")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

    def export_results_markdown(self):
        """导出结果为Markdown格式"""
        items = self.tree.get_children()
        if not items:
            messagebox.showinfo("提示", "没有结果可导出")
            return

        output_dir = self.output_path_var.get()
        if not output_dir:
            output_dir = filedialog.askdirectory(title="选择导出目录")
            if not output_dir:
                return

        try:
            # 获取所有结果的数据
            all_results = []
            for item in items:
                item_values = self.tree.item(item)['values']
                all_results.append(item_values)

            # 创建Markdown格式的输出
            md_content = "# 搜索结果\n\n"
            md_content += f"关键词: {self.keyword_var.get()}\n"
            md_content += f"搜索时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

            # 添加表格头部
            headers = ['文件名', '时间轴', '行号', '集数', '内容']
            md_content += "| " + " | ".join(headers) + " |\n"
            md_content += "| " + " | ".join(['---'] * len(headers)) + " |\n"

            # 添加数据行
            for row in all_results:
                # 确保行数据长度与表头一致
                row_list = list(row)
                if len(row_list) < len(headers):
                    # 如果行数据不足，用空字符串填充
                    row_list.extend([''] * (len(headers) - len(row_list)))
                elif len(row_list) > len(headers):
                    # 如果行数据过多，截断到合适长度
                    row_list = row_list[:len(headers)]

                md_content += "| " + " | ".join(str(cell) for cell in row_list) + " |\n"

            # 写入文件
            output_file = f"{output_dir}/search_results.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(md_content)

            messagebox.showinfo("成功", f"结果已导出到 {output_file}")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

    def clear_results(self):
        """清除结果"""
        if messagebox.askyesno("确认", "确定要清除所有搜索结果吗？"):
            # 清空结果表格
            for item in self.tree.get_children():
                self.tree.delete(item)

            self.status_var.set("结果已清除")

    def create_status_bar(self):
        """创建状态栏"""
        self.status_var = tk.StringVar(value="准备就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def bind_events(self):
        """绑定事件"""
        # 绑定窗口大小变化事件
        self.root.bind('<Configure>', self.on_window_resize)

    def init_file_drag_drop(self):
        """初始化文件拖拽功能"""
        # 使用增强的拖拽模块
        self.drag_drop_handler = enable_drag_drop_for_window(self.root, self.on_files_dropped)

    def on_files_dropped(self, files):
        """处理拖放的文件"""
        if not files:
            return

        # 获取第一个文件或目录作为输入路径
        first_file = files[0]

        # 如果是目录，则设置为输入目录
        if os.path.isdir(first_file):
            self.input_path_var.set(first_file)
        else:
            # 如果是文件，设置为其所在目录
            self.input_path_var.set(os.path.dirname(first_file))

        # 如果只有一个文件且是支持的格式，也可以直接填入关键词
        if len(files) == 1:
            filename = os.path.basename(first_file)
            # 提取文件名（不含扩展名）作为可能的搜索关键词
            name_without_ext = os.path.splitext(filename)[0]
            if not self.keyword_var.get():  # 如果关键词框为空
                self.keyword_var.set(name_without_ext)
    
    def browse_input_path(self):
        """浏览输入路径"""
        # 询问用户是要选择文件还是目录
        choice = messagebox.askquestion("选择输入", "请选择输入类型",
                                       detail="是选择单个文件还是整个目录？\n\n选择“是”选择目录，选择“否”选择文件")

        if choice == 'yes':  # 选择目录
            path = filedialog.askdirectory(initialdir=self.input_path_var.get())
            if path:
                self.input_path_var.set(path)
                self.status_var.set(f"已选择目录: {os.path.basename(path)}")
        else:  # 选择文件
            files = filedialog.askopenfilenames(
                title="选择输入文件",
                initialdir=os.path.dirname(self.input_path_var.get()) if os.path.isfile(self.input_path_var.get()) else self.input_path_var.get(),
                filetypes=[
                    ("支持的文件", "*.srt *.ass *.ssa *.vtt *.txt *.md *.docx *.pdf"),
                    ("字幕文件", "*.srt *.ass *.ssa *.vtt"),
                    ("文档文件", "*.txt *.md *.docx *.pdf"),
                    ("所有文件", "*.*")
                ]
            )
            if files:
                # 如果选择了多个文件，显示文件数量和第一个文件的目录
                if len(files) > 1:
                    dir_path = os.path.dirname(files[0])
                    self.input_path_var.set(dir_path)
                    self.status_var.set(f"已选择 {len(files)} 个文件，目录: {os.path.basename(dir_path)}")
                else:
                    file_path = files[0]
                    self.input_path_var.set(file_path)
                    self.status_var.set(f"已选择文件: {os.path.basename(file_path)}")

    def browse_output_path(self):
        """浏览输出路径"""
        path = filedialog.askdirectory(initialdir=self.output_path_var.get())
        if path:
            self.output_path_var.set(path)
            self.status_var.set(f"已选择输出目录: {os.path.basename(path)}")

    def on_files_dropped(self, files):
        """处理拖放的文件"""
        if not files:
            return

        # 获取第一个文件或目录作为输入路径
        first_file = files[0]

        # 如果是目录，则设置为输入目录
        if os.path.isdir(first_file):
            self.input_path_var.set(first_file)
            self.status_var.set(f"已通过拖拽选择目录: {os.path.basename(first_file)}")
        else:
            # 如果是文件，设置为其所在目录
            dir_path = os.path.dirname(first_file)
            self.input_path_var.set(dir_path)
            self.status_var.set(f"已通过拖拽选择 {len(files)} 个文件，目录: {os.path.basename(dir_path)}")

        # 如果只有一个文件且是支持的格式，也可以直接填入关键词
        if len(files) == 1:
            filename = os.path.basename(first_file)
            # 提取文件名（不含扩展名）作为可能的搜索关键词
            name_without_ext = os.path.splitext(filename)[0]
            if not self.keyword_var.get():  # 如果关键词框为空
                self.keyword_var.set(name_without_ext)
    
    def start_search(self):
        """开始搜索"""
        # 获取输入参数
        input_path = self.input_path_var.get()
        output_path = self.output_path_var.get()
        keywords = self.keyword_var.get().strip()
        
        # 验证输入
        if not input_path:
            messagebox.showerror("错误", "请输入输入路径")
            return
        
        if not keywords:
            messagebox.showerror("错误", "请输入关键词")
            return
        
        # 更新配置
        config_manager.set_input_dir(input_path)
        config_manager.set_output_dir(output_path)
        config_manager.set_search_settings(
            case_sensitive=self.case_sensitive_var.get(),
            fuzzy_match=self.fuzzy_match_var.get(),
            regex_enabled=self.regex_var.get()
        )
        
        # 禁用搜索按钮
        self.search_button.config(state='disabled')
        self.status_var.set("正在搜索...")
        
        # 在新线程中执行搜索
        search_thread = threading.Thread(target=self.perform_search, args=(input_path, keywords))
        search_thread.daemon = True
        search_thread.start()
    
    def perform_search(self, input_path, keywords):
        """执行搜索操作"""
        try:
            # 获取搜索设置
            case_sensitive = self.case_sensitive_var.get()
            fuzzy_match = self.fuzzy_match_var.get()
            regex_enabled = self.regex_var.get()

            # 获取所有支持的文件
            supported_extensions = ['.srt', '.ass', '.ssa', '.vtt', '.txt', '.md', '.docx', '.pdf']
            files_to_search = []

            if os.path.isfile(input_path):
                # 单个文件
                files_to_search.append(input_path)
            elif os.path.isdir(input_path):
                # 目录，遍历所有支持的文件
                for root, dirs, files in os.walk(input_path):
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in supported_extensions):
                            files_to_search.append(os.path.join(root, file))
            else:
                raise ValueError("输入路径无效")

            # 检查是否需要韩语/英语变形匹配
            # 如果关键词包含韩语字符，启用变形匹配
            import re
            korean_pattern = re.compile(r'[\uac00-\ud7af]')
            contains_korean = bool(korean_pattern.search(keywords))

            if contains_korean and not regex_enabled:
                # 使用韩语变形匹配功能
                results = []
                for file_path in files_to_search:
                    file_results = search_engine.search_korean_english_variants(
                        file_path,
                        keywords.split(),  # 将关键词按空格分割
                        case_sensitive=case_sensitive
                    )
                    results.extend(file_results)
            else:
                # 执行常规搜索
                results = search_engine.search_in_files(
                    files_to_search,
                    keywords.split(),  # 将关键词按空格分割
                    case_sensitive=case_sensitive,
                    fuzzy_match=fuzzy_match,
                    regex_enabled=regex_enabled
                )

            # 处理结果以供显示
            # 判断结果是否包含时间轴信息来决定文件类型
            has_time_axis = any('time_axis' in result and result.get('time_axis', 'N/A') != 'N/A' for result in results)
            file_type = 'subtitle' if has_time_axis else 'document'
            formatted_results = result_processor.format_results_for_display(results, file_type)

            # 在主线程中更新UI
            self.root.after(0, self.update_results, formatted_results)
        except Exception as e:
            self.root.after(0, self.handle_search_error, str(e))
    
    def update_results(self, results):
        """更新搜索结果"""
        # 清空现有结果
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加新结果
        for result in results:
            self.tree.insert('', tk.END, values=result)
        
        # 更新状态
        self.status_var.set(f"搜索完成，找到 {len(results)} 条结果")
        self.search_button.config(state='normal')
    
    def handle_search_error(self, error_msg):
        """处理搜索错误"""
        messagebox.showerror("搜索错误", f"搜索过程中发生错误：\n{error_msg}")
        self.status_var.set("搜索失败")
        self.search_button.config(state='normal')
    
    def on_window_resize(self, event):
        """窗口大小改变事件"""
        # 只处理主窗口的resize事件
        if event.widget == self.root:
            # 保存窗口设置
            pos_x = self.root.winfo_x()
            pos_y = self.root.winfo_y()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            
            config_manager.set_ui_settings(width, height, pos_x, pos_y)
    
    def on_closing(self):
        """窗口关闭事件"""
        # 保存配置
        config_manager.set_input_dir(self.input_path_var.get())
        config_manager.set_output_dir(self.output_path_var.get())
        config_manager.set_search_settings(
            case_sensitive=self.case_sensitive_var.get(),
            fuzzy_match=self.fuzzy_match_var.get(),
            regex_enabled=self.regex_var.get()
        )
        
        # 保存配置到文件
        config_manager.save_config()
        
        # 销毁窗口
        self.root.destroy()
    
    def run(self):
        """运行应用程序"""
        # 使用withdraw方法隐藏窗口，然后居中显示，避免闪烁
        self.root.withdraw()
        self.root.update_idletasks()

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 获取当前窗口尺寸
        self.root.update_idletasks()  # 确保窗口尺寸已更新
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # 如果窗口尺寸未设置，默认为800x600
        if window_width <= 1:
            window_width = 800
        if window_height <= 1:
            window_height = 600

        # 计算窗口位置
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # 设置窗口位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 重新显示窗口
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        # 启动主循环
        self.root.mainloop()

    def export_to_csv(self):
        """导出结果到CSV文件"""
        if not self.tree.get_children():
            messagebox.showwarning("警告", "没有结果可以导出")
            return

        output_dir = self.output_path_var.get()
        if not output_dir:
            output_dir = filedialog.askdirectory(title="选择导出目录")
            if not output_dir:
                return

        try:
            # 获取当前显示的所有结果
            results = []
            for child in self.tree.get_children():
                values = self.tree.item(child)['values']
                results.append(values)

            # 使用结果导出器导出
            result_exporter.export_to_csv(results, output_dir)
            messagebox.showinfo("成功", f"结果已导出到 {output_dir}/search_results.csv")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

    def export_to_txt(self):
        """导出结果到TXT文件"""
        if not self.tree.get_children():
            messagebox.showwarning("警告", "没有结果可以导出")
            return

        output_dir = self.output_path_var.get()
        if not output_dir:
            output_dir = filedialog.askdirectory(title="选择导出目录")
            if not output_dir:
                return

        try:
            # 获取当前显示的所有结果
            results = []
            for child in self.tree.get_children():
                values = self.tree.item(child)['values']
                results.append(values)

            # 使用结果导出器导出
            result_exporter.export_to_txt(results, output_dir)
            messagebox.showinfo("成功", f"结果已导出到 {output_dir}/search_results.txt")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

    def __init__(self):
        """初始化主窗口"""
        # 尝试使用tkinterdnd2创建窗口以支持拖拽
        try:
            import tkinterdnd2
            self.root = tkinterdnd2.Tk()
        except ImportError:
            print("提示：安装tkinterdnd2以获得更好的拖拽支持")
            print("运行: pip install tkinterdnd2")
            self.root = tk.Tk()

        self.root.title("字幕语料库检索工具")
        self.root.iconbitmap()  # 设置图标（如果有的话）

        # 设置整体背景颜色
        self.root.configure(bg='#1f1f1f')

        # 初始化历史窗口引用
        self.history_window = None

        # 加载配置
        self.load_window_settings()

        # 设置窗口属性
        self.setup_window()

        # 创建界面元素
        self.create_widgets()

        # 绑定事件
        self.bind_events()

        # 初始化文件选择器
        self.init_file_drag_drop()

    def show_search_history(self):
        """显示搜索历史（只允许打开一个窗口）"""
        # 检查是否已有历史窗口打开
        if self.history_window and self.history_window.winfo_exists():
            # 如果窗口存在，将其带到前台
            self.history_window.lift()
            self.history_window.focus_force()
            return

        # 获取最近的搜索记录
        recent_records = search_history_manager.get_recent_records(10)

        if not recent_records:
            messagebox.showinfo("搜索历史", "暂无搜索历史")
            return

        # 创建历史记录窗口
        self.history_window = tk.Toplevel(self.root)
        self.history_window.title("搜索历史")

        # 实现优雅的居中加载
        self.center_window(self.history_window, 700, 400)

        # 创建树形视图显示历史记录
        tree = ttk.Treeview(self.history_window, columns=('Keywords', 'Time', 'Input Path'), show='headings')
        tree.heading('Keywords', text='关键词')
        tree.heading('Time', text='时间')
        tree.heading('Input Path', text='输入路径')

        # 设置列宽
        tree.column('Keywords', width=150)  # 与时间列宽度相同
        tree.column('Time', width=150)
        tree.column('Input Path', width=350)  # 增加输入路径列宽度

        # 添加滚动条
        v_scrollbar = ttk.Scrollbar(self.history_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=v_scrollbar.set)

        # 添加历史记录到树形视图
        for record in recent_records:
            timestamp = record['timestamp'][:19].replace('T', ' ')  # 格式化时间
            tree.insert('', tk.END, values=(record['keywords'], timestamp, record['input_path']))

        # 创建右键菜单
        context_menu = tk.Menu(self.history_window, tearoff=0)
        context_menu.add_command(label="清除选定条目", command=lambda: self.clear_selected_history(tree))
        context_menu.add_command(label="清除所有历史", command=self.clear_all_history)

        # 绑定右键点击事件
        def show_context_menu(event):
            try:
                # 选择被右键点击的行
                item = tree.identify_row(event.y)
                if item:
                    tree.selection_set(item)

                # 显示菜单
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()

        # 绑定双击事件
        def on_double_click(event):
            item = tree.identify('item', event.x, event.y)
            if item:
                values = tree.item(item, 'values')
                if values:
                    keyword = values[0]  # 关键词在第一列
                    # 将关键词载入主界面的关键词输入框
                    self.keyword_var.set(keyword)
                    # 关闭历史窗口
                    self.history_window.destroy()
                    self.history_window = None  # 重置引用

        tree.bind("<Double-1>", on_double_click)

        # 绑定右键菜单事件
        tree.bind("<Button-3>", show_context_menu)  # Windows/Linux
        tree.bind("<Button-2>", show_context_menu)  # macOS (有时右键是Button-2)

        # 当窗口被关闭时重置引用
        self.history_window.protocol("WM_DELETE_WINDOW", self.close_history_window)

        # 布局
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def clear_selected_history(self, tree):
        """清除选定的历史记录"""
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选择要清除的条目")
            return

        if not messagebox.askyesno("确认", f"确定要清除选中的 {len(selected_items)} 条历史记录吗？"):
            return

        # 获取选定项的关键词
        keywords_to_remove = []
        for item in selected_items:
            values = tree.item(item, 'values')
            if values:
                keywords_to_remove.append(values[0])  # 关键词在第一列

        # 从历史记录中移除选定的条目
        search_history_manager.remove_records_by_keywords(keywords_to_remove)

        # 重新加载历史记录显示
        self.refresh_history_window(tree)

    def refresh_history_window(self, tree):
        """刷新历史记录窗口"""
        # 清空当前显示
        for item in tree.get_children():
            tree.delete(item)

        # 获取更新后的历史记录
        recent_records = search_history_manager.get_recent_records(10)

        if not recent_records:
            messagebox.showinfo("搜索历史", "暂无搜索历史")
            # 不要在这里关闭窗口，因为可能还有其他操作需要进行
            return

        # 添加历史记录到树形视图
        for record in recent_records:
            timestamp = record['timestamp'][:19].replace('T', ' ')  # 格式化时间
            tree.insert('', tk.END, values=(record['keywords'], timestamp, record['input_path']))

    def clear_all_history(self):
        """清除所有历史记录"""
        if messagebox.askyesno("确认", "确定要清除所有搜索历史吗？"):
            search_history_manager.clear_history()
            messagebox.showinfo("成功", "所有搜索历史已清除")

            # 如果历史窗口存在，关闭它
            if self.history_window:
                self.history_window.destroy()
                self.history_window = None

    def close_history_window(self):
        """关闭历史窗口并重置引用"""
        if self.history_window:
            self.history_window.destroy()
            self.history_window = None

    def center_window(self, window, width, height):
        """居中显示窗口，实现优雅加载"""
        # 获取屏幕尺寸
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # 计算窗口位置
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # 设置窗口大小和位置
        window.geometry(f"{width}x{height}+{x}+{y}")

        # 使用withdraw方法隐藏窗口，然后居中显示，避免闪烁
        window.withdraw()
        window.update_idletasks()

        # 重新显示窗口
        window.deiconify()
        window.lift()
        window.focus_force()

    def clear_search_history(self):
        """清除搜索历史"""
        if messagebox.askyesno("确认", "确定要清除所有搜索历史吗？"):
            search_history_manager.clear_history()
            messagebox.showinfo("成功", "搜索历史已清除")

    def export_search_history_md(self):
        """导出搜索历史为Markdown格式"""
        output_dir = filedialog.askdirectory(title="选择导出目录")
        if not output_dir:
            return

        try:
            search_history_manager.export_to_markdown(output_dir)
            messagebox.showinfo("成功", f"搜索历史已导出到 {output_dir}/search_history.md")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

    def update_results(self, results):
        """更新搜索结果"""
        # 清空现有结果
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 添加新结果
        for result in results:
            # 如果需要高亮关键词，可以在这里处理
            # 由于tkinter Treeview不直接支持富文本，我们暂时保持原样
            # 但可以为将来扩展预留接口
            self.tree.insert('', tk.END, values=result)

        # 更新状态
        self.status_var.set(f"搜索完成，找到 {len(results)} 条结果")
        self.search_button.config(state='normal')

        # 添加到搜索历史
        search_history_manager.add_record(
            keywords=self.keyword_var.get(),
            input_path=self.input_path_var.get(),
            output_path=self.output_path_var.get(),
            case_sensitive=self.case_sensitive_var.get(),
            fuzzy_match=self.fuzzy_match_var.get(),
            regex_enabled=self.regex_var.get()
        )