"""配置管理模块"""

import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".crypto-quant"
CONFIG_FILE = CONFIG_DIR / "config.json"
DB_FILE = CONFIG_DIR / "data.db"

DEFAULT_CONFIG = {
    "exchange": {
        "name": "binance",
        "apiKey": "",
        "secret": "",
        "password": "",
        "testnet": True  # 默认使用测试网
    },
    "llm": {
        "provider": "",
        "apiKey": "",
        "model": "",
        "baseUrl": ""
    },
    "app": {
        "password_hash": "",
        "port": 8888
    }
}


def ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    ensure_config_dir()
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return dict(DEFAULT_CONFIG)


def save_config(config: dict):
    ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_exchange_config() -> dict:
    cfg = load_config()
    return cfg.get("exchange", {})


def get_llm_config() -> dict:
    cfg = load_config()
    return cfg.get("llm", {})


def set_exchange_keys(api_key: str, secret: str, password: str = "", testnet: bool = True, name: str = "binance"):
    cfg = load_config()
    cfg["exchange"] = {
        "name": name,
        "apiKey": api_key,
        "secret": secret,
        "password": password,
        "testnet": testnet
    }
    save_config(cfg)


def set_llm_keys(provider: str, api_key: str, model: str, base_url: str = ""):
    cfg = load_config()
    cfg["llm"] = {
        "provider": provider,
        "apiKey": api_key,
        "model": model,
        "baseUrl": base_url
    }
    save_config(cfg)


def is_first_run() -> bool:
    cfg = load_config()
    return not cfg.get("app", {}).get("password_hash")
