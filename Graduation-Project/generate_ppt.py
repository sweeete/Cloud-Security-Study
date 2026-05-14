#!/tmp/pptx-venv/bin/python3
"""优化版毕业答辩PPT — 更专业的排版和视觉设计"""
from pptx import Presentation
from pptx.util import Inches, Pt as EmuPt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn

def Pt(val):
    return EmuPt(val) if isinstance(val, int) else val

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ===== 颜色方案 =====
C = {
    "primary":   RGBColor(0x1B, 0x3A, 0x5C),  # 深蓝
    "secondary": RGBColor(0x2E, 0x86, 0xDE),  # 亮蓝
    "accent":    RGBColor(0xE7, 0x4C, 0x3C),  # 红色
    "green":     RGBColor(0x27, 0xAE, 0x60),  # 绿色
    "bg":        RGBColor(0x0B, 0x0E, 0x11),  # 深色背景
    "card":      RGBColor(0x16, 0x1B, 0x22),  # 卡片
    "card2":     RGBColor(0x1E, 0x23, 0x29),  # 浅卡片
    "text":      RGBColor(0xEA, 0xEC, 0xEF),  # 主文字
    "text2":     RGBColor(0xA0, 0xA8, 0xB4),  # 次要文字
    "white":     RGBColor(0xFF, 0xFF, 0xFF),
    "light_bg":  RGBColor(0xF4, 0xF6, 0xF9),  # 浅色背景
    "dark_text": RGBColor(0x2C, 0x3E, 0x50),  # 深色文字
    "muted":     RGBColor(0x7F, 0x8C, 0x9A),
    "highlight": RGBColor(0xE8, 0xF5, 0xE9),  # 高亮绿底
    "orange":    RGBColor(0xF3, 0x9C, 0x12),
}

def add_bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

def rect(slide, l, t, w, h, color, radius=None):
    shape = slide.shapes.add_shape(1, l, t, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    if radius:
        shape.adjustments[0] = radius
    return shape

def txt(slide, l, t, w, h, text, size=18, color=C["dark_text"], bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(l, t, w, h)
    box.text_frame.word_wrap = True
    p = box.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.alignment = align
    return box

def bullet_box(slide, l, t, w, h, items, size=16, color=C["dark_text"], spacing=10):
    box = slide.shapes.add_textbox(l, t, w, h)
    box.text_frame.word_wrap = True
    for i, item in enumerate(items):
        p = box.text_frame.paragraphs[0] if i == 0 else box.text_frame.add_paragraph()
        p.text = item
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(spacing)
    return box

def header_bar(slide, title, subtitle=""):
    """顶部标题栏"""
    rect(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), C["primary"])
    # 左侧装饰条
    rect(slide, Inches(0), Inches(0), Inches(0.15), Inches(1.2), C["secondary"])
    txt(slide, Inches(0.5), Inches(0.15), Inches(8), Inches(0.6), title, 28, C["white"], bold=True)
    if subtitle:
        txt(slide, Inches(0.5), Inches(0.7), Inches(8), Inches(0.4), subtitle, 14, C["text2"])
    # 页码
    n = len(prs.slides) + 1
    txt(slide, Inches(12), Inches(0.3), Inches(1), Inches(0.5), f"{n:02d}", 16, C["text2"], align=PP_ALIGN.RIGHT)

def make_table(slide, rows, cols, l, t, w, h, headers, data, highlight_row=None):
    """创建表格"""
    table = slide.shapes.add_table(rows, cols, l, t, w, h).table
    # 表头
    for j, hd in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = hd
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = C["white"]
        cell.fill.solid()
        cell.fill.fore_color.rgb = C["primary"]
    # 数据
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = table.cell(i+1, j)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.font.color.rgb = C["dark_text"]
                if highlight_row is not None and i == highlight_row:
                    p.font.color.rgb = C["green"]
                    p.font.bold = True
            if highlight_row is not None and i == highlight_row:
                cell.fill.solid()
                cell.fill.fore_color.rgb = C["highlight"]
            elif i % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xF8, 0xF9, 0xFA)
    return table

# ===========================================================================
# 第1页：封面
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["bg"])

# 装饰
rect(s, Inches(0), Inches(0), Inches(13.333), Inches(0.06), C["secondary"])
rect(s, Inches(0), Inches(7.44), Inches(13.333), Inches(0.06), C["secondary"])
rect(s, Inches(0.5), Inches(2.5), Inches(12.333), Inches(0.015), C["text2"])

txt(s, Inches(1), Inches(1.0), Inches(5), Inches(0.5), "本科毕业设计答辩", 16, C["text2"])
txt(s, Inches(1), Inches(1.8), Inches(11), Inches(1.2), "基于优化XGBoost的DGA检测系统设计", 36, C["white"], bold=True, align=PP_ALIGN.LEFT)
txt(s, Inches(1), Inches(2.7), Inches(11), Inches(0.6), "Design of DGA Detection System Based on Optimized XGBoost", 16, C["muted"])

# 信息区
info_items = [
    ("学    院：", "数学与信息科学学院"),
    ("专    业：", "信息安全"),
    ("班    级：", "信安221"),
    ("学生姓名：", "苑文洋"),
    ("学    号：", "32215300032"),
    ("指导教师：", "余玉银"),
]
y = 3.5
for label, val in info_items:
    txt(s, Inches(1), Inches(y), Inches(2), Inches(0.35), label, 15, C["text2"])
    txt(s, Inches(3), Inches(y), Inches(5), Inches(0.35), val, 15, C["white"])
    y += 0.45

# ===========================================================================
# 第2页：目录
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "目  录", "CONTENTS")

sections = [
    ("01", "研究背景与意义", "DGA威胁现状与检测挑战"),
    ("02", "相关理论与技术", "XGBoost / 贝叶斯优化 / 特征工程"),
    ("03", "系统设计与实现", "数据预处理 / 特征提取 / 模型训练"),
    ("04", "实验与分析", "二分类 / 多分类 / 结果对比"),
    ("05", "总结与展望", "创新点 / 不足 / 改进方向"),
]
for i, (num, title, desc) in enumerate(sections):
    y = 1.8 + i * 1.05
    rect(s, Inches(2), Inches(y), Inches(1.2), Inches(0.7), C["secondary"])
    txt(s, Inches(2.05), Inches(1.82+y-int(y)), Inches(1.1), Inches(0.5), num, 22, C["white"], bold=True, align=PP_ALIGN.CENTER)
    txt(s, Inches(3.5), Inches(y+0.02), Inches(6), Inches(0.4), title, 20, C["primary"], bold=True)
    txt(s, Inches(3.5), Inches(y+0.38), Inches(6), Inches(0.3), desc, 13, C["muted"])

# ===========================================================================
# 第3页：研究背景
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "01  研究背景与意义")

# 左侧：问题描述
rect(s, Inches(0.5), Inches(1.6), Inches(6), Inches(0.5), C["secondary"])
txt(s, Inches(0.7), Inches(1.65), Inches(5.5), Inches(0.4), "核心问题", 18, C["white"], bold=True)

bullet_box(s, Inches(0.5), Inches(2.3), Inches(6), Inches(3.5), [
    "DGA：僵尸网络逃避黑名单检测的核心手段",
    "攻击者通过算法生成随机域名，动态切换C2服务器",
    "传统黑名单/签名检测无法应对域名频繁变种",
    "单日可生成数万个域名，防御方难以预判",
], 15, C["dark_text"], 10)

# 右侧：解决方案
rect(s, Inches(7), Inches(1.6), Inches(6), Inches(0.5), C["accent"])
txt(s, Inches(7.2), Inches(1.65), Inches(5.5), Inches(0.4), "本文方案", 18, C["white"], bold=True)

bullet_box(s, Inches(7), Inches(2.3), Inches(6), Inches(3.5), [
    "基于XGBoost构建检测模型，兼顾效率与精度",
    "引入贝叶斯优化（Optuna）自动调参",
    "对比统计/N-gram/融合特征方案",
    "同时实现二分类（恶意检测）和多分类（家族溯源）",
], 15, C["dark_text"], 10)

# 底部研究目标
rect(s, Inches(0.5), Inches(5.8), Inches(12.3), Inches(1.2), RGBColor(0xEB, 0xF5, 0xFB))
txt(s, Inches(0.8), Inches(5.9), Inches(11.5), Inches(0.4), "🎯 研究目标", 16, C["secondary"], bold=True)
txt(s, Inches(0.8), Inches(6.3), Inches(11.5), Inches(0.5), "构建基于优化XGBoost的DGA检测系统，实现高效的二分类恶意域名检测与多分类家族溯源",
     14, C["dark_text"])

# ===========================================================================
# 第4页：DGA技术原理
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "02  DGA技术原理")

# 流程图：攻击链
rect(s, Inches(0.5), Inches(1.5), Inches(12.3), Inches(0.6), C["card"])
txt(s, Inches(0.7), Inches(1.55), Inches(4), Inches(0.4), "DGA攻击流程", 17, C["white"], bold=True)

steps = ["恶意软件感染", "DGA计算域名", "尝试连接", "注册C2", "执行指令"]
arrows = ["→", "→", "→", "→"]
for i, (step, arr) in enumerate(zip(steps, arrows + [""])):
    x = 0.8 + i * 2.5
    rect(s, Inches(x), Inches(2.4), Inches(2.0), Inches(0.7), C["secondary"] if i < 4 else C["accent"])
    txt(s, Inches(x), Inches(2.45), Inches(2.0), Inches(0.6), step, 13, C["white"], bold=True, align=PP_ALIGN.CENTER)
    if i < 4:
        txt(s, Inches(x+2.0), Inches(2.5), Inches(0.5), Inches(0.4), "→", 22, C["primary"], bold=True)

bullet_box(s, Inches(0.5), Inches(3.5), Inches(12.3), Inches(3.5), [
    "DGA核心逻辑：种子密钥 + 算法 → 批量生成域名 → 攻击者注册少量域名即可维持控制",
    "常见DGA家族：Suppobox（日期+字典）、Kraken（字符拼接）、Shiotob（时间种子）等",
    "检测难点：域名随机化程度高、不断变种、合法域名也可能被误报为恶意",
    "传统方法局限：黑名单无法预知未注册域名，规则匹配难以应对算法变种",
], 14, C["dark_text"], 8)

# ===========================================================================
# 第5页：XGBoost原理
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "02  XGBoost算法原理")

# 左栏
rect(s, Inches(0.5), Inches(1.5), Inches(6), Inches(0.5), C["secondary"])
txt(s, Inches(0.7), Inches(1.55), Inches(5), Inches(0.4), "核心机制", 18, C["white"], bold=True)

bullet_box(s, Inches(0.5), Inches(2.2), Inches(6), Inches(3.5), [
    "逐步添加决策树，每棵新树修正残差",
    "损失函数 = 训练误差 + 正则化项（L1+L2）",
    "二阶泰勒展开近似，收敛速度快于GBDT",
    "支持列采样、Shrinkage、早停防过拟合",
], 14, C["dark_text"], 8)

# 右栏
rect(s, Inches(7), Inches(1.5), Inches(6), Inches(0.5), C["green"])
txt(s, Inches(7.2), Inches(1.55), Inches(5), Inches(0.4), "选择XGBoost的原因", 18, C["white"], bold=True)

bullet_box(s, Inches(7), Inches(2.2), Inches(6), Inches(3.5), [
    "✅ 相比SVM：天然处理高维稀疏特征（10,000维N-gram）",
    "✅ 相比Random Forest：Boosting序列优化，偏差更低",
    "✅ 相比深度学习：训练速度快5~10倍，可解释性强",
    "✅ 相比单模型：集成多个弱分类器，方差低、泛化好",
], 14, C["dark_text"], 8)

# 底部公式
rect(s, Inches(0.5), Inches(5.6), Inches(12.3), Inches(1.5), C["card"])
txt(s, Inches(0.7), Inches(5.7), Inches(4), Inches(0.4), "目标函数", 16, C["white"], bold=True)
txt(s, Inches(0.7), Inches(6.1), Inches(11), Inches(0.8),
   "Obj = Σ L(yi, ŷi) + Σ Ω(fk)    其中 Ω(f) = γT + ½λ‖ω‖²\n"
   "L = 损失函数  |  Ω = 正则化项  |  T = 叶子节点数  |  ω = 叶子权重",
   13, C["text2"])

# ===========================================================================
# 第6页：特征工程
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "02  特征工程")

# 统计特征
rect(s, Inches(0.5), Inches(1.5), Inches(6), Inches(0.5), C["secondary"])
txt(s, Inches(0.7), Inches(1.55), Inches(5), Inches(0.4), "统计特征（6维）", 18, C["white"], bold=True)

stats = [
    "① 域名长度 — 正常 vs DGA 域名字符数差异",
    "② 数字占比 — DGA常含大量随机数字",
    "③ 信息熵 — 随机字符串熵值更高",
    "④ 连续辅音比例 — 恶意域名常出现辅音堆叠",
    "⑤ 重复字符比例 — 正常域名可读性强",
    "⑥ 元音占比 — 正常域名元音比例更高",
]
bullet_box(s, Inches(0.5), Inches(2.2), Inches(6), Inches(4), stats, 13, C["dark_text"], 6)

# N-gram特征
rect(s, Inches(7), Inches(1.5), Inches(6), Inches(0.5), C["green"])
txt(s, Inches(7.2), Inches(1.55), Inches(5), Inches(0.4), "N-gram 特征", 18, C["white"], bold=True)

ngram_items = [
    "将域名按n个连续字符滑动切分",
    "2-gram 示例：apple → ap pp pl le",
    "CountVectorizer 统计各组合频次",
    "取最频繁的10,000维作为特征",
    "捕捉微观字符序列模式差异",
]
bullet_box(s, Inches(7), Inches(2.2), Inches(6), Inches(3), ngram_items, 13, C["dark_text"], 6)

# 融合
rect(s, Inches(0.5), Inches(6.0), Inches(12.3), Inches(1.0), RGBColor(0xFE, 0xF3, 0xE0))
txt(s, Inches(0.7), Inches(6.1), Inches(11), Inches(0.7),
   "💡 融合特征策略：统计特征（宏观基准）+ 2-gram特征（微观指纹）→ 维度：6 + 10,000 = 10,006",
   14, C["orange"], bold=True)

# ===========================================================================
# 第7页：系统架构
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "03  系统设计——整体架构")

# 流程
flow = ["域名采集", "数据预处理", "特征提取", "模型训练", "结果评估"]
for i, step in enumerate(flow):
    x = 0.6 + i * 2.5
    color = C["secondary"] if i < 4 else C["green"]
    rect(s, Inches(x), Inches(1.7), Inches(2.0), Inches(0.8), color)
    txt(s, Inches(x), Inches(1.8), Inches(2.0), Inches(0.6), f"Step {i+1}", 11, C["white"], align=PP_ALIGN.CENTER)
    txt(s, Inches(x), Inches(2.1), Inches(2.0), Inches(0.4), step, 14, C["white"], bold=True, align=PP_ALIGN.CENTER)
    if i < 4:
        txt(s, Inches(x+2.0), Inches(1.85), Inches(0.5), Inches(0.5), "→", 20, C["primary"], bold=True)

details = [
    ("📥 数据采集", "Alexa 20万良性 + 360 DGA 20万恶意 = 40万样本"),
    ("🧹 数据预处理", "去重 → 去TLD → 8:1:1 划分训练/验证/测试集"),
    ("🔧 特征提取", "统计特征（6维）+ N-gram（CountVectorizer, top 10,000）"),
    ("⚙️ 模型训练", "XGBoost默认参数 vs Optuna贝叶斯优化"),
    ("📊 结果评估", "准确率 / 精确率 / 召回率 / F1 / AUC"),
]
for i, (title, desc) in enumerate(details):
    y = 2.9 + i * 0.75
    rect(s, Inches(1), Inches(y), Inches(1.8), Inches(0.5), C["card2"])
    txt(s, Inches(1.05), Inches(2.93+y-int(y)), Inches(1.7), Inches(0.4), title, 13, C["white"], bold=True)
    txt(s, Inches(3), Inches(y+0.02), Inches(9), Inches(0.45), desc, 13, C["dark_text"])

# ===========================================================================
# 第8页：数据预处理
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "03  数据预处理")

# 左栏
rect(s, Inches(0.5), Inches(1.5), Inches(6), Inches(0.5), C["secondary"])
txt(s, Inches(0.7), Inches(1.55), Inches(5), Inches(0.4), "处理流程", 18, C["white"], bold=True)

process_items = [
    "① 数据清洗：去除空值、重复域名（精确去重）",
    "② TLD剥离：去除.com/.net/.org等顶级域后缀",
    "③ 标签编码：良性域名→0，DGA家族→1~10",
    "④ 数据划分：训练集80% / 验证集10% / 测试集10%",
    "⑤ 特征标准化：N-gram使用CountVectorizer拟合",
]
bullet_box(s, Inches(0.5), Inches(2.2), Inches(6), Inches(3.5), process_items, 14, C["dark_text"], 8)

# 右栏
rect(s, Inches(7), Inches(1.5), Inches(6), Inches(0.5), C["accent"])
txt(s, Inches(7.2), Inches(1.55), Inches(5), Inches(0.4), "为什么去TLD？", 18, C["white"], bold=True)

tld_items = [
    "TLD是受控注册基准，对恶意检测无贡献",
    "DGA核心对抗逻辑在二级域名（前缀）",
    "去除TLD减少噪声，提升模型敏感度",
    "例：abc123.com → abc123（保留全部前缀）",
]
bullet_box(s, Inches(7), Inches(2.2), Inches(6), Inches(3), tld_items, 14, C["dark_text"], 8)

# 底部数据
rect(s, Inches(0.5), Inches(5.8), Inches(12.3), Inches(1.2), C["card2"])
txt(s, Inches(0.7), Inches(5.9), Inches(4), Inches(0.4), "📊 数据集统计", 16, C["white"], bold=True)
txt(s, Inches(0.7), Inches(6.3), Inches(11), Inches(0.6),
   "训练集：320,000条  |  验证集：40,000条  |  测试集：40,000条  |  共400,000条域名样本",
   14, C["text2"])

# ===========================================================================
# 第9页：实验设计—特征分组
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "04  实验设计——特征分组")

t = make_table(s, 5, 4,
    Inches(0.8), Inches(1.6), Inches(11.5), Inches(2.5),
    ["特征组", "特征组合", "说明", "维度"],
    [
        ["①", "统计特征", "6维统计特征", "6"],
        ["②", "2-gram 特征", "Bigram切片 + CountVectorizer", "10,000"],
        ["③", "2-4gram 特征", "混合切片（2/3/4字符）", "10,000"],
        ["④", "统计 + 2-gram", "融合特征（最优组合）", "10,006"],
    ])

txt(s, Inches(0.8), Inches(4.5), Inches(10), Inches(0.5), "实验设置", 20, C["primary"], bold=True)
bullet_box(s, Inches(0.8), Inches(5.0), Inches(11), Inches(2), [
    "实验一（二分类）：区分恶意域名（DGA）和良性域名（Alexa）",
    "实验二（多分类）：对10个DGA家族进行细粒度分类",
    "每组特征分别在 XGBoost 默认参数和 Optuna 贝叶斯优化下各运行一次",
    "评估指标：准确率、精确率、召回率、F1-score、AUC（二分类）",
], 14, C["dark_text"], 8)

# ===========================================================================
# 第10页：二分类结果
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "04  实验结果——二分类")

# 最佳结果横幅
rect(s, Inches(0.5), Inches(1.5), Inches(12.3), Inches(1.0), C["highlight"])
txt(s, Inches(0.7), Inches(1.55), Inches(1.5), Inches(0.4), "🏆 最优结果", 16, C["green"], bold=True)
txt(s, Inches(0.7), Inches(1.9), Inches(11.5), Inches(0.5),
   "统计特征 + 2-gram 融合组 + Optuna贝叶斯优化 → 准确率 98.40% | F1 98.40% | AUC 0.9989",
   15, C["green"], bold=True)

t = make_table(s, 7, 7,
    Inches(0.3), Inches(2.8), Inches(12.7), Inches(4.2),
    ["特征组", "优化", "准确率", "精确率", "召回率", "F1", "AUC"],
    [
        ["统计特征",    "默认参数", "95.87%", "95.97%", "95.77%", "95.87%", "0.9931"],
        ["统计特征",    "Optuna",   "96.12%", "96.48%", "95.76%", "96.12%", "0.9948"],
        ["2-gram",     "默认参数", "97.53%", "97.44%", "97.63%", "97.53%", "0.9979"],
        ["2-gram",     "Optuna",   "97.69%", "97.72%", "97.66%", "97.69%", "0.9981"],
        ["统计+2-gram", "默认参数", "98.10%", "98.39%", "97.81%", "98.10%", "0.9984"],
        ["统计+2-gram", "Optuna",   "98.40%", "98.47%", "98.33%", "98.40%", "0.9989"],
    ], highlight_row=5)

# ===========================================================================
# 第11页：多分类结果
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "04  实验结果——多分类")

rect(s, Inches(0.5), Inches(1.5), Inches(12.3), Inches(0.8), C["highlight"])
txt(s, Inches(0.7), Inches(1.6), Inches(11), Inches(0.5),
   "🏆 最优结果：统计特征 + 2-gram 融合组 → 宏平均 F1 = 88.95%", 16, C["green"], bold=True)

t = make_table(s, 5, 4,
    Inches(1.5), Inches(2.6), Inches(10), Inches(2.5),
    ["特征组", "准确率", "宏平均 F1", "说明"],
    [
        ["统计特征",        "65.59%", "53.78%", "宏观基准定位，区分度有限"],
        ["2-gram 特征",     "84.46%", "76.80%", "微观指纹提取，效果显著"],
        ["2-4gram 特征",    "85.55%", "77.70%", "相比2-gram提升有限"],
        ["统计 + 2-gram",   "89.98%", "88.95%", "✅ 最优组合，优势明确"],
    ], highlight_row=3)

rect(s, Inches(0.5), Inches(5.5), Inches(12.3), Inches(1.5), RGBColor(0xFD, 0xF0, 0xED))
txt(s, Inches(0.7), Inches(5.6), Inches(4), Inches(0.4), "📌 分析发现", 14, C["accent"], bold=True)
bullet_box(s, Inches(0.7), Inches(6.0), Inches(11), Inches(1.0), [
    "统计特征 → 宏观基准定位  |  2-gram特征 → 微观指纹修正  |  融合 → 互补增益",
    "贝叶斯优化：二分类提升约+0.3%，多分类提升约+3~5%（复杂任务收益更大）",
], 13, C["dark_text"], 6)

# ===========================================================================
# 第12页：Optuna优化
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "03  Optuna贝叶斯优化")

rect(s, Inches(0.5), Inches(1.5), Inches(12.3), Inches(0.6), C["secondary"])
txt(s, Inches(0.7), Inches(1.55), Inches(11), Inches(0.4),
   "优化流程：定义目标函数 → Optuna搜索超参数空间 → 自动剪枝 → 输出最优参数集", 15, C["white"], bold=True)

# 左栏：参数范围
rect(s, Inches(0.5), Inches(2.5), Inches(6), Inches(0.45), C["primary"])
txt(s, Inches(0.7), Inches(2.53), Inches(5), Inches(0.35), "超参数搜索范围", 15, C["white"], bold=True)

params = [
    "learning_rate:   [0.01, 0.3]      学习率",
    "max_depth:       [3, 12]             树深度",
    "n_estimators:    [50, 500]           树数量",
    "subsample:       [0.6, 1.0]        样本采样",
    "colsample_bytree: [0.6, 1.0]        特征采样",
    "reg_lambda:      [0, 5]               L2正则化",
]
bullet_box(s, Inches(0.5), Inches(3.15), Inches(6), Inches(3), params, 13, C["dark_text"], 6)

# 右栏：优化效果
rect(s, Inches(7), Inches(2.5), Inches(6), Inches(0.45), C["green"])
txt(s, Inches(7.2), Inches(2.53), Inches(5), Inches(0.35), "优化效果对比", 15, C["white"], bold=True)

opt_effects = [
    "默认 vs Optuna（统计+2-gram / 二分类）：",
    "  准确率：98.10% → 98.40%  ▲ +0.30%",
    "  F1：      98.10% → 98.40%  ▲ +0.30%",
    "  AUC：    0.9984 → 0.9989 ▲ +0.0005",
    "",
    "多分类提升更显著：约 +3~5%",
    "搜索效率：50~100次试验即可收敛",
]
bullet_box(s, Inches(7), Inches(3.15), Inches(6), Inches(3.5), opt_effects, 13, C["dark_text"], 5)

# ===========================================================================
# 第13页：结果分析
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "04  结果分析")

findings = [
    ("📊 特征对比", C["secondary"], [
        "统计特征：宏观基准定位，单独使用效果有限（F1 53.78%多分类）",
        "2-gram特征：微观指纹提取，效果显著优于统计特征（F1 76.80%）",
        "融合特征：两者互补，取得最优结果（F1 88.95% / 98.40%）",
        "2-4gram vs 2-gram：提升有限，融合时出现增益递减",
    ]),
    ("⚙️ 优化对比", C["green"], [
        "贝叶斯优化相比默认参数普遍提升模型性能",
        "二分类：提升约 +0.3%（已接近理论上限，AUC > 0.99）",
        "多分类：提升约 +3~5%（参数调优对复杂任务收益更大）",
    ]),
    ("⚠️ 局限性", C["accent"], [
        "多分类准确率仍有提升空间（部分家族样本量有限）",
        "Suppobox等家族随机化程度高，分类精度偏低",
        "目前仅针对离线数据集验证，未部署到在线环境",
    ]),
]

y = 1.6
for title, color, items in findings:
    rect(s, Inches(0.5), Inches(y), Inches(12.3), Inches(0.45), color)
    txt(s, Inches(0.7), Inches(y+0.03), Inches(4), Inches(0.35), title, 15, C["white"], bold=True)
    bullet_box(s, Inches(0.5), Inches(y+0.55), Inches(12.3), Inches(1.2), items, 13, C["dark_text"], 5)
    y += 1.8

# ===========================================================================
# 第14页：创新点
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "创  新  点")

innovs = [
    ("🌟 特征融合策略创新",
     "系统对比了统计特征、N-gram及其融合方案，揭示了统计特征（宏观）与2-gram特征（微观）的正交互补机制"),
    ("🌟 优化方法创新",
     "引入Optuna贝叶斯优化替代传统网格搜索，调参效率提升10倍以上，且在复杂分类任务中效果显著"),
    ("🌟 统一检测框架",
     "同一框架同时支持二分类（恶意域名检测）和多分类（DGA家族溯源），具有实际应用价值"),
    ("🌟 深入的特征正交性分析",
     "通过多组对比实验，量化了不同特征维度对模型性能的贡献，为后续研究提供了参考基准"),
]

for i, (title, desc) in enumerate(innovs):
    y = 1.6 + i * 1.35
    rect(s, Inches(0.5), Inches(y), Inches(0.06), Inches(1.0), C["secondary"])
    txt(s, Inches(0.8), Inches(y), Inches(5), Inches(0.35), title, 17, C["primary"], bold=True)
    txt(s, Inches(0.8), Inches(y+0.4), Inches(11.5), Inches(0.6), desc, 13, C["dark_text"])

# ===========================================================================
# 第15页：总结与展望
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["light_bg"])
header_bar(s, "05  总结与展望")

# 总结
rect(s, Inches(0.5), Inches(1.5), Inches(6), Inches(0.5), C["secondary"])
txt(s, Inches(0.7), Inches(1.55), Inches(5), Inches(0.4), "✅  工作总结", 18, C["white"], bold=True)

summary = [
    "构建了基于XGBoost的DGA检测系统（二分类+多分类）",
    "系统对比4种特征工程方案，确定最优组合",
    "引入Optuna贝叶斯优化自动调参",
    "二分类 F1 98.40% / AUC 0.9989",
    "多分类宏平均 F1 88.95%",
]
bullet_box(s, Inches(0.5), Inches(2.2), Inches(6), Inches(3), summary, 14, C["dark_text"], 6)

# 展望
rect(s, Inches(7), Inches(1.5), Inches(6), Inches(0.5), C["accent"])
txt(s, Inches(7.2), Inches(1.55), Inches(5), Inches(0.4), "🔭  未来展望", 18, C["white"], bold=True)

future = [
    "引入深度学习（CNN/LSTM）与XGBoost集成",
    "扩展到实时在线检测场景",
    "增加更多DGA家族样本覆盖",
    "探索主动学习半监督方法",
]
bullet_box(s, Inches(7), Inches(2.2), Inches(6), Inches(3), future, 14, C["dark_text"], 6)

# 底部关键数据
rect(s, Inches(0.5), Inches(5.8), Inches(12.3), Inches(1.2), C["card2"])
txt(s, Inches(0.7), Inches(5.9), Inches(4), Inches(0.4), "📊 核心指标一览", 16, C["white"], bold=True)
key_stats = "二分类：准确率 98.40% | F1 98.40% | AUC 0.9989    " + \
            "多分类：宏平均 F1 88.95% | 最优特征：统计 + 2-gram"
txt(s, Inches(0.7), Inches(6.3), Inches(11.5), Inches(0.5), key_stats, 15, C["secondary"], bold=True)

# ===========================================================================
# 第16页：致谢
# ===========================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, C["bg"])
rect(s, Inches(0), Inches(0), Inches(13.333), Inches(0.06), C["secondary"])
rect(s, Inches(0), Inches(7.44), Inches(13.333), Inches(0.06), C["secondary"])

txt(s, Inches(1.5), Inches(1.8), Inches(10), Inches(1.0), "致  谢", 42, C["white"], bold=True, align=PP_ALIGN.CENTER)
rect(s, Inches(5.5), Inches(2.8), Inches(2.3), Inches(0.02), C["secondary"])

txt(s, Inches(1.5), Inches(3.2), Inches(10), Inches(1.5),
   "感谢指导老师 余玉银 老师的悉心指导与耐心帮助\n"
   "感谢数学与信息科学学院各位老师的教诲与培养\n"
   "感谢家人和同学的支持与鼓励",
   18, C["text2"], align=PP_ALIGN.CENTER)

rect(s, Inches(3.5), Inches(5.5), Inches(6.3), Inches(0.015), C["text2"])
txt(s, Inches(1.5), Inches(5.8), Inches(10), Inches(0.8), "请各位老师批评指正！", 26, C["white"], bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(1.5), Inches(6.5), Inches(10), Inches(0.4), "Q & A", 18, C["text2"], align=PP_ALIGN.CENTER)

# ===== 保存 =====
out = "/home/girlorn/Cloud-Security-Study/Graduation-Project/毕业答辩PPT.pptx"
prs.save(out)
print(f"✅ PPT 已保存: {out}")
print(f"共 {len(prs.slides)} 页")
