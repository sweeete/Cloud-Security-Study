# 07 · 异常处理与文件

> 目标：程序出错不会直接崩；会用 `with open` 读写文本文件。

## 知识点

### 异常

1. **异常是什么**：运行时错误 → 抛异常 → 不处理就中断程序
   - 常见：`ValueError`、`TypeError`、`KeyError`、`IndexError`、`ZeroDivisionError`、`FileNotFoundError`
2. **完整结构**
   ```python
   try:
       可能出错的代码
   except ValueError as e:
       处理 ValueError
   except (TypeError, KeyError):
       一次捕获多种类型
   except Exception as e:
       兜底（尽量少用，别把 bug 吞掉）
   else:
       没出异常时执行
   finally:
       无论成功失败都执行（收尾：关文件、断连接）
   ```
3. **`raise`**：主动抛异常 → `raise ValueError("年龄不能为负")`
4. **`assert`**：断言，用于「不该发生」的自检（可被 `-O` 关闭，别用它做输入校验）
5. **自定义异常**：`class MyError(Exception): pass`
6. **EAFP 风格**：「先干，出错再说」（try/except）比「先检查再干」（if 判断）更 Pythonic

### 文件

7. **`open` 的模式**
   | 模式 | 含义 |
   | :--- | :--- |
   | `"r"` | 只读（默认，文件不存在报错） |
   | `"w"` | 只写（**会清空原内容**） |
   | `"a"` | 追加 |
   | `"r+"` / `"w+"` | 读写 |
   | `"rb"` / `"wb"` | 二进制（图片、压缩包） |
8. **`with open(...) as f:`** —— 自动关闭文件，永远优先用它
   - 读全部：`f.read()`；按行读：`for line in f:`；去换行 `line.strip()`
   - 写：`f.write("文本\n")`（`\n` 要自己加）；多行：`f.writelines(lines)`
   - **一定要写 `encoding="utf-8"`**，否则 Windows 默认 GBK 会中文乱码
9. **`pathlib`（现代写法，推荐）**
   ```python
   from pathlib import Path
   base = Path(__file__).parent          # 当前文件所在目录
   p = base / "data.txt"                 # 用 / 拼路径
   p.exists() / p.read_text(encoding="utf-8") / p.write_text("hi", encoding="utf-8")
   ```
10. **CSV / JSON**
   - `csv` 模块：`csv.reader` / `csv.DictReader`
   - `json` 模块：`json.dump` / `json.load`（详细在第 10 节）

## 示例代码

| 文件 | 演示内容 |
| :--- | :--- |
| `07_files_and_exceptions.py` | 各种异常演示、try/except/else/finally、raise 与自定义异常、with open 读写追加、逐行读取、pathlib、处理坏数据 |
| `data/`（运行时自动生成） | 示例脚本写出的文件都放这里 |

## 易错点

- `except:` 或 `except Exception:` 一把抓 → 真正的 bug 被静默吞掉，排查时想哭
- `finally` 里有 `return` 会覆盖 try 里的 `return`（别这么写）
- `"w"` 模式打开已存在的文件会**直接清空**，想保留原内容用 `"a"`
- 忘记 `encoding="utf-8"` → 中文报 `UnicodeDecodeError` / 乱码
- 读文件后忘了关闭（没用 `with`）→ 大文件句柄泄漏
- `f.read()` 之后再 `for line in f:` 读不到东西（指针已到末尾）
- 相对路径看到的是**当前工作目录**，不是脚本所在目录；用 `pathlib` + `__file__` 才稳

## 动手练习

1. 写 `safe_divide(a, b)`，`b == 0` 时返回 `None`，并用 try/except 捕获 `TypeError`
2. 用 `with open` 写一个 `notes.txt`，逐行写入 3 条内容，再读出来打印
3. 用 `"a"` 模式往同一个文件追加一行，验证原内容没被清空
4. 读一个不存在的文件，捕获 `FileNotFoundError` 并给出友好提示
5. 写一个自定义异常 `ScoreError`，成绩不在 0~100 时抛出

## 参考

- 错误与异常：https://docs.python.org/zh-cn/3/tutorial/errors.html
- 文件读写：https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#reading-and-writing-files
- pathlib：https://docs.python.org/zh-cn/3/library/pathlib.html
