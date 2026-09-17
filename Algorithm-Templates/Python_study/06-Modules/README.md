# 06 · 模块与包

> 目标：会把自己的代码拆成模块、会用标准库、理解 `if __name__ == "__main__"`。

## 知识点

1. **模块（module）**：一个 `.py` 文件就是一个模块，用 `import 模块名` 使用
2. **包的（package）**：一个含 `__init__.py` 的文件夹，里面放多个模块
3. **import 的几种写法**
   | 写法 | 用法 | 建议 |
   | :--- | :--- | :--- |
   | `import math` | `math.sqrt(4)` | ✅ 推荐，来源清晰 |
   | `import math as m` | `m.sqrt(4)` | ✅ 名字太长时 |
   | `from math import sqrt` | `sqrt(4)` | ⚠️ 少量使用，多了会歧义 |
   | `from math import *` | 污染命名空间 | ❌ 别用 |
4. **`if __name__ == "__main__":`**
   - 直接运行该文件时，`__name__` 是 `"__main__"`
   - 被别的文件 `import` 时，`__name__` 是模块名
   - 所以这个 if 里的代码**只有直接运行时才跑**——模块的「自测入口」
5. **模块搜索顺序**：当前目录 → `PYTHONPATH` → 标准库 → 第三方库（`site-packages`）
6. **import 只执行一次**：重复 import 不会重复执行模块代码（有缓存 `sys.modules`）
7. **第三方库与 pip**
   - 安装：`pip install requests`
   - 查看：`pip list`，卸载：`pip uninstall requests`
   - 冻结依赖：`pip freeze > requirements.txt`，恢复：`pip install -r requirements.txt`
8. **虚拟环境**（每个项目一个）
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows 激活
   pip install xxx
   deactivate
   ```
9. **常用标准库预览**（第 10 节展开）
   - `math` / `random` / `statistics` / `datetime` / `json` / `os` / `pathlib` / `sys`

## 示例代码

| 文件 | 演示内容 |
| :--- | :--- |
| `greet_module.py` | 被导入的模块：函数、常量、`__name__` 入口 |
| `06_modules.py` | import 四种写法、调用自己写的模块、标准库初体验、`__name__` 对比 |

## 易错点

- 文件不要和标准库/第三方库重名（如 `random.py`、`json.py`），否则 `import` 会导入自己
- 被 import 的模块**不能**依赖「运行时的相对路径」，用 `pathlib.Path(__file__).parent` 定位
- 模块名（文件名）不要用 `-`，用下划线 `my_module.py`
- 修改了被导入的模块，需要**重启解释器**（或用 `importlib.reload`）才生效
- `pip install` 报「不是内部或外部命令」→ 用 `python -m pip install xxx`

## 动手练习

1. 把第 05 节写的 `is_prime` 搬进 `my_tools.py`，在另一个文件里 `import` 使用
2. 在模块里加 `if __name__ == "__main__":` 自测代码，分别用「直接运行」和「import」观察区别
3. 建一个包 `utils/`，里面放 `string_tools.py` 和 `math_tools.py`，从外面导入使用
4. 用 `math` 和 `random` 写一个「随机出题」的小脚本

## 参考

- 模块：https://docs.python.org/zh-cn/3/tutorial/modules.html
- pip 使用：https://packaging.python.org/zh-cn/latest/tutorials/installing-packages/
