"""
比特币挖矿核心代码

真正的矿机就在做这件事：
  1. 拿一个区块（包含交易数据）
  2. 暴力枚举 nonce
  3. 算 double SHA256
  4. 检查哈希是否满足难度要求
"""
import hashlib
import time


def mine(block_data, difficulty):
    """
    挖矿函数
    
    参数:
      block_data: 区块数据（交易 + 时间戳 + 前块哈希等）
      difficulty: 目标难度（前 N 位必须是 0）
    
    返回:
      (nonce, block_hash) — 找到的随机数和区块哈希
    """
    target = '0' * difficulty
    nonce = 0
    start = time.time()
    attempts = 0

    while True:
        # 拼起来算双重 SHA256
        data = f"{block_data}{nonce}"
        h1 = hashlib.sha256(data.encode()).hexdigest()
        h2 = hashlib.sha256(h1.encode()).hexdigest()

        attempts += 1

        if h2.startswith(target):
            elapsed = time.time() - start
            hashrate = attempts / elapsed
            print(f"\n🎉 挖到区块！")
            print(f"   nonce = {nonce}")
            print(f"   hash  = {h2}")
            print(f"   尝试次数: {attempts:,}")
            print(f"   算力: {hashrate:,.0f} H/s")
            print(f"   用时: {elapsed:.2f} 秒")
            return nonce, h2

        nonce += 1

        if attempts % 100000 == 0:
            elapsed = time.time() - start
            hashrate = attempts / elapsed
            print(f"   已算 {attempts:,} 次 | 算力: {hashrate:,.0f} H/s | 当前: {h2[:20]}...", end='\r')


if __name__ == "__main__":
    import sys
    
    # 模拟一个区块
    block = f"""
    区块头:
      版本: 1
      前块哈希: 0000000000000000000000000000000000000000000000000000000000000000
      Merkle根: 3ba4ed8f7e8b4c6d9a0f1b2c3d4e5f6a
      时间戳: {int(time.time())}
      交易数: 2345 笔
    """
    
    # 难度 4: 前 4 位是 0（演示用）
    # 真实比特币: 前 20+ 位是 0
    difficulty = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    
    print(f"⛏️  比特币挖矿演示")
    print(f"   难度: 前 {difficulty} 位为 0")
    print(f"   每成功一次的概率: 1/{16**difficulty:,}")
    print()
    
    mine(block, difficulty)
