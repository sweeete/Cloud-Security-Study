# 00 · 环境准备

> 目标：把「写 Python → 跑 Python」这条链路打通，第一行代码跑起来。

## 知识点

1. **解释器与版本**：Python 是解释型语言，用 `python xxx.py` 执行；先确认版本
2. **两个运行方式**
   - 写文件再跑（主用）：`python 00_hello.py`
   - 交互式 REPL（试验用）：命令行输入 `python` 进入，`>>>` 后面直接敲代码，`exit()` 退出
3. **注释**：`#` 单行注释，`"""..."""` 多行字符串当注释用
4. **`print()`**：输出；多个值用逗号分隔会自动加空格
5. **缩进即语法**：Python 靠缩进划分代码块，同一层必须对齐（习惯用 4 个空格）
6. **pip**：包管理器，`pip install 包名` 装第三方库（现在用不到，先知道）
7. **虚拟环境 venv**：给每个项目独立一份依赖，避免互相污染
   - 建：`python -m venv .venv`
   - 激活（Windows）：`.venv\Scripts\activate`
   - 退出：`deactivate`
   - 本仓库的 `.gitignore` 已经忽略 `.venv/`，可以放心建
8. **查看帮助**：`help(print)`、`dir(obj)`、`type(obj)` 都在 REPL 里能救命

## 示例代码

| 文件 | 演示内容 |
| :--- | :--- |
| `00_hello.py` | 注释、`print` 的几种写法、转义字符、`type()` 初体验、`__name__` |

## 易错点

- 命令行里写 `python` 没反应 → 检查有没有勾选「Add Python to PATH」，或直接用 `py` 命令
- 文件名别叫 `random.py`、`json.py` 这种**和标准库重名**的名字，`import` 会把自己导进来
- 中文乱码 → 源码统一用 UTF-8（VS Code 右下角可以确认）
- Windows 下路径分隔符是 `\`，但在字符串里要么写 `\\`，要么用 `/` 或原始字符串 `r"..."`

## 动手练习

1. 把 `00_hello.py` 跑起来，看看输出
2. 在命令行输入 `python` 进入 REPL，算一下 `2 ** 10` 和 `7 // 2`，然后 `exit()`
3. 新建一个 `practice.py`，打印自己的名字和今天的日期

## 参考

- 官方教程：https://docs.python.org/zh-cn/3/tutorial/index.html
- venv 文档：https://docs.python.org/zh-cn/3/library/venv.html
