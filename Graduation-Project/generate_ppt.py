#!/tmp/pptx-venv/bin/python3
"""毕业答辩PPT v3 — 精确定位版"""
from pptx import Presentation
from pptx.util import Inches, Pt as E, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import copy

def Pt(v): return E(v)

# 固定16:9宽屏
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# 颜色
BG      = RGBColor(0xFF, 0xFF, 0xFF)
BG_DARK = RGBColor(0x0B, 0x0E, 0x11)
BLUE    = RGBColor(0x1A, 0x3C, 0x6E)
BLUE2   = RGBColor(0x29, 0x80, 0xB9)
TEAL    = RGBColor(0x17, 0xA1, 0x8E)
RED     = RGBColor(0xE7, 0x4C, 0x3C)
GREEN   = RGBColor(0x27, 0xAE, 0x60)
ORANGE  = RGBColor(0xF3, 0x9C, 0x12)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
TEXT    = RGBColor(0x2C, 0x3E, 0x50)
TEXT2   = RGBColor(0x7F, 0x8C, 0x9A)
CARD    = RGBColor(0xF4, 0xF6, 0xF9)
GREEN_BG = RGBColor(0xE8, 0xF5, 0xE9)
BLUE_BG  = RGBColor(0xEB, 0xF5, 0xFB)

def add_shape(s, l, t, w, h, c):
    x = s.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    x.fill.solid(); x.fill.fore_color.rgb = c; x.line.fill.background()
    return x

def add_text(s, l, t, w, h, txt, sz=16, c=TEXT, b=False, a=PP_ALIGN.LEFT, v=MSO_ANCHOR.TOP):
    bx = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    bx.text_frame.word_wrap = True; bx.text_frame.auto_size = None
    bx.text_frame.paragraphs[0].text = txt
    bx.text_frame.paragraphs[0].font.size = Pt(sz)
    bx.text_frame.paragraphs[0].font.color.rgb = c
    bx.text_frame.paragraphs[0].font.bold = b
    bx.text_frame.paragraphs[0].alignment = a
    bx.text_frame.vertical_anchor = v
    return bx

def add_bullets(s, l, t, w, h, items, sz=14, c=TEXT, sp=8):
    bx = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    bx.text_frame.word_wrap = True; bx.text_frame.auto_size = None
    for i, item in enumerate(items):
        p = bx.text_frame.paragraphs[0] if i == 0 else bx.text_frame.add_paragraph()
        p.text = item; p.font.size = Pt(sz); p.font.color.rgb = c; p.space_after = Pt(sp)
    return bx

def page_header(s, title, subtitle=""):
    add_shape(s, 0, 0, 13.333, 1.1, BLUE)
    add_shape(s, 0, 0, 0.12, 1.1, BLUE2)
    add_text(s, 0.6, 0.15, 10, 0.55, title, 26, WHITE, True)
    if subtitle:
        add_text(s, 0.6, 0.65, 10, 0.35, subtitle, 13, RGBColor(0xBB,0xCC,0xDD))
    n = len(prs.slides)
    add_text(s, 12.2, 0.3, 1, 0.5, f"{n:02d}", 14, RGBColor(0x99,0xAA,0xBB), a=PP_ALIGN.RIGHT)

def make_tbl(s, rows, cols, l, t, w, h, headers, data, hl=None):
    tbl = s.shapes.add_table(rows, cols, Inches(l), Inches(t), Inches(w), Inches(h)).table
    for j, hd in enumerate(headers):
        c = tbl.cell(0, j); c.text = hd
        for p in c.text_frame.paragraphs: p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = WHITE
        c.fill.solid(); c.fill.fore_color.rgb = BLUE
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            c = tbl.cell(i+1, j); c.text = val
            for p in c.text_frame.paragraphs:
                p.font.size = Pt(10); p.font.color.rgb = TEXT
                if hl is not None and i == hl: p.font.color.rgb = GREEN; p.font.bold = True
            if hl is not None and i == hl: c.fill.solid(); c.fill.fore_color.rgb = GREEN_BG
            elif i % 2 == 0: c.fill.solid(); c.fill.fore_color.rgb = RGBColor(0xF8,0xF9,0xFA)

def section_box(s, l, t, w, h, title, items, color=BLUE2, title_sz=15, item_sz=12):
    add_shape(s, l, t, w, h, WHITE)
    add_shape(s, l, t, 0.06, h, color)
    add_text(s, l+0.25, t+0.08, w-0.5, 0.35, title, title_sz, color, True)
    add_bullets(s, l+0.25, t+0.45, w-0.5, h-0.55, items, item_sz, TEXT, 4)

# ============================================================
# P1 封面
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_shape(s, 0, 0, 13.333, 7.5, BG_DARK)
add_shape(s, 0, 0, 13.333, 0.05, BLUE2)
add_shape(s, 0, 7.45, 13.333, 0.05, BLUE2)

add_text(s, 1.2, 1.0, 5, 0.5, "本科毕业设计答辩", 15, TEXT2)
add_text(s, 1.2, 1.8, 11, 1.0, "基于优化XGBoost的\nDGA检测系统设计", 34, WHITE, True)
add_text(s, 1.2, 3.0, 11, 0.4, "Design of DGA Detection System Based on Optimized XGBoost", 14, TEXT2)
add_shape(s, 1.2, 3.5, 3, 0.02, BLUE2)

info = [
    ("学    院：", "数学与信息科学学院"),
    ("专    业：", "信息安全"),
    ("班    级：", "信安221"),
    ("学生姓名：", "苑文洋"),
    ("学    号：", "32215300032"),
    ("指导教师：", "余玉银"),
]
for i, (k, v) in enumerate(info):
    add_text(s, 1.2, 3.8+i*0.42, 1.5, 0.35, k, 13, TEXT2)
    add_text(s, 2.8, 3.8+i*0.42, 4, 0.35, v, 13, WHITE)

# ============================================================
# P2 目录
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "目  录", "CONTENTS")
toc = [
    ("01", "研究背景与意义", "DGA威胁现状与检测挑战"),
    ("02", "相关理论与技术", "XGBoost / 贝叶斯优化 / 特征工程"),
    ("03", "系统设计与实现", "数据预处理 / 特征提取 / 模型训练"),
    ("04", "实验与分析", "二分类 / 多分类 / 结果对比"),
    ("05", "总结与展望", "创新点 / 不足 / 改进方向"),
]
for i, (num, title, desc) in enumerate(toc):
    y = 1.7 + i * 1.0
    add_shape(s, 2.5, y, 0.8, 0.55, BLUE2)
    add_text(s, 2.55, y+0.05, 0.7, 0.45, num, 18, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    add_text(s, 3.6, y+0.02, 6, 0.3, title, 18, BLUE, True)
    add_text(s, 3.6, y+0.32, 6, 0.2, desc, 12, TEXT2)

# ============================================================
# P3 研究背景
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "01  研究背景与意义")

section_box(s, 0.5, 1.5, 6, 3.5, "核心问题", [
    "DGA：僵尸网络逃避黑名单检测的核心手段",
    "攻击者通过算法生成随机域名，动态切换C2服务器",
    "传统黑名单/签名检测无法应对域名频繁变种",
    "单日可生成数万个域名，防御方难以预判",
], BLUE2, 15, 13)

section_box(s, 7, 1.5, 6, 3.5, "本文目标", [
    "基于XGBoost构建检测模型，兼顾效率与精度",
    "引入贝叶斯优化（Optuna）自动调参",
    "对比统计/N-gram/融合特征方案",
    "同时实现二分类（恶意检测）和多分类（家族溯源）",
], RED, 15, 13)

add_shape(s, 0.5, 5.5, 12.3, 1.3, BLUE_BG)
add_text(s, 0.8, 5.6, 11.5, 0.35, "🎯  研究目标", 15, BLUE2, True)
add_text(s, 0.8, 6.0, 11.5, 0.6, "构建基于优化XGBoost的DGA检测系统，实现高效的二分类恶意域名检测与多分类家族溯源", 13, TEXT)

# ============================================================
# P4 DGA技术
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "02  DGA技术原理")

add_shape(s, 0.5, 1.4, 12.3, 0.55, CARD)
add_text(s, 0.8, 1.45, 4, 0.4, "DGA攻击流程", 15, BLUE2, True)

flow = ["恶意软件感染", "DGA计算域名", "尝试连接C2", "注册少数域名", "执行控制指令"]
for i, step in enumerate(flow):
    x = 0.8 + i * 2.5
    c = BLUE2 if i < 4 else RED
    add_shape(s, x, 2.2, 2.0, 0.65, c)
    add_text(s, x+0.05, 2.28, 1.9, 0.5, step, 12, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    if i < 4:
        add_text(s, x+2.0, 2.3, 0.5, 0.4, "→", 20, BLUE, True, PP_ALIGN.CENTER)

add_bullets(s, 0.5, 3.2, 12.3, 3.5, [
    "DGA核心逻辑：种子 + 算法 → 批量生成候选域名 → 攻击者注册少量即可维持C2通信",
    "主流DGA家族：Suppobox（日期+字典）、Kraken（字符拼接）、Shiotob（时间种子）、Bamital等",
    "检测难点：域名高度随机化、不断变种、合法域名可能被误报",
    "传统方法局限：黑名单无法预知、规则匹配难以应对算法变种",
], 13, TEXT, 7)

# ============================================================
# P5 XGBoost
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "02  XGBoost算法原理")

section_box(s, 0.5, 1.5, 6, 3.2, "核心机制", [
    "逐步添加决策树，每棵新树修正残差",
    "损失 = 训练误差 + L1/L2正则化",
    "二阶泰勒展开近似，收敛快于GBDT",
    "列采样 + Shrinkage + 早停防过拟合",
], BLUE2, 15, 13)

section_box(s, 7, 1.5, 6, 3.2, "选择XGBoost的原因", [
    "✅ 天然处理高维稀疏特征（10,000维）",
    "✅ Boosting序列优化，偏差低于RF",
    "✅ 训练速度快于深度学习5~10倍",
    "✅ 可解释性强，特征重要性可直接获取",
], TEAL, 15, 13)

add_shape(s, 0.5, 5.2, 12.3, 1.5, CARD)
add_text(s, 0.8, 5.3, 4, 0.35, "目标函数", 15, BLUE, True)
add_text(s, 0.8, 5.7, 11, 0.9, "Obj = Σ L(yᵢ, ŷᵢ) + Σ Ω(fₖ)\nΩ(f) = γT + ½λ‖ω‖²    L=损失  Ω=正则化  T=叶节点  ω=叶权重", 13, TEXT)

# ============================================================
# P6 特征工程
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "02  特征工程")

section_box(s, 0.5, 1.5, 6, 4.0, "统计特征（6维）", [
    "① 域名长度 — 正常与DGA域名字符数差异",
    "② 数字占比 — DGA含大量随机数字",
    "③ 信息熵 — 随机字符串熵值更高",
    "④ 连续辅音比例 — 恶意域名常辅音堆叠",
    "⑤ 重复字符比例 — 正常域名更易记忆",
    "⑥ 元音占比 — 正常域名可读性更强",
], BLUE2, 15, 12)

section_box(s, 7, 1.5, 6, 4.0, "N-gram 特征", [
    "将域名按n个连续字符滑动切分",
    "2-gram 示例：apple → ap pp pl le",
    "CountVectorizer统计各组合频次",
    "取最频繁的10,000维作为特征",
    "捕捉微观字符序列模式差异",
    "2-4gram 混合2/3/4字符组合",
], TEAL, 15, 12)

add_shape(s, 0.5, 5.9, 12.3, 1.0, RGBColor(0xFE,0xF3,0xE0))
add_text(s, 0.8, 6.0, 11, 0.8, "💡 融合策略：统计特征（宏观基准）+ 2-gram特征（微观指纹）→ 维度 6 + 10,000 = 10,006", 14, ORANGE, True)

# ============================================================
# P7 系统架构
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "03  系统设计——整体架构")

flow = ["域名采集", "数据预处理", "特征提取", "模型训练", "结果评估"]
for i, step in enumerate(flow):
    x = 0.6 + i * 2.5
    c = BLUE2 if i < 4 else GREEN
    add_shape(s, x, 1.6, 2.0, 0.7, c)
    add_text(s, x+0.1, 1.65, 1.8, 0.5, f"Step {i+1}", 11, WHITE, a=PP_ALIGN.CENTER)
    add_text(s, x+0.1, 1.85, 1.8, 0.4, step, 13, WHITE, True, PP_ALIGN.CENTER)
    if i < 4:
        add_text(s, x+2.0, 1.75, 0.5, 0.4, "→", 20, BLUE, True, PP_ALIGN.CENTER)

details = [
    ("📥  数据采集", "Alexa 20万 + 360 DGA 20万 = 40万样本"),
    ("🧹  数据预处理", "去重 → 去TLD → 8:1:1 划分训练/验证/测试集"),
    ("🔧  特征提取", "统计特征（6维）+ N-gram（CountVectorizer, top 10,000）"),
    ("⚙️  模型训练", "XGBoost默认参数 vs Optuna贝叶斯优化"),
    ("📊  结果评估", "准确率 / 精确率 / 召回率 / F1 / AUC"),
]
for i, (title, desc) in enumerate(details):
    y = 2.7 + i * 0.75
    add_shape(s, 1.5, y, 6, 0.55, CARD)
    add_text(s, 1.7, y+0.02, 2.5, 0.3, title, 13, BLUE2, True)
    add_text(s, 1.7, y+0.28, 6, 0.25, desc, 12, TEXT)

# ============================================================
# P8 预处理
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "03  数据预处理")

section_box(s, 0.5, 1.5, 6, 4.0, "处理流程", [
    "① 数据清洗：去除空值、重复域名",
    "② TLD剥离：去除.com/.net等顶级域后缀",
    "③ 标签编码：良性 → 0，DGA家族 → 1~10",
    "④ 划分：训练80% / 验证10% / 测试10%",
    "⑤ 特征标准化：CountVectorizer拟合",
], BLUE2, 15, 13)

section_box(s, 7, 1.5, 6, 4.0, "为什么去TLD？", [
    "TLD是受控注册基准，对检测无贡献",
    "DGA核心对抗逻辑在二级域名（前缀）",
    "去除TLD可减少噪声，增强敏感度",
    "例：abc123.com → abc123",
    "保留全部前缀层级",
], RED, 15, 13)

add_shape(s, 0.5, 5.8, 12.3, 1.2, CARD)
add_text(s, 0.8, 5.9, 5, 0.35, "📊  数据集统计", 15, BLUE, True)
add_text(s, 0.8, 6.3, 11, 0.5, "训练集 320,000  |  验证集 40,000  |  测试集 40,000  |  合计 400,000 条域名样本", 14, TEXT2)

# ============================================================
# P9 实验设计
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "04  实验设计——特征分组")

make_tbl(s, 5, 4, 1, 1.6, 11.5, 2.2,
    ["特征组", "特征组合", "说明", "维度"],
    [["①", "统计特征", "6维统计特征", "6"],
     ["②", "2-gram 特征", "Bigram切片 + CountVectorizer", "10,000"],
     ["③", "2-4gram 特征", "混合切片（2/3/4字符）", "10,000"],
     ["④", "统计 + 2-gram", "融合特征（最优组合）", "10,006"]])

add_text(s, 1, 4.3, 8, 0.4, "实验设置", 17, BLUE, True)
add_bullets(s, 1, 4.8, 11, 1.5, [
    "实验一（二分类）：区分恶意域名（DGA）和良性域名（Alexa）",
    "实验二（多分类）：对10个DGA家族进行细粒度分类",
    "每组特征分别在 XGBoost 默认参数和 Optuna 贝叶斯优化下实验",
], 13, TEXT, 6)

# ============================================================
# P10 二分类结果
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "04  实验结果——二分类")

add_shape(s, 0.5, 1.4, 12.3, 0.9, GREEN_BG)
add_text(s, 0.8, 1.45, 11, 0.35, "🏆  最优结果", 15, GREEN, True)
add_text(s, 0.8, 1.78, 11.5, 0.4, "统计特征 + 2-gram + Optuna → 准确率 98.40%  |  F1 98.40%  |  AUC 0.9989", 14, GREEN, True)

make_tbl(s, 7, 7, 0.3, 2.6, 12.7, 4.2,
    ["特征组", "优化", "准确率", "精确率", "召回率", "F1", "AUC"],
    [["统计特征",    "默认", "95.87%", "95.97%", "95.77%", "95.87%", "0.9931"],
     ["统计特征",    "Optuna","96.12%","96.48%","95.76%","96.12%","0.9948"],
     ["2-gram",     "默认", "97.53%", "97.44%", "97.63%", "97.53%", "0.9979"],
     ["2-gram",     "Optuna","97.69%","97.72%","97.66%","97.69%","0.9981"],
     ["统计+2-gram", "默认", "98.10%", "98.39%", "97.81%", "98.10%", "0.9984"],
     ["统计+2-gram", "Optuna","98.40%","98.47%","98.33%","98.40%","0.9989"]], hl=5)

# ============================================================
# P11 多分类结果
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "04  实验结果——多分类")

add_shape(s, 0.5, 1.4, 12.3, 0.75, GREEN_BG)
add_text(s, 0.8, 1.48, 11, 0.5, "🏆  最优：统计 + 2-gram 融合组 → 宏平均 F1 = 88.95%", 15, GREEN, True)

make_tbl(s, 5, 4, 1.5, 2.5, 10, 2.5,
    ["特征组", "准确率", "宏平均 F1", "说明"],
    [["统计特征",      "65.59%", "53.78%", "宏观基准定位，区分度有限"],
     ["2-gram 特征",   "84.46%", "76.80%", "微观指纹提取，效果显著"],
     ["2-4gram 特征",  "85.55%", "77.70%", "相比2-gram提升有限"],
     ["统计+2-gram",   "89.98%", "88.95%", "✅ 最优组合"]], hl=3)

add_shape(s, 0.5, 5.5, 12.3, 1.3, BLUE_BG)
add_text(s, 0.8, 5.6, 5, 0.35, "📌 分析发现", 14, BLUE2, True)
add_text(s, 0.8, 6.0, 11.5, 0.5, "统计特征→宏观基准  |  2-gram→微观指纹  |  融合→互补增益", 13, TEXT)
add_text(s, 0.8, 6.35, 11.5, 0.4, "贝叶斯优化：二分类+0.3%  |  多分类+3~5%（复杂任务收益更大）", 13, TEXT)

# ============================================================
# P12 Optuna
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "03  Optuna贝叶斯优化")

add_shape(s, 0.5, 1.5, 12.3, 0.55, CARD)
add_text(s, 0.8, 1.55, 11, 0.4, "优化流程：定义目标函数 → 搜索超参数 → 自动剪枝 → 输出最优参数", 14, BLUE2, True)

section_box(s, 0.5, 2.4, 6, 3.5, "超参数搜索范围", [
    "learning_rate:   [0.01, 0.3]",
    "max_depth:       [3, 12]",
    "n_estimators:    [50, 500]",
    "subsample:       [0.6, 1.0]",
    "colsample_bytree: [0.6, 1.0]",
    "reg_lambda:      [0, 5]",
], BLUE2, 14, 13)

section_box(s, 7, 2.4, 6, 3.5, "优化效果对比", [
    "统计+2-gram / 二分类：",
    "  准确率 98.10% → 98.40%  ▲",
    "  F1     98.10% → 98.40%  ▲",
    "  AUC   0.9984 → 0.9989 ▲",
    "多分类提升：+3~5%（更显著）",
    "搜索效率：50~100次试验收敛",
], TEAL, 14, 13)

# ============================================================
# P13 结果分析
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "04  结果分析")

section_box(s, 0.5, 1.5, 12.3, 1.5, "📊  特征对比", [
    "统计特征：宏观基准定位，多分类F1仅53.78%，单独使用有限",
    "2-gram特征：微观指纹提取，F1达76.80%，效果显著优于统计",
    "融合特征：两者互补，F1 88.95%，为最优组合",
    "2-4gram vs 2-gram：提升有限，融合时增益递减",
], BLUE2, 14, 12)

section_box(s, 0.5, 3.3, 12.3, 1.5, "⚙️  优化对比", [
    "二分类：默认→ Optuna 提升约+0.3%（已接近理论上限，AUC>0.99）",
    "多分类：默认→ Optuna 提升约+3~5%（复杂任务参数调优收益更大）",
], TEAL, 14, 12)

section_box(s, 0.5, 5.1, 12.3, 1.5, "⚠️  局限性", [
    "多分类准确率仍有提升空间（部分DGA家族样本量有限）",
    "Suppobox等家族随机化程度高，F1偏低（72.1%）",
    "目前仅离线验证，未部署在线环境",
], RED, 14, 12)

# ============================================================
# P14 家族级分析
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "04  多分类——家族级分析")

make_tbl(s, 6, 4, 0.8, 1.5, 11.5, 3.0,
    ["DGA家族", "F1-score", "样本量", "特征分析"],
    [["Kraken",   "92.3%", "40,000", "长度+字符分布特征明显"],
     ["Shiotob",  "91.8%", "35,000", "n-gram模式区分度高"],
     ["Bamital",  "90.5%", "30,000", "域名结构较为固定"],
     ["Pykspa",   "87.2%", "25,000", "随机化程度较高"],
     ["Suppobox", "72.1%", "8,000",  "样本量有限，模式随机"]])

add_shape(s, 0.5, 5.0, 12.3, 1.8, BLUE_BG)
add_text(s, 0.8, 5.1, 5, 0.35, "📌  分析结论", 14, BLUE2, True)
add_text(s, 0.8, 5.5, 11.5, 0.8,
    "统计特征对域名结构固化的家族（如Bamital）区分度好\n"
    "2-gram特征对字符模式差异大的家族（如Shiotob）更有效\n"
    "融合特征在所有家族上取得平衡最优表现", 13, TEXT)
add_text(s, 0.8, 6.4, 11.5, 0.3, "样本量 < 10,000 的家族 F1 明显偏低，说明数据量对多分类精度有显著影响", 12, RED, True)

# ============================================================
# P15 总结展望
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
page_header(s, "05  总结与展望")

section_box(s, 0.5, 1.5, 6, 3.5, "✅  工作总结", [
    "构建基于XGBoost的DGA检测系统",
    "系统对比4种特征工程方案",
    "引入Optuna贝叶斯优化自动调参",
    "二分类 F1 98.40% / AUC 0.9989",
    "多分类宏平均 F1 88.95%",
], BLUE2, 15, 13)

section_box(s, 7, 1.5, 6, 3.5, "🔭  未来展望", [
    "引入深度学习（CNN/LSTM）集成",
    "扩展到实时在线检测场景",
    "增加更多DGA家族样本覆盖",
    "探索主动学习半监督方法",
], RED, 15, 13)

add_shape(s, 0.5, 5.5, 12.3, 1.3, CARD)
add_text(s, 0.8, 5.6, 5, 0.35, "📊  核心指标", 15, BLUE, True)
add_text(s, 0.8, 6.0, 11.5, 0.6,
    "二分类：准确率 98.40%  |  F1 98.40%  |  AUC 0.9989\n"
    "多分类：宏平均 F1 88.95%  |  最优特征组合：统计 + 2-gram", 14, BLUE2, True)

# ============================================================
# P16 致谢
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_shape(s, 0, 0, 13.333, 7.5, BG_DARK)
add_shape(s, 0, 0, 13.333, 0.05, BLUE2)
add_shape(s, 0, 7.45, 13.333, 0.05, BLUE2)

add_text(s, 2, 1.5, 9, 1.0, "致  谢", 44, WHITE, True, PP_ALIGN.CENTER)
add_shape(s, 5.5, 2.6, 2.3, 0.02, BLUE2)

add_text(s, 2, 3.0, 9, 1.5, "感谢指导老师余玉银老师的悉心指导与耐心帮助\n"
         "感谢数学与信息科学学院各位老师的教诲与培养\n"
         "感谢家人和同学的支持与鼓励",
         17, TEXT2, a=PP_ALIGN.CENTER)

add_shape(s, 4.5, 5.2, 4.3, 0.02, TEXT2)
add_text(s, 2, 5.5, 9, 0.8, "请各位老师批评指正！", 26, WHITE, True, PP_ALIGN.CENTER)
add_text(s, 2, 6.3, 9, 0.4, "Q & A", 16, TEXT2, a=PP_ALIGN.CENTER)

# ===== 保存 =====
out = "/home/girlorn/Cloud-Security-Study/Graduation-Project/毕业答辩PPT.pptx"
prs.save(out)
print(f"✅ 保存: {out}")
print(f"共 {len(prs.slides)} 页")
