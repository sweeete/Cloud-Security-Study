#!/usr/bin/env python3
"""
CryptoQuant Windows 桌面客户端
依赖: pip install requests pillow (Windows 上 Python 自带 tkinter)
运行: python crypto_quant_client.py
"""
import json
import threading
import time
import webbrowser
from datetime import datetime
from tkinter import ttk, messagebox
import tkinter as tk

try:
    import requests
except ImportError:
    tk.messagebox.showerror("缺少依赖", "请先安装: pip install requests")
    exit(1)

# ===== 配置 =====
CONFIG_FILE = "cq_config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return {"server": "http://127.0.0.1:8888", "token": ""}

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


class CryptoQuantClient:
    """CryptoQuant Windows 桌面客户端"""

    def __init__(self):
        self.config = load_config()
        self.token = self.config.get("token", "")
        self.server = self.config.get("server", "http://127.0.0.1:8888")
        self.tickers = []
        self._running = True

        self.root = tk.Tk()
        self.root.title("CryptoQuant - 加密货币量化交易")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)

        # 图标（如果有）
        try:
            self.root.iconbitmap(default="")
        except:
            pass

        self._setup_ui()
        self._check_auth()

        # 定时刷新
        self._refresh_timer()

    def _setup_ui(self):
        """创建界面"""
        # 菜单栏
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="连接设置", command=self._show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self._on_close)
        menubar.add_cascade(label="文件", menu=file_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="刷新行情", command=self._fetch_tickers)
        menubar.add_cascade(label="视图", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=lambda: messagebox.showinfo("关于", "CryptoQuant v1.0\n加密货币量化交易桌面客户端"))
        menubar.add_cascade(label="帮助", menu=help_menu)
        self.root.config(menu=menubar)

        # 主布局 - Notebook (标签页)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # === Tab 1: 行情总览 ===
        self.tab_overview = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_overview, text="📊 行情总览")

        # 顶部状态栏
        status_frame = tk.Frame(self.tab_overview)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        self.lbl_status = tk.Label(status_frame, text="连接状态: 检查中...", font=("Arial", 10))
        self.lbl_status.pack(side=tk.LEFT)
        self.lbl_time = tk.Label(status_frame, text="", font=("Arial", 10), fg="gray")
        self.lbl_time.pack(side=tk.RIGHT)
        btn_refresh = tk.Button(status_frame, text="🔄 刷新", command=self._fetch_tickers)
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # 币种行情表格
        columns = ("币种", "名称", "最新价", "24h涨跌", "24h最高", "24h最低", "24h成交量")
        self.tree_tickers = ttk.Treeview(self.tab_overview, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree_tickers.heading(col, text=col)
            self.tree_tickers.column(col, width=100, anchor="center")
        self.tree_tickers.column("币种", width=80)
        self.tree_tickers.column("名称", width=120)
        self.tree_tickers.column("最新价", width=120)
        self.tree_tickers.column("24h涨跌", width=100)
        self.tree_tickers.column("24h成交量", width=120)

        scrollbar = ttk.Scrollbar(self.tab_overview, orient=tk.VERTICAL, command=self.tree_tickers.yview)
        self.tree_tickers.configure(yscrollcommand=scrollbar.set)
        self.tree_tickers.pack(fill=tk.BOTH, expand=True, padx=10, pady=5, side=tk.LEFT)
        scrollbar.pack(fill=tk.Y, pady=5, side=tk.RIGHT)

        # 双击打开K线
        self.tree_tickers.bind("<Double-1>", self._on_ticker_double_click)

        # === Tab 2: K 线图 ===
        self.tab_chart = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_chart, text="📈 K 线图")

        chart_ctrl = tk.Frame(self.tab_chart)
        chart_ctrl.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(chart_ctrl, text="币种:").pack(side=tk.LEFT)
        self.chart_symbol_var = tk.StringVar(value="BTC")
        chart_symbol_combo = ttk.Combobox(chart_ctrl, textvariable=self.chart_symbol_var,
                                          values=["BTC", "ETH", "SOL", "BNB", "XRP",
                                                  "DOGE", "ADA", "AVAX", "LINK", "DOT"],
                                          width=8, state="readonly")
        chart_symbol_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(chart_ctrl, text="周期:").pack(side=tk.LEFT, padx=(10, 0))
        self.chart_tf_var = tk.StringVar(value="1h")
        chart_tf_combo = ttk.Combobox(chart_ctrl, textvariable=self.chart_tf_var,
                                      values=["1m", "5m", "15m", "1h", "4h", "1d"],
                                      width=6, state="readonly")
        chart_tf_combo.pack(side=tk.LEFT, padx=5)

        btn_load_chart = tk.Button(chart_ctrl, text="加载K线", command=self._load_chart_data)
        btn_load_chart.pack(side=tk.LEFT, padx=10)

        # K线图用 Canvas + Text 文本模式显示
        self.chart_text = tk.Text(self.tab_chart, bg="#0b0e11", fg="#eaecef",
                                  font=("Consolas", 9), wrap=tk.NONE)
        self.chart_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # 技术指标显示
        self.lbl_indicators = tk.Label(self.tab_chart, text="技术指标: 加载中...",
                                       font=("Arial", 10), bg="#1e2329", fg="#848e9c",
                                       anchor=tk.W, padx=10, pady=5)
        self.lbl_indicators.pack(fill=tk.X, padx=10, pady=(0, 10))

        # === Tab 3: 策略管理 ===
        self.tab_strategies = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_strategies, text="⚙️ 策略管理")

        strat_ctrl = tk.Frame(self.tab_strategies)
        strat_ctrl.pack(fill=tk.X, padx=10, pady=10)

        btn_new_strat = tk.Button(strat_ctrl, text="＋ 新建策略", command=self._show_new_strategy)
        btn_new_strat.pack(side=tk.LEFT, padx=5)
        btn_refresh_strat = tk.Button(strat_ctrl, text="🔄 刷新策略", command=self._load_strategies)
        btn_refresh_strat.pack(side=tk.LEFT, padx=5)

        columns_strat = ("ID", "名称", "类型", "交易对", "状态", "创建时间")
        self.tree_strategies = ttk.Treeview(self.tab_strategies, columns=columns_strat, show="headings", height=8)
        for col in columns_strat:
            self.tree_strategies.heading(col, text=col)
            self.tree_strategies.column(col, width=100, anchor="center")
        self.tree_strategies.column("ID", width=40)
        self.tree_strategies.column("名称", width=150)
        self.tree_strategies.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 策略操作按钮
        strat_actions = tk.Frame(self.tab_strategies)
        strat_actions.pack(fill=tk.X, padx=10, pady=10)
        btn_toggle = tk.Button(strat_actions, text="▶ 启动/停止", command=self._toggle_strategy)
        btn_toggle.pack(side=tk.LEFT, padx=5)
        btn_run = tk.Button(strat_actions, text="▶ 运行一次", command=self._run_strategy_once)
        btn_run.pack(side=tk.LEFT, padx=5)
        btn_del = tk.Button(strat_actions, text="🗑 删除", fg="red", command=self._delete_strategy)
        btn_del.pack(side=tk.LEFT, padx=5)

        # === Tab 4: 持仓 & 订单 ===
        self.tab_portfolio = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_portfolio, text="💰 持仓 & 订单")

        # 持仓
        tk.Label(self.tab_portfolio, text="持仓", font=("Arial", 12, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 5))
        columns_pf = ("币种", "数量", "均价", "当前价", "盈亏")
        self.tree_portfolio = ttk.Treeview(self.tab_portfolio, columns=columns_pf, show="headings", height=5)
        for col in columns_pf:
            self.tree_portfolio.heading(col, text=col)
            self.tree_portfolio.column(col, width=120, anchor="center")
        self.tree_portfolio.pack(fill=tk.X, padx=10, pady=5)

        # 订单
        tk.Label(self.tab_portfolio, text="订单记录", font=("Arial", 12, "bold")).pack(anchor=tk.W, padx=10, pady=(15, 5))
        columns_orders = ("时间", "币种", "方向", "价格", "数量", "金额", "状态")
        self.tree_orders = ttk.Treeview(self.tab_portfolio, columns=columns_orders, show="headings", height=8)
        for col in columns_orders:
            self.tree_orders.heading(col, text=col)
            self.tree_orders.column(col, width=100, anchor="center")
        self.tree_orders.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        btn_refresh_pf = tk.Button(self.tab_portfolio, text="🔄 刷新", command=self._load_portfolio)
        btn_refresh_pf.pack(padx=10, pady=5, anchor=tk.W)

        # === Tab 5: 设置 ===
        self.tab_settings = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_settings, text="🔧 设置")

        sf = tk.Frame(self.tab_settings, padx=20, pady=20)
        sf.pack(fill=tk.BOTH, expand=True)

        # 服务器设置
        tk.Label(sf, text="服务器地址", font=("Arial", 11)).pack(anchor=tk.W)
        self.entry_server = tk.Entry(sf, width=40, font=("Arial", 10))
        self.entry_server.insert(0, self.server)
        self.entry_server.pack(fill=tk.X, pady=(0, 15))

        tk.Label(sf, text="Token", font=("Arial", 11)).pack(anchor=tk.W)
        self.entry_token = tk.Entry(sf, width=40, font=("Arial", 10))
        self.entry_token.insert(0, self.token)
        self.entry_token.pack(fill=tk.X, pady=(0, 15))

        btn_save = tk.Button(sf, text="保存设置", command=self._save_settings, bg="#1e80ff", fg="white",
                             font=("Arial", 11), padx=20, pady=5)
        btn_save.pack(anchor=tk.W)

        tk.Label(sf, text="\n💡 提示：首次使用请在服务器上先运行后端，\n然后在浏览器中首次设置密码并登录，\n之后用浏览器获取 Token 填到这里。",
                 font=("Arial", 9), fg="gray", justify=tk.LEFT).pack(anchor=tk.W, pady=10)

    # ===== 认证 =====
    def _check_auth(self):
        if not self.token:
            self.lbl_status.config(text="❌ 未配置 Token，请到设置页面配置", fg="red")
            self.notebook.select(self.tab_settings)
        else:
            self._fetch_tickers()

    def _save_settings(self):
        self.server = self.entry_server.get().strip()
        self.token = self.entry_token.get().strip()
        self.config["server"] = self.server
        self.config["token"] = self.token
        save_config(self.config)
        messagebox.showinfo("设置", "设置已保存")
        self._check_auth()

    def _show_settings(self):
        self.notebook.select(self.tab_settings)

    # ===== API 请求 =====
    def _api_request(self, method, path, data=None):
        url = f"{self.server.rstrip('/')}{path}"
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        try:
            if method == "GET":
                resp = requests.get(url, headers=headers, timeout=10)
            else:
                resp = requests.post(url, headers=headers, json=data, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 401:
                self.lbl_status.config(text="❌ Token 过期，请重新配置", fg="red")
                return None
            else:
                return None
        except requests.exceptions.ConnectionError:
            self.lbl_status.config(text=f"❌ 无法连接服务器 {self.server}", fg="red")
            return None
        except Exception as e:
            self.lbl_status.config(text=f"❌ 请求错误: {str(e)[:30]}", fg="red")
            return None

    # ===== 行情数据 =====
    def _fetch_tickers(self):
        def _do():
            data = self._api_request("GET", "/api/market/tickers")
            if data and isinstance(data, list):
                self.tickers = data
                self.root.after(0, self._update_ticker_table)
                self.root.after(0, lambda: self.lbl_status.config(
                    text=f"✅ 已连接 | {len(data)} 个币种", fg="#0ecb81"))
            elif data is None:
                self.root.after(0, lambda: self.lbl_status.config(
                    text="❌ 连接失败", fg="red"))

        threading.Thread(target=_do, daemon=True).start()

    def _update_ticker_table(self):
        for item in self.tree_tickers.get_children():
            self.tree_tickers.delete(item)

        for t in self.tickers:
            change = t.get("change", 0) or 0
            price = t.get("last", 0)
            tags = "up" if change >= 0 else "down"
            self.tree_tickers.insert("", tk.END, values=(
                t.get("symbol", ""),
                t.get("name", ""),
                f"${price:,.2f}" if price else "—",
                f"{change:+.2f}%" if change else "—",
                f"${t.get('high', 0):,.2f}" if t.get('high') else "—",
                f"${t.get('low', 0):,.2f}" if t.get('low') else "—",
                f"{t.get('volume', 0):,.0f}" if t.get('volume') else "—",
            ), tags=(tags,))
            if tags == "up":
                self.tree_tickers.tag_configure("up", foreground="#0ecb81")
            else:
                self.tree_tickers.tag_configure("down", foreground="#f6465d")

        self.lbl_time.config(text=f"更新于 {datetime.now().strftime('%H:%M:%S')}")

    def _on_ticker_double_click(self, event):
        selection = self.tree_tickers.selection()
        if selection:
            values = self.tree_tickers.item(selection[0], "values")
            if values:
                self.chart_symbol_var.set(values[0])
                self.notebook.select(self.tab_chart)
                self._load_chart_data()

    # ===== K 线图（文本模式） =====
    def _load_chart_data(self):
        symbol = self.chart_symbol_var.get()
        tf = self.chart_tf_var.get()

        def _do():
            data = self._api_request("GET", f"/api/market/klines/{symbol}?timeframe={tf}&limit=60")
            indicators = self._api_request("GET", f"/api/market/indicators/{symbol}?timeframe={tf}&limit=60")

            self.root.after(0, lambda: self._render_chart(symbol, tf, data, indicators))

        threading.Thread(target=_do, daemon=True).start()

    def _render_chart(self, symbol, tf, klines, indicators):
        self.chart_text.delete(1.0, tk.END)

        if not klines or isinstance(klines, dict) and "error" in klines:
            self.chart_text.insert(tk.END, "无法加载K线数据")
            return

        # 标题
        self.chart_text.insert(tk.END, f" {symbol}/USDT  {tf}  共 {len(klines)} 根K线\n\n")

        # 显示最近20根K线
        recent = klines[-20:]
        headers = f"{'时间':>12} {'开盘':>10} {'收盘':>10} {'最高':>10} {'最低':>10} {'涨跌幅':>8}\n"
        self.chart_text.insert(tk.END, headers, "header")
        self.chart_text.tag_config("header", foreground="#1e80ff")

        for k in recent:
            dt = datetime.fromtimestamp(k["time"]).strftime("%m-%d %H:%M")
            close = k["close"]
            open_ = k["open"]
            change = ((close - open_) / open_) * 100 if open_ else 0
            prefix = " ▲" if close >= open_ else " ▼"
            tag = "up" if close >= open_ else "down"

            line = f"{prefix} {dt}  {open_:>10.2f} {close:>10.2f} {k['high']:>10.2f} {k['low']:>10.2f} {change:>+7.2f}%\n"
            self.chart_text.insert(tk.END, line, tag)

        self.chart_text.tag_config("up", foreground="#0ecb81")
        self.chart_text.tag_config("down", foreground="#f6465d")

        # 指标
        if indicators and not isinstance(indicators, dict) or "error" not in (indicators or {}):
            items = []
            for k, v in (indicators or {}).items():
                if v is not None:
                    items.append(f"{k}: {v}")
            ind_text = " | ".join(items)
        else:
            ind_text = "无数据"

        self.lbl_indicators.config(text=f"📊 技术指标: {ind_text}")

    # ===== 策略管理 =====
    def _load_strategies(self):
        def _do():
            data = self._api_request("GET", "/api/strategies")
            if data and "strategies" in data:
                self.root.after(0, lambda: self._update_strat_table(data["strategies"]))
        threading.Thread(target=_do, daemon=True).start()

    def _update_strat_table(self, strategies):
        for item in self.tree_strategies.get_children():
            self.tree_strategies.delete(item)
        for s in strategies:
            status = "🟢 运行中" if s.get("enabled") else "🔴 已停止"
            self.tree_strategies.insert("", tk.END, values=(
                s["id"], s["name"], s["type"], s["symbol"], status, s.get("created_at", "")
            ))

    def _toggle_strategy(self):
        selection = self.tree_strategies.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个策略")
            return
        sid = self.tree_strategies.item(selection[0], "values")[0]

        def _do():
            data = self._api_request("POST", f"/api/strategies/{sid}/toggle")
            self.root.after(0, self._load_strategies)
        threading.Thread(target=_do, daemon=True).start()

    def _run_strategy_once(self):
        selection = self.tree_strategies.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个策略")
            return
        sid = self.tree_strategies.item(selection[0], "values")[0]

        def _do():
            data = self._api_request("POST", f"/api/strategies/{sid}/run")
            if data:
                action = data.get("action", "?")
                reason = data.get("reason", "")
                self.root.after(0, lambda: messagebox.showinfo(
                    "执行结果", f"信号: {action}\n{reason}"))
        threading.Thread(target=_do, daemon=True).start()

    def _delete_strategy(self):
        selection = self.tree_strategies.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个策略")
            return
        sid = self.tree_strategies.item(selection[0], "values")[0]
        name = self.tree_strategies.item(selection[0], "values")[1]
        if not messagebox.askyesno("确认", f"确定删除策略「{name}」？"):
            return

        def _do():
            self._api_request("DELETE", f"/api/strategies/{sid}")
            self.root.after(0, self._load_strategies)
        threading.Thread(target=_do, daemon=True).start()

    def _show_new_strategy(self):
        """简单的新建策略对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("新建策略")
        dialog.geometry("400x350")
        dialog.resizable(False, False)

        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="策略名称:").pack(anchor=tk.W)
        entry_name = tk.Entry(frame, width=30)
        entry_name.pack(fill=tk.X, pady=(0, 10))

        tk.Label(frame, text="策略类型:").pack(anchor=tk.W)
        type_var = tk.StringVar(value="grid")
        type_combo = ttk.Combobox(frame, textvariable=type_var,
                                  values=["grid", "ma_cross", "rsi", "macd", "llm"],
                                  state="readonly")
        type_combo.pack(fill=tk.X, pady=(0, 10))

        tk.Label(frame, text="交易对:").pack(anchor=tk.W)
        symbol_var = tk.StringVar(value="BTC/USDT")
        symbol_combo = ttk.Combobox(frame, textvariable=symbol_var,
                                    values=["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT",
                                            "XRP/USDT", "DOGE/USDT", "ADA/USDT",
                                            "AVAX/USDT", "LINK/USDT", "DOT/USDT"],
                                    state="readonly")
        symbol_combo.pack(fill=tk.X, pady=(0, 20))

        def do_create():
            data = {
                "name": entry_name.get(),
                "type": type_var.get(),
                "symbol": symbol_var.get(),
                "config": {"interval": "1h", "trade_amount": 0.001}
            }
            def _do():
                result = self._api_request("POST", "/api/strategies", data)
                self.root.after(0, lambda: (
                    messagebox.showinfo("成功", "策略创建成功"),
                    dialog.destroy(),
                    self._load_strategies()
                ))
            threading.Thread(target=_do, daemon=True).start()

        btn_create = tk.Button(frame, text="创建策略", command=do_create,
                               bg="#1e80ff", fg="white", font=("Arial", 11))
        btn_create.pack()

    # ===== 持仓 & 订单 =====
    def _load_portfolio(self):
        def _do():
            pf = self._api_request("GET", "/api/portfolio")
            orders = self._api_request("GET", "/api/orders?limit=20")
            tickers = self._api_request("GET", "/api/market/tickers")

            price_map = {}
            if isinstance(tickers, list):
                for t in tickers:
                    price_map[t.get("symbol", "")] = t.get("last", 0)

            self.root.after(0, lambda: self._update_portfolio_ui(pf, orders, price_map))

        threading.Thread(target=_do, daemon=True).start()

    def _update_portfolio_ui(self, pf_data, orders_data, price_map):
        # 持仓
        for item in self.tree_portfolio.get_children():
            self.tree_portfolio.delete(item)

        if pf_data and "portfolio" in pf_data:
            for p in pf_data["portfolio"]:
                sym = p.get("symbol", "")
                cur_price = price_map.get(sym, 0)
                avg = p.get("avg_price", 0)
                amount = p.get("amount", 0)
                pnl = (cur_price - avg) * amount if cur_price and avg else 0
                pnl_text = f"+${pnl:.2f}" if pnl >= 0 else f"-${abs(pnl):.2f}"
                self.tree_portfolio.insert("", tk.END, values=(
                    sym, f"{amount:.6f}", f"${avg:.2f}" if avg else "—",
                    f"${cur_price:.2f}" if cur_price else "—", pnl_text
                ))

        # 订单
        for item in self.tree_orders.get_children():
            self.tree_orders.delete(item)

        if orders_data and "orders" in orders_data:
            for o in orders_data["orders"][:20]:
                self.tree_orders.insert("", tk.END, values=(
                    o.get("created_at", ""),
                    o.get("symbol", ""),
                    o.get("side", "").upper(),
                    f"${o.get('price', 0):.2f}" if o.get("price") else "—",
                    o.get("amount", ""),
                    f"${o.get('cost', 0):.2f}" if o.get("cost") else "—",
                    o.get("status", ""),
                ))

    # ===== 定时刷新 =====
    def _refresh_timer(self):
        if not self._running:
            return
        try:
            # 每30秒刷新行情
            self._fetch_tickers()
        except:
            pass
        self.root.after(30000, self._refresh_timer)

    # ===== 退出 =====
    def _on_close(self):
        self._running = False
        self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()


if __name__ == "__main__":
    app = CryptoQuantClient()
    app.run()
