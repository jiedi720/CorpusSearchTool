#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试配置文件中是否包含output_dir选项
"""

import os
import configparser
from function.config_manager import config_manager

print("=== 测试配置文件output_dir选项 ===")

# 打印当前配置
print("1. 当前配置:")
print(f"英语语料库配置: {config_manager.get_corpus_config('english')}")
print(f"韩语语料库配置: {config_manager.get_corpus_config('korean')}")

# 模拟保存配置（不传递output_dir参数）
print("\n2. 保存英语语料库配置（不传递output_dir）:")
config_manager.set_corpus_config('english', input_dir='E:/Test/EnglishCorpus', keyword_type='名词 & 副词')
config_manager.save_config()
print(f"英语语料库配置: {config_manager.get_corpus_config('english')}")

# 查看配置文件内容
print("\n3. 配置文件内容:")
with open('CorpusSearchTool.ini', 'r', encoding='utf-8') as f:
    config_content = f.read()
    print(config_content)
    
    # 检查是否包含output_dir
    if 'output_dir' in config_content:
        print("\n✅ 配置文件中包含output_dir选项")
    else:
        print("\n❌ 配置文件中不包含output_dir选项")

# 检查get_output_dir方法
print("\n4. 获取英语语料库的output_dir:")
output_dir = config_manager.get_output_dir()
print(f"output_dir: {output_dir}")

# 检查韩语语料库的output_dir
print("\n5. 保存韩语语料库配置:")
config_manager.set_corpus_config('korean', input_dir='E:/Test/KoreanCorpus', keyword_type='单词')
config_manager.save_config()
print(f"韩语语料库配置: {config_manager.get_corpus_config('korean')}")

# 再次查看配置文件
print("\n6. 配置文件内容（更新后）:")
with open('CorpusSearchTool.ini', 'r', encoding='utf-8') as f:
    config_content = f.read()
    print(config_content)
    
    # 检查是否包含output_dir
    if 'output_dir' in config_content:
        print("\n✅ 配置文件中包含output_dir选项")
    else:
        print("\n❌ 配置文件中不包含output_dir选项")
