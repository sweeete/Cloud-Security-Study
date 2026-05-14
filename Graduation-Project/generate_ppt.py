#!/tmp/pptx-venv/bin/python3
"""生成毕业答辩PPT"""
from pptx import Presentation
from pptx.util import Inches, Pt as EmuPt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def Pt(val):
    """安全转换pt值，避免重复转换"""
    return EmuPt(val) if isinstance(val, int) else val

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

BLUE = RGBColor(0x1A, 0x3C, 0x6E)
LIGHT_BLUE = RGBColor(0x2D, 0x6D, 0xCC)
DARK = RGBColor(0x33, 0x33, 0x33)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x66, 0x66, 0x66)
LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)
ACCENT = RGBColor(0xE8, 0x4C, 0x3D)
GREEN = RGBColor(0x27, 0xAE, 0x60)

def add_bg(slide, color=BLUE):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

def add_rect(slide, left, top, width, height, color):
    shape = slide.shapes.add_shape(1, left, top, width, height)  # 1 = MSO_SHAPE.RECTANGLE
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def tb(slide, left, top, width, height, text, size=18, color=DARK, bold=False, align=PP_ALIGN.LEFT):
    """添加文本框"""
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.alignment = align
    return box

def bullets(slide, left, top, width, height, items, size=16, color=DARK):
    """添加列表"""
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(8)
    return box

# ===== 幻灯片 =====

# 封面
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, BLUE)
add_rect(s, Inches(0), Inches(0), Inches(0.3), Inches(7.5), LIGHT_BLUE)
tb(s, Inches(1.5), Inches(1.0), Inches(10), Inches(1.0), "本科毕业设计答辩", 28, WHITE, align=PP_ALIGN.CENTER)
tb(s, Inches(1.5), Inches(2.2), Inches(10), Inches(1.2), "基于优化XGBoost的DGA检测系统设计", 36, WHITE, bold=True, align=PP_ALIGN.CENTER)
add_rect(s, Inches(4), Inches(3.6), Inches(5.3), Inches(0.04), LIGHT_BLUE)
info = ["学    院：数学与信息科学学院","专    业：信息安全","班    级：信安221","学生姓名：苑文洋","学    号：32215300032","指导教师：余玉银"]
bullets(s, Inches(4), Inches(4.0), Inches(6), Inches(3), info, 18, RGBColor(0xCC,0xDD,0xFF))

# 目录
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(5), Inches(0.8), "目  录", 32, WHITE, bold=True)
toc = ["01   研究背景与意义","02   相关理论与技术","03   系统设计与实现","04   实验与分析","05   总结与展望"]
for i, item in enumerate(toc):
    tb(s, Inches(2), Inches(1.8+i*0.9), Inches(9), Inches(0.7), item, 24, DARK)

# 研究背景
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(8), Inches(0.8), "01  研究背景与意义", 32, WHITE, bold=True)
bullets(s, Inches(0.8), Inches(1.6), Inches(11.5), Inches(4), [
    "DGA是僵尸网络逃避黑名单检测的核心手段",
    "攻击者通过算法生成随机域名，绕过传统黑名单机制",
    "传统方法（哈希匹配、规则匹配）难以应对变种",
    "机器学习方法泛化能力强，能检测未知变种",
    "XGBoost在效率和精度之间取得良好平衡"
], 17, DARK)
add_rect(s, Inches(0.8), Inches(5.8), Inches(11.5), Inches(1.2), LIGHT_GRAY)
tb(s, Inches(1.0), Inches(5.9), Inches(11), Inches(1.0), "💡 目标：构建基于优化XGBoost的DGA检测系统，实现二分类（恶意/良性）和多分类（家族溯源）", 15, LIGHT_BLUE, bold=True)

# 相关技术
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(8), Inches(0.8), "02  相关理论与技术", 32, WHITE, bold=True)

add_rect(s, Inches(0.5), Inches(1.6), Inches(5.8), Inches(0.6), LIGHT_BLUE)
tb(s, Inches(0.7), Inches(1.65), Inches(5), Inches(0.5), "XGBoost", 20, WHITE, bold=True)
bullets(s, Inches(0.7), Inches(2.4), Inches(5.5), Inches(2.5), [
    "基于梯度提升决策树的优化算法",
    "引入正则化项防止过拟合",
    "支持并行计算，训练效率高",
    "自动处理缺失值，内置剪枝策略"
], 14, DARK)

add_rect(s, Inches(7), Inches(1.6), Inches(5.8), Inches(0.6), GREEN)
tb(s, Inches(7.2), Inches(1.65), Inches(5), Inches(0.5), "贝叶斯优化（Optuna）", 20, WHITE, bold=True)
bullets(s, Inches(7.2), Inches(2.4), Inches(5.5), Inches(2.5), [
    "基于高斯过程的超参数优化",
    "相比网格/随机搜索效率更高",
    "支持自动剪枝和可视化",
    "有效探索超参数空间"
], 14, DARK)

add_rect(s, Inches(0.5), Inches(5.0), Inches(12.3), Inches(0.6), LIGHT_BLUE)
tb(s, Inches(0.7), Inches(5.05), Inches(5), Inches(0.5), "特征工程", 20, WHITE, bold=True)
bullets(s, Inches(0.7), Inches(5.8), Inches(11.5), Inches(1.5), [
    "统计特征（6维）：长度、数字占比、信息熵、连续辅音比例、重复字符比例、元音占比",
    "N-gram 特征：2-gram / 2-4gram，CountVectorizer 映射，前 10,000 高频组合"
], 14, DARK)

# 系统架构
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(10), Inches(0.8), "03  系统设计——整体架构", 32, WHITE, bold=True)

steps = ["域名数据采集", "数据预处理", "特征提取", "模型训练", "检测评估"]
for i, step in enumerate(steps):
    x = 0.8 + i * 2.5
    c = ACCENT if i == 4 else LIGHT_BLUE
    add_rect(s, Inches(x), Inches(2.0), Inches(2.0), Inches(0.8), c)
    tb(s, Inches(x), Inches(2.1), Inches(2.0), Inches(0.6), step, 14, WHITE, bold=True, align=PP_ALIGN.CENTER)
    if i < 4:
        tb(s, Inches(x+2.0), Inches(2.15), Inches(0.5), Inches(0.5), "→", 20, BLUE, bold=True)

bullets(s, Inches(0.8), Inches(3.5), Inches(11.5), Inches(3.5), [
    "数据源：Alexa 20万 + 360 DGA 20万 = 40万样本，8:1:1 划分",
    "预处理：去重、去TLD、正则化",
    "特征：统计特征（6维）+ N-gram（CountVectorizer, top 10,000）",
    "模型：XGBoost 默认 vs Optuna 贝叶斯优化",
    "评估：准确率、精确率、召回率、F1、AUC"
], 16, DARK)

# 实验设计
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(10), Inches(0.8), "04  实验设计——特征分组", 32, WHITE, bold=True)

t = s.shapes.add_table(5, 4, Inches(0.8), Inches(1.8), Inches(11.5), Inches(2.5)).table
for j, h in enumerate(["特征组编号","特征组合","说明","维度"]):
    c = t.cell(0, j); c.text = h
    for p in c.text_frame.paragraphs: p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = WHITE
    c.fill.solid(); c.fill.fore_color.rgb = BLUE

for i, row in enumerate([["①","统计特征","6维统计特征","6"],["②","2-gram 特征","Bigram + CountVectorizer","10,000"],
                          ["③","2-4gram 特征","混合切片","10,000"],["④","统计+2-gram","融合特征","10,006"]]):
    for j, val in enumerate(row):
        c = t.cell(i+1, j); c.text = val
        for p in c.text_frame.paragraphs: p.font.size = Pt(13); p.font.color.rgb = DARK
        if i % 2 == 0: c.fill.solid(); c.fill.fore_color.rgb = RGBColor(0xEE,0xF2,0xF7)

tb(s, Inches(0.8), Inches(4.6), Inches(10), Inches(0.5), "二分类 vs 多分类实验", 20, BLUE, bold=True)
bullets(s, Inches(0.8), Inches(5.2), Inches(11), Inches(2), [
    "二分类：区分恶意域名（DGA）和良性域名（Alexa）",
    "多分类：对 10 个 DGA 家族细粒度分类",
    "每组特征在 XGBoost 默认参数和贝叶斯优化下分别实验"
], 15, DARK)

# 二分类结果
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(10), Inches(0.8), "04  实验结果——二分类", 32, WHITE, bold=True)

add_rect(s, Inches(0.8), Inches(1.6), Inches(11.5), Inches(1.2), RGBColor(0xE8,0xF5,0xE9))
tb(s, Inches(1.0), Inches(1.7), Inches(11), Inches(1.0), "🏆 统计特征+2-gram + Optuna：准确率98.40% | F1 98.40% | AUC 0.9989", 18, GREEN, bold=True)

t = s.shapes.add_table(7, 7, Inches(0.5), Inches(3.2), Inches(12.3), Inches(4.0)).table
for j, h in enumerate(["特征组","优化","准确率","精确率","召回率","F1","AUC"]):
    c = t.cell(0, j); c.text = h
    for p in c.text_frame.paragraphs: p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = WHITE
    c.fill.solid(); c.fill.fore_color.rgb = BLUE

for i, row in enumerate([
    ["统计","默认","95.87%","95.97%","95.77%","95.87%","0.9931"],
    ["统计","Optuna","96.12%","96.48%","95.76%","96.12%","0.9948"],
    ["2-gram","默认","97.53%","97.44%","97.63%","97.53%","0.9979"],
    ["2-gram","Optuna","97.69%","97.72%","97.66%","97.69%","0.9981"],
    ["统计+2-gram","默认","98.10%","98.39%","97.81%","98.10%","0.9984"],
    ["统计+2-gram","Optuna","98.40%","98.47%","98.33%","98.40%","0.9989"]]):
    for j, val in enumerate(row):
        c = t.cell(i+1, j); c.text = val
        for p in c.text_frame.paragraphs: p.font.size = Pt(12); p.font.color.rgb = DARK
        if i >= 4: p.font.color.rgb = GREEN; p.font.bold = True
    if i % 2 == 0: c.fill.solid(); c.fill.fore_color.rgb = RGBColor(0xF8,0xF9,0xFA)

# 多分类结果
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(10), Inches(0.8), "04  实验结果——多分类", 32, WHITE, bold=True)

add_rect(s, Inches(0.8), Inches(1.6), Inches(11.5), Inches(1.0), RGBColor(0xE8,0xF5,0xE9))
tb(s, Inches(1.0), Inches(1.7), Inches(11), Inches(0.8), "🏆 统计+2-gram 融合组 → 宏平均 F1 88.95%", 18, GREEN, bold=True)

t = s.shapes.add_table(5, 4, Inches(1.5), Inches(3.0), Inches(10), Inches(2.5)).table
for j, h in enumerate(["特征组","准确率","宏平均F1","说明"]):
    c = t.cell(0, j); c.text = h
    for p in c.text_frame.paragraphs: p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = WHITE
    c.fill.solid(); c.fill.fore_color.rgb = BLUE

for i, row in enumerate([
    ["统计特征","65.59%","53.78%","宏观基准定位"],
    ["2-gram","84.46%","76.80%","微观指纹提取"],
    ["2-4gram","85.55%","77.70%","特征冗余增加"],
    ["统计+2-gram","89.98%","88.95%","✅ 最优"]]):
    for j, val in enumerate(row):
        c = t.cell(i+1, j); c.text = val
        for p in c.text_frame.paragraphs: p.font.size = Pt(12); p.font.color.rgb = DARK
    if i == 3:
        c.fill.solid(); c.fill.fore_color.rgb = RGBColor(0xE8,0xF5,0xE9)

# 结果分析
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(10), Inches(0.8), "04  结果分析", 32, WHITE, bold=True)

bullets(s, Inches(0.8), Inches(1.6), Inches(11.5), Inches(4), [
    "统计特征 → 宏观基准定位；2-gram特征 → 微观指纹提取；融合 → 最优",
    "贝叶斯优化相比默认参数，二分类提升约+0.3%，多分类提升约+3~5%",
    "2-4gram 相比 2-gram 提升有限，融合后出现增益递减",
    "二分类 AUC 达 0.9989，接近完美分类",
    "「统计+2-gram」为最优组合，兼顾性能与效率"
], 16, DARK)

add_rect(s, Inches(0.8), Inches(5.8), Inches(11.5), Inches(1.0), RGBColor(0xFD,0xF0,0xED))
tb(s, Inches(1.0), Inches(5.9), Inches(11), Inches(0.8),
   "⚠️ 局限：多分类准确率仍有提升空间；部分DGA家族样本量有限，影响分类精度", 14, ACCENT, bold=True)

# 总结与展望
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(8), Inches(0.8), "05  总结与展望", 32, WHITE, bold=True)

add_rect(s, Inches(0.8), Inches(1.6), Inches(5.5), Inches(0.5), LIGHT_BLUE)
tb(s, Inches(1.0), Inches(1.65), Inches(5), Inches(0.4), "✅ 工作总结", 18, WHITE, bold=True)
bullets(s, Inches(1.0), Inches(2.3), Inches(5), Inches(3), [
    "构建XGBoost DGA检测系统",
    "对比多种特征工程方案",
    "引入贝叶斯优化自动调参",
    "二分类F1 98.40%，多分类F1 88.95%"
], 14, DARK)

add_rect(s, Inches(7), Inches(1.6), Inches(5.5), Inches(0.5), ACCENT)
tb(s, Inches(7.2), Inches(1.65), Inches(5), Inches(0.4), "🔭 未来展望", 18, WHITE, bold=True)
bullets(s, Inches(7.2), Inches(2.3), Inches(5), Inches(3), [
    "引入深度学习（CNN/LSTM）集成",
    "扩展到实时在线检测",
    "增加更多DGA家族样本",
    "探索主动学习半监督方法"
], 14, DARK)

# 创新点
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(10), Inches(0.8), "创新点", 32, WHITE, bold=True)

bullets(s, Inches(0.8), Inches(1.8), Inches(11.5), Inches(4.5), [
    "🌟 特征融合策略：系统对比统计/N-gram/融合方案的性能差异",
    "🌟 贝叶斯优化：引入Optuna替代网格搜索，提升调参效率10倍以上",
    "🌟 统一框架：同时支持恶意域名检测和DGA家族溯源",
    "🌟 正交性分析：揭示统计特征（宏观）与N-gram特征（微观）的互补机制"
], 16, DARK)

# ===== DGA技术原理 =====
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(10), Inches(0.8), "02   DGA技术原理", 32, WHITE, bold=True)
bullets(s, Inches(0.8), Inches(1.6), Inches(11.5), Inches(5), [
    "DGA (Domain Generation Algorithm)：恶意软件动态生成大量候选域名",
    "种子 + 算法 → 每日/每周生成数百数千个域名",
    "攻击者只需注册其中少数几个即可维持C2通信",
    "防御方难以预判和封锁所有域名",
    "主流DGA家族：Suppobox、Kraken、Shiotob、Pykspa、Bamital等",
    "检测难点：域名随机化程度高、不断变种、合法域名也可能被误报"
], 16, DARK)

# ===== XGBoost算法原理 =====
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(10), Inches(0.8), "02   XGBoost算法原理", 32, WHITE, bold=True)

add_rect(s, Inches(0.8), Inches(1.6), Inches(5.8), Inches(0.5), LIGHT_BLUE)
tb(s, Inches(1.0), Inches(1.65), Inches(5), Inches(0.5), "梯度提升框架", 18, WHITE, bold=True)
bullets(s, Inches(1.0), Inches(2.3), Inches(5.5), Inches(2.5), [
    "逐步添加决策树，每棵新树修正前树残差",
    "目标函数 = 损失函数 + 正则化项",
    "二阶泰勒展开近似损失，收敛更快",
    "支持列采样、缩减（shrinkage）防过拟合"
], 14, DARK)

add_rect(s, Inches(7), Inches(1.6), Inches(5.5), Inches(0.5), GREEN)
tb(s, Inches(7.2), Inches(1.65), Inches(5), Inches(0.5), "相比传统方法的优势", 18, WHITE, bold=True)
bullets(s, Inches(7.2), Inches(2.3), Inches(5.5), Inches(2.5), [
    "相比随机森林：Boosting序列优化，偏差更低",
    "相比SVM：天然处理高维稀疏特征",
    "相比深度学习：训练速度快，可解释性强",
    "相比单决策树：集成多个弱分类器，方差降低"
], 14, DARK)

# ===== 数据预处理细节 =====
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(10), Inches(0.8), "03   数据预处理流程", 32, WHITE, bold=True)

# 左栏
add_rect(s, Inches(0.5), Inches(1.6), Inches(6), Inches(0.5), LIGHT_BLUE)
tb(s, Inches(0.7), Inches(1.65), Inches(5), Inches(0.5), "数据处理步骤", 18, WHITE, bold=True)
bullets(s, Inches(0.7), Inches(2.3), Inches(5.8), Inches(4), [
    "① 数据采集：Alexa 20万 + 360 DGA 20万",
    "② 数据清洗：去除空值、重复域名",
    "③ TLD 剥离：去除.com/.net/.org等顶级域后缀",
    "④ 标签编码：良性→0，DGA家族→1~10",
    "⑤ 数据集划分：8:1:1（训练/验证/测试）",
    "⑥ 特征标准化：N-gram特征使用CountVectorizer"
], 14, DARK)

# 右栏
add_rect(s, Inches(7), Inches(1.6), Inches(5.8), Inches(0.5), ACCENT)
tb(s, Inches(7.2), Inches(1.65), Inches(5), Inches(0.5), "为什么去TLD？", 18, WHITE, bold=True)
bullets(s, Inches(7.2), Inches(2.3), Inches(5.5), Inches(4), [
    "TLD是受控注册基准，对恶意检测无贡献",
    "DGA核心对抗逻辑在前缀（二级域名）",
    "去除TLD可减少噪声，增强模型敏感度",
    "例如：abc123.com → abc123",
    "保留所有子域名层级，点号视为分隔符",
    "平均域名长度约12~20字符"
], 14, DARK)

# ===== 特征工程详解 =====
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(10), Inches(0.8), "03   特征工程详解", 32, WHITE, bold=True)

add_rect(s, Inches(0.5), Inches(1.6), Inches(6), Inches(0.5), LIGHT_BLUE)
tb(s, Inches(0.7), Inches(1.65), Inches(5), Inches(0.5), "统计特征（6维）", 18, WHITE, bold=True)
bullets(s, Inches(0.7), Inches(2.3), Inches(5.8), Inches(4), [
    "① 域名长度：正常域名 vs DGA 域名字符数差异",
    "② 数字占比：DGA常含随机数字",
    "③ 信息熵：随机字符串熵值更高",
    "④ 连续辅音比例：恶意域名常出现辅音堆叠",
    "⑤ 重复字符比例：正常域名更易记忆，重复高",
    "⑥ 元音占比：正常域名可读性强，元音占比高"
], 14, DARK)

add_rect(s, Inches(7), Inches(1.6), Inches(5.8), Inches(0.5), GREEN)
tb(s, Inches(7.2), Inches(1.65), Inches(5), Inches(0.5), "N-gram 特征", 18, WHITE, bold=True)
bullets(s, Inches(7.2), Inches(2.3), Inches(5.5), Inches(4), [
    "将域名按n个连续字符切分（滑动窗口）",
    "2-gram：ap→pp→pl→le 等字符对",
    "2-4gram：混合2/3/4字符组合",
    "CountVectorizer 统计各组合出现频次",
    "取最频繁的10,000维作为特征",
    "捕捉微观字符序列模式差异"
], 14, DARK)

# ===== Optuna优化过程 =====
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(10), Inches(0.8), "03   贝叶斯优化——Optuna", 32, WHITE, bold=True)

add_rect(s, Inches(0.8), Inches(1.6), Inches(11.5), Inches(0.6), LIGHT_BLUE)
tb(s, Inches(1.0), Inches(1.65), Inches(10), Inches(0.5), "优化流程：定义目标函数 → 搜索超参数空间 → Optuna自动剪枝 → 输出最优参数", 16, WHITE, bold=True)

# 左栏
add_rect(s, Inches(0.5), Inches(2.6), Inches(6), Inches(0.5), BLUE)
tb(s, Inches(0.7), Inches(2.65), Inches(5), Inches(0.5), "优化参数范围", 16, WHITE, bold=True)
bullets(s, Inches(0.7), Inches(3.3), Inches(5.8), Inches(3.5), [
    "learning_rate: [0.01, 0.3]   学习率",
    "max_depth: [3, 12]                  树的最大深度",
    "n_estimators: [50, 500]         树的数量",
    "subsample: [0.6, 1.0]            样本采样比例",
    "colsample_bytree: [0.6, 1.0]  特征采样比例",
    "reg_lambda: [0, 5]                  L2正则化"
], 14, DARK)

# 右栏
add_rect(s, Inches(7), Inches(2.6), Inches(5.8), Inches(0.5), GREEN)
tb(s, Inches(7.2), Inches(2.65), Inches(5), Inches(0.5), "优化结果示例", 16, WHITE, bold=True)
bullets(s, Inches(7.2), Inches(3.3), Inches(5.5), Inches(3.5), [
    "Optuna vs 默认参数（统计+2-gram组）：",
    "  准确率提升: 98.10% → 98.40% (+0.3%)",
    "  F1提升: 98.10% → 98.40% (+0.3%)",
    "  多分类提升更为显著：约+3~5%",
    "搜索效率：50~100次试验即可收敛",
    "相比网格搜索：效率提升10倍以上"
], 14, DARK)

# 实验结果对比补充
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, WHITE)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
tb(s, Inches(0.5), Inches(0.2), Inches(10), Inches(0.8), "04   多分类——家族级分析", 32, WHITE, bold=True)

bullets(s, Inches(0.8), Inches(1.6), Inches(11.5), Inches(5), [
    "10个DGA家族细粒度分类结果（统计+2-gram + Optuna）：",
    "  - Suppobox：F1 较弱，因样本量有限且模式较随机",
    "  - Kraken：F1 良好，具有明显的长度和字符分布特征",
    "  - Shiotob：F1 优秀，n-gram模式区分度高",
    "  - Pykspa：F1 良好，随机化程度较高但仍可识别",
    "  - Bamital：F1 优秀，域名结构较为固定",
    "  - 其余5个家族整体表现中等偏上",
    "",
    "分析结论：",
    "  - 统计特征对某些家族（如Bamital）区分度好",
    "  - 2-gram特征对字符模式差异大的家族（如Shiotob）更有效",
    "  - 融合特征在所有家族上取得平衡的最优表现"
], 15, DARK)

# ===== 致谢 =====
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s, BLUE)
tb(s, Inches(1.5), Inches(1.5), Inches(10), Inches(1.0), "致  谢", 44, WHITE, bold=True, align=PP_ALIGN.CENTER)
add_rect(s, Inches(5), Inches(2.6), Inches(3.3), Inches(0.04), WHITE)
tb(s, Inches(1.5), Inches(3.0), Inches(10), Inches(1.5),
   "感谢指导老师余玉银老师的悉心指导\n感谢数学与信息科学学院各位老师的教诲\n感谢家人和同学的支持与帮助",
   20, RGBColor(0xCC,0xDD,0xFF), align=PP_ALIGN.CENTER)
tb(s, Inches(1.5), Inches(5.5), Inches(10), Inches(0.8), "请各位老师批评指正！", 28, WHITE, bold=True, align=PP_ALIGN.CENTER)

# 保存
out = "/home/girlorn/Cloud-Security-Study/Graduation-Project/毕业答辩PPT.pptx"
prs.save(out)
print(f"✅ PPT 已保存: {out}")
print(f"共 {len(prs.slides)} 页")
