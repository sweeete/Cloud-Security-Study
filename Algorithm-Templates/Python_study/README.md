# 🐍 Python_study

Python 学习工作区 —— **从零开始**，只学 Python 语言本身。

> 定位：纯粹学 Python。这里**不放** NumPy / PyTorch / 大模型 / Agent 相关的内容（那些在 `STUDY_FOR_WORK/`）。
> 目标：把语言基础打扎实，能独立写出规范的 Python 代码。

---

## 🧭 环境信息

| 项目 | 值 |
| :--- | :--- |
| Python 版本 | 3.13.12（命令行输入 `python --version` 查看） |
| 解释器路径 | `C:\Users\Girlorn\AppData\Local\Programs\Python\Python313\python.exe` |
| 平台 | Windows |
| 编辑器 | VS Code（推荐装 Python 扩展） |

**怎么跑示例代码**：在本文件夹里打开终端，然后

```bash
python 01-Basics/01_basics.py
```

---

## 📚 学习路线

按编号顺序学，每个主题的 README 里都有「知识点 → 示例代码 → 易错点 → 练习」。

| 编号 | 主题 | 主要内容 | 状态 |
| :--- | :--- | :--- | :--- |
| 00 | [Environment](./00-Environment/) | 解释器、REPL、pip、虚拟环境、第一个脚本 | ⬜ |
| 01 | [Basics](./01-Basics/) | 变量、数据类型、运算符、类型转换 | ⬜ |
| 02 | [Strings](./02-Strings/) | 引号、切片、f-string、字符串方法 | ⬜ |
| 03 | [Control-Flow](./03-Control-Flow/) | if / while / for、range、break / continue | ⬜ |
| 04 | [Collections](./04-Collections/) | list / tuple / dict / set、推导式 | ⬜ |
| 05 | [Functions](./05-Functions/) | 参数、返回值、作用域、lambda | ⬜ |
| 06 | [Modules](./06-Modules/) | import、`__main__`、标准库、pip 与 venv | ⬜ |
| 07 | [Files-and-Exceptions](./07-Files-and-Exceptions/) | try / except、with open、pathlib | ⬜ |
| 08 | [OOP](./08-OOP/) | 类、继承、魔术方法、@property | ⬜ |
| 09 | [Advanced](./09-Advanced/) | 迭代器、生成器、闭包、装饰器 | ⬜ |
| 10 | [Stdlib](./10-Stdlib/) | pathlib / json / datetime / re / collections | ⬜ |

状态标记：⬜ 未学 · 🔄 学习中 · ✅ 已掌握

---

## 📁 目录约定

```
Python_study/
├─ README.md              ← 你正在看的这份总索引
├─ 00-Environment/
│  ├─ README.md           ← 该主题的要点笔记
│  └─ 00_hello.py         ← 可直接运行的示例代码
├─ 01-Basics/
│  ├─ README.md
│  └─ 01_basics.py
└─ ...
```

- **文件夹**：`两位编号-英文名`，跟同级 `OJ-C++`、`LeetCode-Daily` 的风格保持一致
- **示例代码**：文件名用英文；**注释、输出说明用中文**，尽量做到「读注释就能懂」
- **笔记**：直接写在各主题的 `README.md` 里，和代码放在一起，方便对照
- **练习**：每个示例文件末尾有「动手练习」，建议自己新建一个 `practice.py` 写答案，不要直接改示例文件

---

## ✅ 进度记录

| 日期 | 内容 | 备注 |
| :--- | :--- | :--- |
| 2026-09-17 | 建立工作区、铺好学习路线与示例代码骨架 | 从零开始 |
