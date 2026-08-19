"""
简易比特币挖矿演示脚本

原理: 暴力枚举 nonce，找到使哈希以足够多 0 开头的值
"""
import hashlib
import time

def sha256_double(data):
    """双重 SHA256（比特币实际使用的算法）"""
    return hashlib.sha256(hashlib.sha256(data.encode()).hexdigest().encode()).hexdigest()

def mine(block_data, difficulty):
    """
    挖矿函数
    block_data: 区块数据
    difficulty: 目标难度（哈希前几位为0）
    """
    target = '0' * difficulty  # 目标前缀
    nonce = 0
    start = time.time()
    hashrate_log = []

    print(f"⛏️  开始挖矿...")
    print(f"   区块数据: {block_data}")
    print(f"   目标难度: 前 {difficulty} 位为 0")
    print(f"   目标哈希: {target}{'x' * (64 - difficulty)}")
    print()

    while True:
        hash_result = sha256_double(f"{block_data}{nonce}")

        # 每 10 万次打印一次进度
        if nonce % 100000 == 0:
            elapsed = time.time() - start
            hashrate = nonce / elapsed if elapsed > 0 else 0
            print(f"   已尝试 {nonce:,} 次 | 算力: {hashrate:,.0f} H/s | 当前哈希: {hash_result[:20]}...")

        if hash_result.startswith(target):
            elapsed = time.time() - start
            hashrate = nonce / elapsed if elapsed > 0 else 0
            print(f"\n🎉 挖矿成功！")
            print(f"   总共尝试: {nonce:,} 次")
            print(f"   花费时间: {elapsed:.2f} 秒")
            print(f"   平均算力: {hashrate:,.0f} H/s")
            print(f"   有效 nonce: {nonce}")
            print(f"   区块哈希: {hash_result}")
            return nonce, hash_result

        nonce += 1


if __name__ == "__main__":
    # 模拟一个简单的区块
    block = {
        "version": 1,
        "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",
        "merkle_root": "3ba4ed8f7e8b4c6d9a0f1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2",
        "timestamp": int(time.time()),
        "bits": "1d00ffff",
        "nonce": 0,
    }

    block_data = f"{block['version']}{block['prev_hash']}{block['merkle_root']}{block['timestamp']}{block['bits']}"

    # 难度 4 = 前 4 位是 0（主网实际难度是 ~18-20 位）
    mine(block_data, difficulty=4)
