#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完整测试变体表生成功能
"""

import sys
sys.path.insert(0, '.')

from function.search_engine_kor import search_engine_kor

def generate_lemmalist(keywords):
    """生成变体表"""
    # 分析关键词
    analyzed_words = search_engine_kor.kiwi.analyze(keywords)
    
    # 提取主要词
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
    
    # 修正分析错误
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
    
    # 判定词性并生成变体
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
    
    # 格式化变体列表
    lemmalist_text = f"关键词: {keywords}\n"
    lemmalist_text += f"词性: {pos_full}\n"
    lemmalist_text += f"词典形: {lemma}\n"
    lemmalist_text += f"\n变体列表 ({len(variant_set)}个):\n"
    lemmalist_text += "\n".join([f"• {v}" for v in variant_set])
    
    return lemmalist_text

def test_all():
    """测试各种类型的词"""
    
    test_cases = [
        '이루다',      # 动词
        '하다',        # 动词
        '속다',        # 动词
        '좋아하다',    # 复合动词
        '사람',        # 名词
        '크다',        # 形容词
        '가다',        # 动词
        '먹다',        # 动词
        '예쁘다',      # 形容词
        '빠르다',      # 形容词
    ]
    
    for keyword in test_cases:
        print("=" * 60)
        print(f"测试: '{keyword}'")
        print("=" * 60)
        result = generate_lemmalist(keyword)
        print(result)
        print()
    
    print("=" * 60)
    print("✅ 所有测试完成")
    print("=" * 60)

if __name__ == '__main__':
    test_all()