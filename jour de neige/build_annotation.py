#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the annotated lyrics JSON for "Jour de neige" (French -> Chinese),
then render HTML + DOCX via the multilingual-annotation-engine output writer.
"""
import json
import sys
import collections
from pathlib import Path

SKILL_DIR = Path("/Users/dylan/.claude/skills/multilingual-annotation-engine")
sys.path.insert(0, str(SKILL_DIR / "scripts"))

PALETTE = [
    "#E74C3C", "#2ECC71", "#3498DB", "#F39C12", "#9B59B6", "#1ABC9C",
    "#E67E22", "#2980B9", "#C0392B", "#27AE60", "#8E44AD", "#D35400",
    "#16A085", "#2C3E50", "#F1C40F", "#7F8C8D", "#E91E63", "#00BCD4",
    "#FF5722", "#795548", "#607D8B", "#4CAF50", "#FFC107", "#2196F3",
    "#9C27B0", "#FF9800", "#009688", "#673AB7", "#CDDC39", "#03A9F4",
]


def L(groups, torder=None):
    return {"groups": groups, "torder": torder}


# ---- reusable refrain lines -------------------------------------------
DOUX = [("doux", "Tout doux,", "轻轻的，"), ("doux", "tout doux", "轻轻的")]
REVE = [
    ("comme", "Comme", "像"), ("mesure", "un", "一场"), ("reve", "rêve", "梦"),
    ("un_peu", "un peu", "有点"), ("flou", "flou", "朦胧的"),
]
REVE_T = [0, 1, 3, 4, 2]
FROID = [
    ("froid", "Froid", "冷"), ("dehors", "dehors", "外面"), ("et", "et", "，"),
    ("chaud", "chaud", "暖"), ("dedans", "dedans", "里面"),
]
FROID_T = [1, 0, 2, 4, 3]
JOUR_NEIGE = [("jour", "Jour", "天"), ("neige", "de neige", "雪")]
JOUR_NEIGE_T = [1, 0]
PULL = [
    ("dans", "Dans", "裹在"), ("mesure", "un", "一件"), ("grand", "grand", "大"),
    ("pull", "pull", "毛衣里"), ("protege", "qui me protège", "保护我的"),
]
PULL_T = [0, 1, 4, 2, 3]
PREMIERE_NEIGE = [("premiere", "Première", "初"), ("neige", "neige", "雪")]
VERTIGE = [
    ("vertige", "Vertige", "眩晕"), ("en_moi", "en moi", "心中的"),
    ("comme", "comme", "像"), ("manege", "un manège", "旋转木马"),
]
VERTIGE_T = [1, 0, 2, 3]
TENDRE = [("jour", "Jour", "日子"), ("tendre", "bien tendre", "温柔的")]
TENDRE_T = [1, 0]
ATTENDRE = [
    ("comme", "Comme", "像"), ("ce", "ce", "那个"), ("quelquun", "quelqu'un", "的人"),
    ("vient", "qui vient", "来"), ("attendre", "m'attendre", "等我"),
]
ATTENDRE_T = [0, 1, 3, 4, 2]
CHEMIN = [("au", "Au", "在"), ("bout", "bout", "尽头"), ("chemin", "du chemin", "路的")]
CHEMIN_T = [0, 2, 1]

# ---- all 48 lines, in source order ------------------------------------
lines = [
    L(DOUX),
    L(REVE, REVE_T),
    L(FROID, FROID_T),
    L([("descendre", "Descendre", "冲下"),
       ("en_courant", "en courant", "跑着"),
       ("escalier", "l'escalier", "楼梯")], [1, 0, 2]),
    L([("quand", "Quand", "当"),
       ("tout", "tout,", "一切，"),
       ("meme", "même", "连"),
       ("ciel", "le ciel", "天空"),
       ("est", "est", "都是"),
       ("blanc", "blanc", "白的")]),
    L([("comme", "Comme", "像"),
       ("le", "le", "一张"),
       ("papier", "papier", "纸"),
       ("plie", "plié", "折起的"),
       ("secret", "d'un secret", "秘密")], [0, 1, 3, 4, 2]),
    L([("pressee", "Pressée", "匆匆忙忙"),
       ("sans_savoir", "sans savoir", "却不知"),
       ("pourquoi", "pourquoi", "为何")]),
    L([("filer", "Filer", "飞驰"),
       ("deja", "déjà", "已经"),
       ("sur", "sur", "骑上"),
       ("velo", "mon vélo", "我的单车")], [1, 2, 3, 0]),
    L([("longue", "La longue", "长长的"),
       ("echarpe", "écharpe", "围巾"),
       ("apres_moi", "après moi", "拖在身后")]),
    L([("coeur", "Le cœur", "心"),
       ("galop", "en plein galop", "在狂奔")]),
    L(JOUR_NEIGE, JOUR_NEIGE_T),
    L(PULL, PULL_T),
    L(PREMIERE_NEIGE),
    L(VERTIGE, VERTIGE_T),
    L(TENDRE, TENDRE_T),
    L(ATTENDRE, ATTENDRE_T),
    L(CHEMIN, CHEMIN_T),
    L(DOUX),
    L(REVE, REVE_T),
    L(FROID, FROID_T),
    L([("flocon", "Les flocons", "雪花"),
       ("comme", "comme", "像"),
       ("papillon", "des papillons", "蝴蝶")]),
    L([("sur", "Sur", "落在"),
       ("levres", "mes lèvres", "我的唇上"),
       ("et", "et", "，"),
       ("sur", "sur", "落在"),
       ("dents", "mes dents", "我的齿上")]),
    L([("une", "Une", "一阵"),
       ("sensation", "sensation", "感觉"),
       ("frisson", "frisson", "颤栗的")], [0, 2, 1]),
    L([("et_pour_ca", "Et pour ça,", "正因如此，"),
       ("vouloir", "vouloir", "想要"),
       ("preserver", "préserver", "把它留住"),
       ("pareille", "pareille", "原样")], [0, 1, 3, 2]),
    L([("blancheur", "La blancheur", "洁白"),
       ("que_rien", "que rien", "什么都"),
       ("sauvera", "ne sauvera", "无法挽回的")], [1, 2, 0]),
    L([("apres", "Après", "之后"),
       ("retour", "le retour", "归来"),
       ("soleil", "du soleil", "太阳")], [2, 1, 0]),
    L([("toujours", "Toujours,", "永远，"),
       ("toujours", "toujours", "永远"),
       ("en_moi", "en moi", "在我心中")]),
    L(JOUR_NEIGE, JOUR_NEIGE_T),
    L(PULL, PULL_T),
    L(PREMIERE_NEIGE),
    L(VERTIGE, VERTIGE_T),
    L(TENDRE, TENDRE_T),
    L(ATTENDRE, ATTENDRE_T),
    L(CHEMIN, CHEMIN_T),
    L(DOUX),
    L(REVE, REVE_T),
    L(JOUR_NEIGE, JOUR_NEIGE_T),
    L(PULL, PULL_T),
    L(JOUR_NEIGE, JOUR_NEIGE_T),
    L([("au_loin", "Au loin", "远处"),
       ("disparait", "disparaît", "消失了"),
       ("manege", "le manège", "旋转木马")], [0, 2, 1]),
    L(PREMIERE_NEIGE),
    L([("tourbillon", "Tourbillon", "旋风"),
       ("leger", "léger", "轻柔的"),
       ("enleve", "qui m'enlève", "把我带走")], [1, 0, 2]),
    L(JOUR_NEIGE, JOUR_NEIGE_T),
    L([("sur_velo", "Sur mon vélo", "骑着单车"),
       ("comme", "comme", "如"),
       ("dans_reve", "dans un rêve", "在梦中")]),
    L(JOUR_NEIGE, JOUR_NEIGE_T),
    L([("pourtant", "Et pourtant", "然而"),
       ("avoir_peur", "j'ai peur", "我不怕"),
       ("aucun_piege", "d'aucun piège", "任何陷阱")]),
    L(JOUR_NEIGE, JOUR_NEIGE_T),
    L([("dans", "Dans", "裹在"),
       ("grand", "un grand", "大"),
       ("pull", "pull", "毛衣里")]),
]

assert len(lines) == 48, f"expected 48 lines, got {len(lines)}"

# ---- idiomatic, emotion-matched free translation per line (Reading tab) ----
# These differ from the word-aligned gloss: fluent, native-quality 信达雅.
FREE = [
    "轻轻柔柔，轻轻柔柔",           # 1  Tout doux, tout doux
    "像一场朦胧的梦",               # 2  Comme un rêve un peu flou
    "外面冷，里面暖",               # 3  Froid dehors et chaud dedans
    "一路小跑冲下楼梯",             # 4  Descendre en courant l'escalier
    "当一切，连天空都是白的",       # 5  Quand tout, même le ciel est blanc
    "像一张折起的秘密纸条",         # 6  Comme le papier plié d'un secret
    "匆匆忙忙，却不知为何",         # 7  Pressée sans savoir pourquoi
    "已经骑上单车飞驰",             # 8  Filer déjà sur mon vélo
    "长围巾拖在身后",               # 9  La longue écharpe après moi
    "心在狂奔",                     # 10 Le cœur en plein galop
    "下雪天",                       # 11 Jour de neige
    "裹在一件保护着我的大毛衣里",   # 12 Dans un grand pull qui me protège
    "初雪",                         # 13 Première neige
    "心中的眩晕像旋转木马",         # 14 Vertige en moi comme un manège
    "温柔的日子",                   # 15 Jour bien tendre
    "像那个来等我的人",             # 16 Comme ce quelqu'un qui vient m'attendre
    "在路的尽头",                   # 17 Au bout du chemin
    "轻轻柔柔，轻轻柔柔",           # 18
    "像一场朦胧的梦",               # 19
    "外面冷，里面暖",               # 20
    "雪花像蝴蝶一样",               # 21 Les flocons comme des papillons
    "落在我的唇上，落在我的齿间",   # 22 Sur mes lèvres et sur mes dents
    "一阵颤栗的感觉",               # 23 Une sensation frisson
    "正因如此，想要把它原样留住",   # 24 Et pour ça, vouloir préserver pareille
    "那终将消逝的洁白",             # 25 La blancheur que rien ne sauvera
    "当太阳归来之后",               # 26 Après le retour du soleil
    "永远，永远在我心中",           # 27 Toujours, toujours en moi
    "下雪天",                       # 28
    "裹在一件保护着我的大毛衣里",   # 29
    "初雪",                         # 30
    "心中的眩晕像旋转木马",         # 31
    "温柔的日子",                   # 32
    "像那个来等我的人",             # 33
    "在路的尽头",                   # 34
    "轻轻柔柔，轻轻柔柔",           # 35
    "像一场朦胧的梦",               # 36
    "下雪天",                       # 37
    "裹在一件保护着我的大毛衣里",   # 38
    "下雪天",                       # 39
    "远处，旋转木马渐渐消失",       # 40 Au loin disparaît le manège
    "初雪",                         # 41
    "轻柔的旋风把我卷起",           # 42 Tourbillon léger qui m'enlève
    "下雪天",                       # 43
    "骑着单车，如在梦中",           # 44 Sur mon vélo comme dans un rêve
    "下雪天",                       # 45
    "然而我什么陷阱都不怕",         # 46 Et pourtant j'ai peur d'aucun piège
    "下雪天",                       # 47
    "裹在大毛衣里",                 # 48 Dans un grand pull
]
assert len(FREE) == 48, f"expected 48 free translations, got {len(FREE)}"

# ---- vocabulary: concept -> (lemma, pronunciation, meaning, pos) ------
# order is irrelevant; color + frequency are computed from the lines above.
VOCAB = {
    "doux":         ("doux", "doo", "轻柔的；温和的", "形容词"),
    "comme":        ("comme", "kom", "像；如同", "连词"),
    "mesure":       ("un / une", "un", "一个（量词）", "量词"),
    "reve":         ("rêve", "rev", "梦", "名词"),
    "un_peu":       ("un peu", "un puh", "一点；有点", "副词"),
    "flou":         ("flou", "floo", "朦胧的；模糊的", "形容词"),
    "froid":        ("froid", "frwa", "寒冷的", "形容词"),
    "dehors":       ("dehors", "duh-or", "外面", "副词"),
    "et":           ("et", "ay", "和；而", "连词"),
    "chaud":        ("chaud", "sho", "温暖的", "形容词"),
    "dedans":       ("dedans", "duh-dahn", "里面", "副词"),
    "descendre":    ("descendre", "deh-sahndr", "走下；冲下", "动词"),
    "en_courant":   ("en courant", "ahn koo-rahn", "跑着", "副动词"),
    "escalier":     ("escalier", "ess-kal-yay", "楼梯", "名词"),
    "quand":        ("quand", "kahn", "当……时", "连词"),
    "tout":         ("tout", "too", "一切；所有", "代词"),
    "meme":         ("même", "mem", "甚至；连", "副词"),
    "ciel":         ("ciel", "syel", "天空", "名词"),
    "est":          ("est", "eh", "是（être）", "动词"),
    "blanc":        ("blanc", "blahn", "白色的", "形容词"),
    "le":           ("le", "luh", "定冠词（量词）", "冠词"),
    "papier":       ("papier", "pah-pyay", "纸", "名词"),
    "plie":         ("plié", "plee-yay", "折起的", "形容词"),
    "secret":       ("secret", "suh-kreh", "秘密", "名词"),
    "pressee":      ("pressée", "preh-say", "匆忙的", "形容词"),
    "sans_savoir":  ("sans savoir", "sahn sah-vwar", "却不知", "短语"),
    "pourquoi":     ("pourquoi", "poor-kwa", "为什么；为何", "副词"),
    "filer":        ("filer", "fee-lay", "飞奔；疾驰", "动词"),
    "deja":         ("déjà", "day-zhah", "已经", "副词"),
    "sur":          ("sur", "soor", "在……上；落在", "介词"),
    "velo":         ("vélo", "vay-lo", "自行车；单车", "名词"),
    "longue":       ("longue", "lohng", "长的", "形容词"),
    "echarpe":      ("écharpe", "ay-sharp", "围巾", "名词"),
    "apres_moi":    ("après moi", "ah-preh mwa", "在我身后", "短语"),
    "coeur":        ("cœur", "kur", "心", "名词"),
    "galop":        ("galop", "gah-lo", "疾驰；狂奔", "名词"),
    "jour":         ("jour", "zhoor", "日子；天", "名词"),
    "neige":        ("neige", "nezh", "雪", "名词"),
    "dans":         ("dans", "dahn", "在……里", "介词"),
    "grand":        ("grand", "grahn", "大的", "形容词"),
    "pull":         ("pull", "puhl", "毛衣；套头衫", "名词"),
    "protege":      ("protège", "pro-tezh", "保护", "动词"),
    "premiere":     ("première", "pruh-myair", "第一的；初次的", "形容词"),
    "vertige":      ("vertige", "ver-teezh", "眩晕", "名词"),
    "en_moi":       ("en moi", "ahn mwa", "在我心中", "短语"),
    "manege":       ("manège", "mah-nezh", "旋转木马", "名词"),
    "tendre":       ("tendre", "tahndr", "温柔的", "形容词"),
    "ce":           ("ce", "suh", "这个；那个", "指示词"),
    "quelquun":     ("quelqu'un", "kel-kun", "某人；那个人", "代词"),
    "vient":        ("vient", "vyahn", "来（venir）", "动词"),
    "attendre":     ("attendre", "ah-tahndr", "等待", "动词"),
    "au":           ("au", "oh", "在（à+le）", "介词"),
    "bout":         ("bout", "boo", "尽头；末端", "名词"),
    "chemin":       ("chemin", "shuh-man", "路；小路", "名词"),
    "flocon":       ("flocon", "flo-kon", "雪花", "名词"),
    "papillon":     ("papillon", "pah-pee-yon", "蝴蝶", "名词"),
    "levres":       ("lèvres", "levr", "嘴唇", "名词"),
    "dents":        ("dents", "dahn", "牙齿", "名词"),
    "une":          ("une", "oon", "一阵（量词）", "量词"),
    "sensation":    ("sensation", "sahn-sah-syon", "感觉", "名词"),
    "frisson":      ("frisson", "free-son", "颤栗；寒战", "名词"),
    "et_pour_ca":   ("et pour ça", "ay poor sah", "正因如此", "短语"),
    "vouloir":      ("vouloir", "voo-lwar", "想要", "动词"),
    "preserver":    ("préserver", "pray-zer-vay", "保留；留住", "动词"),
    "pareille":     ("pareille", "pah-rey", "同样的；原样", "形容词"),
    "blancheur":    ("blancheur", "blahn-shur", "洁白；白色", "名词"),
    "que_rien":     ("que rien", "kuh ryahn", "什么都不", "短语"),
    "sauvera":      ("sauvera", "so-vrah", "挽救；挽回", "动词"),
    "apres":        ("après", "ah-preh", "在……之后", "介词"),
    "retour":       ("retour", "ruh-toor", "归来；返回", "名词"),
    "soleil":       ("soleil", "so-lay", "太阳", "名词"),
    "toujours":     ("toujours", "too-zhoor", "永远", "副词"),
    "au_loin":      ("au loin", "oh lwan", "在远处", "短语"),
    "disparait":    ("disparaît", "dee-spa-reh", "消失", "动词"),
    "tourbillon":   ("tourbillon", "toor-bee-yon", "漩涡；旋风", "名词"),
    "leger":        ("léger", "lay-zhay", "轻盈的；轻柔的", "形容词"),
    "enleve":       ("enlève", "ahn-lev", "带走；卷起", "动词"),
    "sur_velo":     ("sur mon vélo", "soor mon vay-lo", "骑着我的单车", "短语"),
    "dans_reve":    ("dans un rêve", "dahn un rev", "在梦中", "短语"),
    "pourtant":     ("pourtant", "poor-tahn", "然而", "连词"),
    "avoir_peur":   ("avoir peur", "ah-vwar pur", "害怕", "动词短语"),
    "aucun_piege":  ("aucun piège", "oh-kun pyezh", "任何陷阱", "短语"),
}

# ============================================================
#  Build color lexicon + rows
# ============================================================
lex = {}          # concept -> color
freq = collections.Counter()

rows = []
for i, line in enumerate(lines, start=1):
    groups = line["groups"]
    torder = line["torder"] if line["torder"] is not None else list(range(len(groups)))

    # assign colors in first-encounter order
    for (concept, fr, zh) in groups:
        if concept not in lex:
            lex[concept] = PALETTE[len(lex) % len(PALETTE)]
        freq[concept] += 1

    # original row (French order)
    orig_segments = []
    for gi, (concept, fr, zh) in enumerate(groups):
        text = fr + (" " if gi < len(groups) - 1 else "")
        seg = {"text": text, "color": lex[concept], "group_id": f"L{i:02d}-W{gi+1}"}
        pron = VOCAB.get(concept, (None, None, None, None))[1]
        if pron:
            seg["pronunciation"] = pron
        orig_segments.append(seg)

    # translation row (Chinese order)
    trans_segments = []
    for tj, gi in enumerate(torder):
        concept, fr, zh = groups[gi]
        seg = {"text": zh, "color": lex[concept], "group_id": f"L{i:02d}-W{gi+1}"}
        trans_segments.append(seg)

    rows.append({"type": "original", "language": "fr", "direction": "ltr",
                 "script": "Latin", "free_translation": FREE[i-1],
                 "segments": orig_segments})
    rows.append({"type": "translation", "language": "zh", "direction": "ltr",
                 "script": "CJK", "segments": trans_segments})

# ============================================================
#  Vocabulary list
# ============================================================
vocabulary = []
for concept in lex:
    word, pron, meaning, pos = VOCAB[concept]
    vocabulary.append({
        "word": word,
        "romanization": pron,
        "meaning": meaning,
        "pos": pos,
        "color": lex[concept],
        "frequency": freq[concept],
    })
# sort by frequency desc, then word
vocabulary.sort(key=lambda v: (-v["frequency"], v["word"]))

# ============================================================
#  Structure + metadata
# ============================================================
structure = {
    "structure_type": "verse-chorus",
    "sections": [
        {"type": "Verse", "number": 1, "line_start": 1, "line_end": 10},
        {"type": "Chorus", "number": 1, "line_start": 11, "line_end": 17},
        {"type": "Verse", "number": 2, "line_start": 18, "line_end": 27},
        {"type": "Chorus", "number": 2, "line_start": 28, "line_end": 34},
        {"type": "Outro", "number": 1, "line_start": 35, "line_end": 48},
    ],
}

data = {
    "verse_id": "jour-de-neige",
    "text_direction": "ltr",
    "script_family": "latin",
    "metadata": {
        "source_language": "fr",
        "target_language": "zh",
        "title": "Jour de neige",
        "artist": "",
        "sentiment": "tender",
    },
    "structure": structure,
    "rows": rows,
    "vocabulary": vocabulary,
    "annotations": [],
}

# ============================================================
#  Write JSON + render HTML/DOCX
# ============================================================
out_dir = Path("/Users/dylan/Desktop/jour de neige")

json_path = out_dir / "annotation.json"
json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

import output_writer

html = output_writer.render_html(data)
(out_dir / "jour-de-neige.html").write_text(html, encoding="utf-8")

docx_bytes = output_writer.render_docx(data)
(out_dir / "jour-de-neige.docx").write_bytes(docx_bytes)

print(json.dumps({
    "lines": len(lines),
    "rows": len(rows),
    "unique_concepts": len(lex),
    "vocabulary": len(vocabulary),
    "json_bytes": json_path.stat().st_size,
    "html_bytes": (out_dir / "jour-de-neige.html").stat().st_size,
    "docx_bytes": (out_dir / "jour-de-neige.docx").stat().st_size,
}, ensure_ascii=False, indent=2))
