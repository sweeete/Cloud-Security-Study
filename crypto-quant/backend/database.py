"""SQLite 数据库管理"""
import sqlite3
import json
from datetime import datetime
from config import DB_FILE


def get_conn():
    conn = sqlite3.connect(str(DB_FILE))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = get_conn()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS exchange_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exchange TEXT NOT NULL DEFAULT 'binance',
            api_key TEXT NOT NULL,
            secret TEXT NOT NULL,
            password TEXT DEFAULT '',
            testnet INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS strategies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            symbol TEXT NOT NULL,
            side TEXT NOT NULL DEFAULT 'both',
            config TEXT NOT NULL DEFAULT '{}',
            enabled INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            strategy_id INTEGER,
            symbol TEXT NOT NULL,
            side TEXT NOT NULL,
            type TEXT NOT NULL,
            price REAL,
            amount REAL,
            cost REAL,
            status TEXT DEFAULT 'pending',
            order_id TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS trade_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            strategy_id INTEGER,
            symbol TEXT NOT NULL,
            action TEXT NOT NULL,
            detail TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            amount REAL DEFAULT 0,
            avg_price REAL DEFAULT 0,
            updated_at TEXT DEFAULT (datetime('now'))
        );
    """)

    conn.commit()
    conn.close()


def save_order(strategy_id, symbol, side, type_, price, amount, cost, status="pending", order_id=""):
    conn = get_conn()
    conn.execute(
        """INSERT INTO orders (strategy_id, symbol, side, type, price, amount, cost, status, order_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (strategy_id, symbol, side, type_, price, amount, cost, status, order_id)
    )
    conn.commit()
    conn.close()


def get_orders(limit=50):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM orders ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def log_trade(strategy_id, symbol, action, detail=""):
    conn = get_conn()
    conn.execute(
        "INSERT INTO trade_log (strategy_id, symbol, action, detail) VALUES (?, ?, ?, ?)",
        (strategy_id, symbol, action, detail)
    )
    conn.commit()
    conn.close()


def get_trade_logs(limit=100):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM trade_log ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_strategy(name, type_, symbol, side, config, enabled=0):
    conn = get_conn()
    cursor = conn.execute(
        "INSERT INTO strategies (name, type, symbol, side, config, enabled) VALUES (?, ?, ?, ?, ?, ?)",
        (name, type_, symbol, side, json.dumps(config), enabled)
    )
    conn.commit()
    strategy_id = cursor.lastrowid
    conn.close()
    return strategy_id


def get_strategies():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM strategies ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_strategy(strategy_id, **kwargs):
    conn = get_conn()
    fields = []
    values = []
    for k, v in kwargs.items():
        if k == "config":
            v = json.dumps(v)
        fields.append(f"{k}=?")
        values.append(v)
    values.append(strategy_id)
    conn.execute(f"UPDATE strategies SET {', '.join(fields)} WHERE id=?", values)
    conn.commit()
    conn.close()


def delete_strategy(strategy_id):
    conn = get_conn()
    conn.execute("DELETE FROM strategies WHERE id=?", (strategy_id,))
    conn.commit()
    conn.close()


def update_portfolio(symbol, amount, avg_price):
    conn = get_conn()
    existing = conn.execute("SELECT * FROM portfolio WHERE symbol=?", (symbol,)).fetchone()
    if existing:
        conn.execute(
            "UPDATE portfolio SET amount=?, avg_price=?, updated_at=datetime('now') WHERE symbol=?",
            (amount, avg_price, symbol)
        )
    else:
        conn.execute(
            "INSERT INTO portfolio (symbol, amount, avg_price) VALUES (?, ?, ?)",
            (symbol, amount, avg_price)
        )
    conn.commit()
    conn.close()


def get_portfolio():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM portfolio").fetchall()
    conn.close()
    return [dict(r) for r in rows]
