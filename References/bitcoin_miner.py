"""
简易比特币挖矿客户端

工作原理：
  1. 从矿池获取挖矿任务
  2. 暴力枚举 nonce 算哈希
  3. 找到符合难度的提交到矿池

⚠️ 注意：这只是教学演示，你的 CPU 永远挖不到真正的比特币
   但如果连接到测试网矿池，可以正常工作
"""
import hashlib
import struct
import time
import threading

# =============================================
# 核心：区块哈希计算
# 这就是矿机芯片里几十亿次在算的东西
# =============================================

def double_sha256(data):
    """双重 SHA256 — 比特币的核心算法"""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def bytes_to_le(n, length=4):
    """转小端字节序（比特币协议要求）"""
    return n.to_bytes(length, 'little')

def compute_block_hash(version, prev_block, merkle_root, timestamp, bits, nonce):
    """
    计算一个完整区块的哈希
    
    区块头 = 80 字节:
      version       (4字节)  版本号
      prev_block    (32字节) 前一个区块的哈希
      merkle_root   (32字节) 交易Merkle树根
      timestamp     (4字节)  时间戳
      bits          (4字节)  难度目标
      nonce         (4字节)  随机数
    """
    header = (
        bytes_to_le(version, 4) +
        bytes.fromhex(prev_block)[::-1] +          # 小端
        bytes.fromhex(merkle_root)[::-1] +         # 小端
        bytes_to_le(timestamp, 4) +
        bytes.fromhex(bits)[::-1] +                # 小端
        bytes_to_le(nonce, 4)
    )
    
    hash_result = double_sha256(header)
    # 转成可读的十六进制（大端显示）
    return hash_result[::-1].hex()


# =============================================
# 挖矿循环（矿机芯片在干的事）
# =============================================

class Miner:
    """模拟一台矿机"""
    
    def __init__(self, worker_name="test.worker"):
        self.worker = worker_name
        self.running = False
        self.hash_count = 0
        self.start_time = None
        
        # 模拟一个挖矿任务（从矿池获取）
        self.task = {
            "version": 1,
            "prev_block": "0000000000000000000000000000000000000000000000000000000000000000",
            "merkle_root": "aa
            "timestamp": int(time.time()),
            "bits": "1d00ffff",   # 难度目标
            "target_zeros": 5,     # 前 5 位为 0（演示用低难度）
        }
    
    def mine(self):
        """挖矿主循环——就是不停地算哈希"""
        self.running = True
        self.start_time = time.time()
        nonce = 0
        
        print(f"⛏️  矿机启动: {self.worker}")
        print(f"   目标难度: 前 {self.task['target_zeros']} 位为 0")
        print(f"   开始挖矿...\n")
        
        while self.running:
            # 算一次区块哈希
            block_hash = compute_block_hash(
                self.task['version'],
                self.task['prev_block'],
                self.task['merkle_root'],
                self.task['timestamp'],
                self.task['bits'],
                nonce
            )
            
            self.hash_count += 1
            
            # 检查是否符合难度目标
            if block_hash.startswith('0' * self.task['target_zeros']):
                elapsed = time.time() - self.start_time
                hashrate = self.hash_count / elapsed
                print(f"\n🎉 找到符合条件的哈希！")
                print(f"   nonce:      {nonce}")
                print(f"   区块哈希:   {block_hash}")
                print(f"   尝试次数:   {self.hash_count:,}")
                print(f"   平均算力:   {hashrate:,.0f} H/s")
                print(f"   用时:       {elapsed:.2f} 秒")
                print(f"\n   ⚡ 提交到矿池... 等待下一个任务...\n")
                
                # 提交后重置，挖下一个块
                self.hash_count = 0
                self.start_time = time.time()
                self.task['timestamp'] = int(time.time())
                nonce = 0
                continue
            
            nonce += 1
            
            # 每 10 万次出个状态
            if nonce % 100000 == 0:
                elapsed = time.time() - self.start_time
                hashrate = self.hash_count / elapsed
                print(f"   已算 {self.hash_count:,} 次 | 算力: {hashrate:,.0f} H/s | 当前哈希: {block_hash[:16]}...", end='\r')
    
    def stop(self):
        self.running = False


if __name__ == "__main__":
    miner = Miner("我的矿机.001")
    
    try:
        miner.mine()
    except KeyboardInterrupt:
        miner.stop()
        print("\n\n⛔ 矿机停止")
