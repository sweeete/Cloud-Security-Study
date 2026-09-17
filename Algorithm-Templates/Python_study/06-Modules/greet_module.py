# -*- coding: utf-8 -*-
"""
06 · 一个可以被导入的模块（示例用）

这个文件本身就是「模块」——文件名 greet_module 就是模块名。
别人这样用：
    import greet_module
    greet_module.greet("主人")
"""

# 模块级的常量（习惯全大写）
AUTHOR = "亚美"
VERSION = "1.0"


def greet(name: str) -> str:
    """返回一句问候语。"""
    return f"你好，{name}！来自 {AUTHOR} v{VERSION}"


def add(a: int, b: int) -> int:
    """两数相加。"""
    return a + b


def _helper():
    """下划线开头的函数表示「模块内部用」，不建议外部调用。"""
    return "内部工具"


# ===== 模块的自测入口 =====
# 直接运行 greet_module.py 时，__name__ == "__main__" 成立 → 下面的代码执行
# 被 import 时 __name__ == "greet_module" → 下面的代码不执行
if __name__ == "__main__":
    print("【作为脚本直接运行】")
    print(greet("自己"))
    print("顺带测试 add(1, 2) =", add(1, 2))
else:
    # 只有被导入时才打印，方便观察执行时机
    print(f"（greet_module 被导入了，我的 __name__ = {__name__}）")
