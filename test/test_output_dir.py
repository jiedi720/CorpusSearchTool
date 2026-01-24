#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试output_dir默认值功能
验证当output_dir未设定时，是否默认使用input_dir
"""

from function.config_manager import config_manager

print("=== 测试output_dir默认值功能 ===")

# 测试1：获取当前配置
print("\n1. 当前配置:")
print(f"当前标签页: {config_manager.get_current_tab()}")
print(f"英语语料库配置: {config_manager.get_corpus_config('english')}")
print(f"韩语语料库配置: {config_manager.get_corpus_config('korean')}")

# 测试2：设置英语语料库的input_dir，但不设置output_dir
print("\n2. 设置英语语料库的input_dir，但不设置output_dir:")
config_manager.set_corpus_config('english', input_dir='E:/Test/EnglishCorpus')
english_config = config_manager.get_corpus_config('english')
print(f"英语语料库配置: {english_config}")
print(f"英语output_dir是否与input_dir相同: {english_config['output_dir'] == english_config['input_dir']}")

# 测试3：获取英语语料库的output_dir
print("\n3. 获取英语语料库的output_dir:")
english_output_dir = config_manager.get_output_dir()
print(f"英语output_dir: {english_output_dir}")

# 测试4：切换到韩语标签页，获取output_dir
print("\n4. 切换到韩语标签页，获取output_dir:")
config_manager.set_current_tab(1)
korean_output_dir = config_manager.get_output_dir()
korean_config = config_manager.get_corpus_config('korean')
print(f"韩语output_dir: {korean_output_dir}")
print(f"韩语output_dir是否与input_dir相同: {korean_output_dir == korean_config['input_dir']}")

# 测试5：显式设置output_dir为空字符串
print("\n5. 显式设置output_dir为空字符串:")
config_manager.set_corpus_config('english', output_dir='')
english_config = config_manager.get_corpus_config('english')
print(f"英语语料库配置: {english_config}")
print(f"英语output_dir是否与input_dir相同: {english_config['output_dir'] == english_config['input_dir']}")

# 测试6：显式设置output_dir为不同值
print("\n6. 显式设置output_dir为不同值:")
config_manager.set_corpus_config('english', output_dir='E:/Test/CustomOutput')
english_config = config_manager.get_corpus_config('english')
print(f"英语语料库配置: {english_config}")
print(f"英语output_dir是否与input_dir不同: {english_config['output_dir'] != english_config['input_dir']}")

# 测试7：通过set_output_dir方法设置为空
print("\n7. 通过set_output_dir方法设置为空:")
config_manager.set_output_dir('')
english_output_dir = config_manager.get_output_dir()
print(f"英语output_dir: {english_output_dir}")
print(f"英语output_dir是否与input_dir相同: {english_output_dir == english_config['input_dir']}")

print("\n=== 测试完成 ===")
