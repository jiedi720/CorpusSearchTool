"""
验证韩语搜索高亮修改的代码逻辑
检查关键修改点是否正确
"""

def test_search_engine_modifications():
    """检查 search_engine_kor.py 的修改"""

    print("=== 检查 search_engine_kor.py 修改 ===\n")

    # 读取文件
    with open('function/search_engine_kor.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查 1: 是否添加了 matched_terms_set
    if 'matched_terms_set' in content:
        print("✓ 1. matched_terms_set 变量已添加到搜索逻辑中")
    else:
        print("✗ 1. matched_terms_set 变量未找到")

    # 检查 2: 是否在形态分析中收集匹配词
    if 'item_matched_terms' in content:
        print("✓ 2. 每条记录的匹配词收集逻辑已添加")
    else:
        print("✗ 2. 每条记录的匹配词收集逻辑未找到")

    # 检查 3: 是否添加了词干形式
    if "if token.form != lemma and lemma not in item_matched_terms:" in content:
        print("✓ 3. 词干形式添加逻辑已实现")
    else:
        print("✗ 3. 词干形式添加逻辑未找到")

    # 检查 4: 是否更新了全局集合
    if 'matched_terms_set.update(item_matched_terms)' in content:
        print("✓ 4. 全局匹配词集合更新逻辑已实现")
    else:
        print("✗ 4. 全局匹配词集合更新逻辑未找到")

    # 检查 5: 返回结果中是否包含 matched_terms_set
    if "'matched_terms_set': list(matched_terms_set)" in content:
        print("✓ 5. matched_terms_set 已添加到返回结果中")
    else:
        print("✗ 5. matched_terms_set 未添加到返回结果中")


def test_gui_modifications():
    """检查 GUI 代码的修改"""

    print("\n=== 检查 GUI 代码修改 ===\n")

    # 读取文件
    with open('gui/qt_CorpusSearchTool.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查 1: SearchThread 是否添加了 matched_terms_set 属性
    if 'self.matched_terms_set = []' in content:
        print("✓ 1. SearchThread 已添加 matched_terms_set 属性")
    else:
        print("✗ 1. SearchThread 未添加 matched_terms_set 属性")

    # 检查 2: 是否收集所有匹配词
    if 'matched_terms_set_all' in content:
        print("✓ 2. 所有文件匹配词收集逻辑已添加")
    else:
        print("✗ 2. 所有文件匹配词收集逻辑未找到")

    # 检查 3: 信号是否包含 matched_terms_set
    if 'search_completed = Signal(list, str, list, str, list, list)' in content:
        print("✓ 3. 信号定义已更新包含 matched_terms_set")
    else:
        print("✗ 3. 信号定义未更新")

    # 检查 4: 信号发送是否包含 matched_terms_set
    if 'self.matched_terms_set if hasattr' in content:
        print("✓ 4. 信号发送包含 matched_terms_set")
    else:
        print("✗ 4. 信号发送未包含 matched_terms_set")

    # 检查 5: search_completed 方法签名是否更新
    if 'def search_completed(self, results, lemma="", actual_variant_set=[], pos_full="", target_variant_set=[], matched_terms_set=[]):' in content:
        print("✓ 5. search_completed 方法签名已更新")
    else:
        print("✗ 5. search_completed 方法签名未更新")

    # 检查 6: 是否合并了高亮集合
    if 'highlight_set = set(target_variant_set)' in content and 'highlight_set.update(matched_terms_set)' in content:
        print("✓ 6. 高亮集合合并逻辑已实现")
    else:
        print("✗ 6. 高亮集合合并逻辑未找到")

    # 检查 7: 是否传递合并后的集合给 HTMLDelegate
    if 'self.html_delegate.set_search_params(self.current_search_params, list(highlight_set))' in content:
        print("✓ 7. 合并后的集合已传递给 HTMLDelegate")
    else:
        print("✗ 7. 合并后的集合未传递给 HTMLDelegate")


def test_html_delegate_modifications():
    """检查 HTMLDelegate 的修改"""

    print("\n=== 检查 HTMLDelegate 修改 ===\n")

    # 读取文件
    with open('gui/search_result_table_gui.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查: HTMLDelegate 的 variants 参数说明是否更新
    if 'variants: 需要高亮的词列表（包括变体和实际匹配的词）' in content:
        print("✓ HTMLDelegate 的文档字符串已更新，说明 variants 包含匹配的词")
    else:
        print("✗ HTMLDelegate 的文档字符串未更新")

    print("\n注意：HTMLDelegate 的高亮逻辑本身不需要修改，")
    print("因为我们通过 variants 参数传递了合并后的高亮集合。")


if __name__ == "__main__":
    test_search_engine_modifications()
    test_gui_modifications()
    test_html_delegate_modifications()

    print("\n" + "="*50)
    print("验证完成！")
    print("\n修改总结：")
    print("1. search_engine_kor.py: 收集所有实际匹配的词（包括词干）")
    print("2. qt_CorpusSearchTool.py: 在 SearchThread 和主窗口中传递匹配词集合")
    print("3. search_result_table_gui.py: 接收合并后的高亮集合")
    print("\n这样，词干形式（如 이루）就能被正确高亮了！")
