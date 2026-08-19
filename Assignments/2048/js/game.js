/**
 * 2048 Game - Core Algorithm Module
 *
 * 包含 Board 类、四方向滑动合并、游戏状态检测、GameEngine 类。
 * 所有导出挂载到 window 上，末尾附带 console.assert 单元测试。
 */

// 兼容 Node.js 环境（无 window 对象）
if (typeof window === 'undefined') {
  globalThis.window = {};
}

// ============================================================
//  Board 类：封装二维网格数据
// ============================================================

/**
 * @class Board
 * @description 表示 2048 游戏的棋盘，提供基本的网格操作。
 *
 * @param {number} [size=4] - 棋盘行列数，标准 2048 为 4×4
 */
window.Board = class Board {
  constructor(size = 4) {
    /** @type {number} 棋盘尺寸 */
    this.size = size;

    /** @type {number[][]} 二维数组，每个元素为 0 或 2 的幂 */
    this.grid = Array.from({ length: size }, () => Array(size).fill(0));
  }

  /**
   * 获取指定坐标的值
   * @param {number} row - 行索引（0-based）
   * @param {number} col - 列索引（0-based）
   * @returns {number} 该格的值
   */
  get(row, col) {
    return this.grid[row][col];
  }

  /**
   * 设置指定坐标的值
   * @param {number} row - 行索引（0-based）
   * @param {number} col - 列索引（0-based）
   * @param {number} value - 要设置的值
   */
  set(row, col, value) {
    this.grid[row][col] = value;
  }

  /**
   * 深拷贝棋盘
   * @returns {Board} 一个全新的 Board 实例，与原棋盘数据完全独立
   */
  clone() {
    const newBoard = new Board(this.size);
    for (let r = 0; r < this.size; r++) {
      for (let c = 0; c < this.size; c++) {
        newBoard.grid[r][c] = this.grid[r][c];
      }
    }
    return newBoard;
  }

  /**
   * 获取所有空格（值为 0）的坐标
   * @returns {Array<{row: number, col: number}>} 空格坐标数组
   */
  getEmptyCells() {
    const emptyCells = [];
    for (let r = 0; r < this.size; r++) {
      for (let c = 0; c < this.size; c++) {
        if (this.grid[r][c] === 0) {
          emptyCells.push({ row: r, col: c });
        }
      }
    }
    return emptyCells;
  }

  /**
   * 遍历所有格子
   * @param {function(number, number, number): void} callback - (row, col, value) => ...
   */
  forEach(callback) {
    for (let r = 0; r < this.size; r++) {
      for (let c = 0; c < this.size; c++) {
        callback(r, c, this.grid[r][c]);
      }
    }
  }
};

// ============================================================
//  一维左滑核心算法
// ============================================================

/**
 * slideRowLeft — 一维左滑核心算法（挂载到 window 以便测试）
 */

/**
 * 一维左滑核心算法
 *
 * 实现思路（与 2048 官方规则一致）：
 *   1. 过滤掉 0，保留非零元素
 *   2. 从左到右遍历，若当前元素与下一个元素相同，则合并（左侧×2），
 *      并跳过已合并的下一个元素（i++）
 *   3. 再次过滤 0（合并过程中不会产生 0，此处为保险）
 *   4. 末尾补 0 到原始长度
 *
 * @param {number[]} row - 一维数组，长度任意
 * @returns {{ row: number[], score: number }}
 *   row  - 左滑后的结果数组
 *   score - 本次合并产生的得分（所有合并值之和）
 *
 * @example
 * slideRowLeft([0,2,0,2]) → { row: [4,0,0,0], score: 4 }
 * slideRowLeft([2,2,4,4]) → { row: [4,8,0,0], score: 12 }
 */
function slideRowLeft(row) {
  const len = row.length;
  let score = 0;

  // Step 1: 过滤 0，保留非零元素
  const nonZero = row.filter(v => v !== 0);

  // Step 2: 从左到右合并相邻相同元素
  // 同时追踪哪些位置是由合并产生的
  const merged = [];
  const isMergeResult = []; // 与 merged 一一对应，标记该位置是否由合并产生
  for (let i = 0; i < nonZero.length; i++) {
    if (i + 1 < nonZero.length && nonZero[i] === nonZero[i + 1]) {
      // 相邻相同，合并：左侧×2
      merged.push(nonZero[i] * 2);
      isMergeResult.push(true); // 此位置是合并结果
      score += nonZero[i] * 2;
      i++; // 跳过已合并的下一个元素
    } else {
      merged.push(nonZero[i]);
      isMergeResult.push(false); // 此位置不是合并结果
    }
  }

  // Step 3: 过滤 0 并同步追踪合并位置
  const result = [];
  const mergedColIndices = []; // 合并发生在结果数组的哪些列索引
  for (let i = 0; i < merged.length; i++) {
    if (merged[i] !== 0) {
      const colIdx = result.length; // 即将被 push 的位置
      result.push(merged[i]);
      if (isMergeResult[i]) {
        mergedColIndices.push(colIdx);
      }
    }
  }

  // Step 4: 末尾补 0 到原始长度
  while (result.length < len) {
    result.push(0);
  }

  return { row: result, score, mergedColIndices };
}

// ============================================================
//  四方向移动函数
// ============================================================

/**
 * 检查两个二维网格是否完全相同
 * @param {number[][]} a
 * @param {number[][]} b
 * @returns {boolean}
 */
function gridsEqual(a, b) {
  if (a.length !== b.length) return false;
  for (let r = 0; r < a.length; r++) {
    if (a[r].length !== b[r].length) return false;
    for (let c = 0; c < a[r].length; c++) {
      if (a[r][c] !== b[r][c]) return false;
    }
  }
  return true;
}

/**
 * 对二维网格应用逐行左滑
 * @param {number[][]} grid - 二维数组
 * @returns {{ grid: number[][], score: number, moved: boolean }}
 */
function moveLeft(grid) {
  const size = grid.length;
  // 深拷贝一份 grid
  const newGrid = grid.map(row => [...row]);
  let totalScore = 0;
  const mergedPositions = []; // 收集合并位置

  // 对每一行执行左滑
  for (let r = 0; r < size; r++) {
    const result = slideRowLeft(newGrid[r]);
    newGrid[r] = result.row;
    totalScore += result.score;
    // 记录此行中的合并列位置
    result.mergedColIndices.forEach(function (c) {
      mergedPositions.push({ row: r, col: c, value: result.row[c] });
    });
  }

  // 判断是否有变化
  const moved = !gridsEqual(grid, newGrid);

  return { grid: newGrid, score: totalScore, moved, mergedPositions };
}

/**
 * 右滑：每行 reverse → slideRowLeft → reverse
 * @param {number[][]} grid
 * @returns {{ grid: number[][], score: number, moved: boolean }}
 */
function moveRight(grid) {
  const size = grid.length;
  // 先对每行做 reverse，等价于将右滑转为左滑
  const reversed = grid.map(row => [...row].reverse());
  const result = moveLeft(reversed);
  // 将结果再 reverse 回来
  const newGrid = result.grid.map(row => [...row].reverse());
  const moved = !gridsEqual(grid, newGrid);

  // 转换合并位置：左滑时的 col 需要映射回右滑后的位置
  // 右滑时每行先 reverse，所以左滑时的 col → size-1-col
  const mergedPositions = result.mergedPositions.map(function (pos) {
    return { row: pos.row, col: size - 1 - pos.col, value: pos.value };
  });

  return { grid: newGrid, score: result.score, moved, mergedPositions };
}

/**
 * 辅助：矩阵转置（行变列、列变行）
 * @param {number[][]} grid
 * @returns {number[][]}
 */
function transpose(grid) {
  const size = grid.length;
  const transposed = Array.from({ length: size }, (_, c) =>
    Array.from({ length: size }, (_, r) => grid[r][c])
  );
  return transposed;
}

/**
 * 上滑：转置 → moveLeft → 转置还原
 * @param {number[][]} grid
 * @returns {{ grid: number[][], score: number, moved: boolean }}
 */
function moveUp(grid) {
  const transposed = transpose(grid);
  const result = moveLeft(transposed);
  const newGrid = transpose(result.grid);
  const moved = !gridsEqual(grid, newGrid);

  // 转换合并位置：左滑是在转置后的 grid 上操作的，
  // 所以 (row=r, col=c) 对应原 grid 的 (row=c, col=r)
  const mergedPositions = result.mergedPositions.map(function (pos) {
    return { row: pos.col, col: pos.row, value: pos.value };
  });

  return { grid: newGrid, score: result.score, moved, mergedPositions };
}

/**
 * 下滑：转置 → moveRight → 转置还原
 * @param {number[][]} grid
 * @returns {{ grid: number[][], score: number, moved: boolean }}
 */
function moveDown(grid) {
  const transposed = transpose(grid);
  const result = moveRight(transposed);
  const newGrid = transpose(result.grid);
  const moved = !gridsEqual(grid, newGrid);

  // 转换合并位置：先 right (reverse+left) 再 transpose 的组合变换
  // right 在转置上操作 → 先映射回转置坐标 → 再转置回原坐标
  const mergedPositions = result.mergedPositions.map(function (pos) {
    return { row: pos.col, col: pos.row, value: pos.value };
  });

  return { grid: newGrid, score: result.score, moved, mergedPositions };
}

// 方向映射表，方便 GameEngine 调用
const DIRECTION_MAP = {
  left:  moveLeft,
  right: moveRight,
  up:    moveUp,
  down:  moveDown,
};

// ============================================================
//  游戏状态检测
// ============================================================

/**
 * 判断游戏是否结束
 *
 * 结束条件：无空格 ∧ 无水平相邻相同 ∧ 无垂直相邻相同
 *
 * @param {number[][]} grid - 二维网格
 * @returns {boolean} true 表示游戏结束
 */
function isGameOver(grid) {
  const size = grid.length;

  // 检查是否有空格
  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size; c++) {
      if (grid[r][c] === 0) return false;
    }
  }

  // 检查水平相邻是否有相同值
  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size - 1; c++) {
      if (grid[r][c] === grid[r][c + 1]) return false;
    }
  }

  // 检查垂直相邻是否有相同值
  for (let c = 0; c < size; c++) {
    for (let r = 0; r < size - 1; r++) {
      if (grid[r][c] === grid[r + 1][c]) return false;
    }
  }

  return true;
}

/**
 * 判断玩家是否获胜（达到 2048）
 * @param {number[][]} grid
 * @returns {boolean}
 */
function hasWon(grid) {
  for (let r = 0; r < grid.length; r++) {
    for (let c = 0; c < grid[r].length; c++) {
      if (grid[r][c] >= 2048) return true;
    }
  }
  return false;
}

// ============================================================
//  GameEngine 类：游戏引擎，封装完整游戏逻辑
// ============================================================

/**
 * @class GameEngine
 * @description 2048 游戏主引擎，管理棋盘状态、分数、游戏结束/胜利判定。
 *
 * @property {Board}   grid       - 棋盘实例
 * @property {number}  score      - 当前分数
 * @property {number}  bestScore  - 历史最高分
 * @property {boolean} isGameOver - 是否游戏结束
 * @property {boolean} hasWon     - 是否获胜
 */
window.GameEngine = class GameEngine {
  constructor() {
    /** @type {Board} 棋盘实例 */
    this.grid = new window.Board(4);
    /** @type {number} 当前分数 */
    this.score = 0;
    /** @type {number} 历史最高分 */
    this.bestScore = 0;
    /** @type {boolean} 游戏是否结束 */
    this.isGameOver = false;
    /** @type {boolean} 是否已获胜 */
    this.hasWon = false;

    // 从 localStorage 恢复历史最高分
    try {
      const saved = localStorage.getItem('2048-best-score');
      if (saved !== null) {
        this.bestScore = parseInt(saved, 10) || 0;
      }
    } catch (e) {
      // localStorage 不可用时忽略（如某些浏览器禁用或 Safari 隐私模式）
    }
  }

  /**
   * 设置新游戏：重置所有状态，并自动添加两个随机方块
   */
  setupNewGame() {
    // 重置棋盘
    this.grid = new window.Board(4);
    this.score = 0;
    this.isGameOver = false;
    this.hasWon = false;
    this._continueMode = false;  // 重置继续模式标志

    // 添加初始两个随机方块
    this.addRandomTile();
    this.addRandomTile();
  }

  /**
   * 在随机空格中生成一个新方块
   * 90% 概率生成 2，10% 概率生成 4
   *
   * @returns {{ row: number, col: number, value: number } | null}
   *   返回新方块的位置和值，棋盘满时返回 null
   */
  addRandomTile() {
    const emptyCells = this.grid.getEmptyCells();
    if (emptyCells.length === 0) return null;

    // 随机选一个空格
    const { row, col } = emptyCells[Math.floor(Math.random() * emptyCells.length)];

    // 90% 概率为 2，10% 概率为 4
    const value = Math.random() < 0.9 ? 2 : 4;
    this.grid.set(row, col, value);
    return { row, col, value };
  }

  /**
   * 执行一次方向移动
   *
   * @param {'up'|'down'|'left'|'right'} direction - 移动方向
   * @returns {{ moved: boolean, score: number, gameOver: boolean, won: boolean }}
   *   moved    - 是否有实际移动（true 表示棋盘发生了变化）
   *   score    - 本次移动合并获得的新增分数
   *   gameOver - 移动后游戏是否结束
   *   won      - 移动后玩家是否获胜
   */
  move(direction) {
    // 如果游戏已结束或已获胜，拒绝移动
    if (this.isGameOver || this.hasWon) {
      return { moved: false, score: 0, gameOver: this.isGameOver, won: this.hasWon };
    }

    // 获取对应方向的移动函数
    const moveFn = DIRECTION_MAP[direction];
    if (!moveFn) {
      throw new Error(`Invalid direction: "${direction}". Use 'up', 'down', 'left', or 'right'.`);
    }

    // 执行移动
    const gridArray = this.grid.grid;
    const result = moveFn(gridArray);

    // 如果无变化，直接返回
    if (!result.moved) {
      return { moved: false, score: 0, gameOver: this.isGameOver, won: this.hasWon };
    }

    // 应用新棋盘
    this.grid.grid = result.grid;

    // 合并位置已由方向函数精确计算（基于 slideRowLeft 的合并追踪）
    const mergedPositions = result.mergedPositions || [];

    // 累加分数
    this.score += result.score;

    // 更新最高分并持久化到 localStorage
    if (this.score > this.bestScore) {
      this.bestScore = this.score;
      try {
        localStorage.setItem('2048-best-score', String(this.bestScore));
      } catch (e) {
        // localStorage 不可用时忽略
      }
    }

    // 添加随机新方块并记录位置
    const newTile = this.addRandomTile();

    // 检查游戏是否结束
    this.isGameOver = isGameOver(this.grid.grid);

    // 检查是否获胜：
    // - 正常模式：如果 hasWon 为 false，检测棋盘
    // - 继续模式（玩家已点击继续挑战）：不再自动触发获胜覆盖层，
    //   除非玩家明确需要再提示。原版 2048 在继续后不再弹出获胜提示。
    if (!this.hasWon && !this._continueMode) {
      this.hasWon = hasWon(this.grid.grid);
    }

    return {
      moved: true,
      score: result.score,
      gameOver: this.isGameOver,
      won: this.hasWon,
      newTile: newTile,              // 新增：新方块位置
      mergedPositions: mergedPositions, // 新增：合并位置列表
    };
  }

  /**
   * 获取当前全部状态（用于 UI 渲染）
   * @returns {{ grid: number[][], score: number, bestScore: number, isGameOver: boolean, hasWon: boolean }}
   */
  getState() {
    return {
      grid: this.grid.grid,
      score: this.score,
      bestScore: this.bestScore,
      isGameOver: this.isGameOver,
      hasWon: this.hasWon,
    };
  }

  /**
   * 继续游戏（获胜后解除获胜状态，允许继续操作）
   * 隐藏获胜覆盖层后调用此方法，以便玩家继续挑战更高分数
   * 进入继续模式后不再自动触发获胜检测
   */
  continueGame() {
    this.hasWon = false;
    this._continueMode = true;
  }
};

// ============================================================
//  导出辅助函数到 window（供测试和外部访问）
// ============================================================

// 确保所有内部函数/类都导出到 window
// 注意：Board 和 GameEngine 已直接赋值到 window，
// 此处补充导出未自动挂载的辅助函数
Object.assign(window, {
  slideRowLeft,
  moveLeft,
  moveRight,
  moveUp,
  moveDown,
  isGameOver,
  hasWon,
  gridsEqual,
  transpose,
});

// ============================================================
//  单元测试 — 取消注释下方代码块以在 Node.js 中运行测试
// ============================================================

// 使用 const { ... } = window 获取引用，保证 Node.js 和浏览器均可用
/*
(function runTests() {
  const {
    slideRowLeft: _slideRowLeft,
    Board: _Board,
    moveLeft: _moveLeft,
    moveRight: _moveRight,
    moveUp: _moveUp,
    moveDown: _moveDown,
    isGameOver: _isGameOver,
    hasWon: _hasWon,
    GameEngine: _GameEngine,
  } = window;

  // ---- slideRowLeft 测试 ----
  // 测试 1：[0,2,0,2] → [4,0,0,0], score=4
  let res = _slideRowLeft([0, 2, 0, 2]);
  console.assert(
    JSON.stringify(res.row) === JSON.stringify([4, 0, 0, 0]) && res.score === 4,
    `Test 1 FAIL: ${JSON.stringify(res)}`
  );
  // 测试 2：[2,2,4,4] → [4,8,0,0], score=12
  res = _slideRowLeft([2, 2, 4, 4]);
  console.assert(
    JSON.stringify(res.row) === JSON.stringify([4, 8, 0, 0]) && res.score === 12,
    `Test 2 FAIL: ${JSON.stringify(res)}`
  );
  // 测试 3：[2,0,2,4] → [4,4,0,0], score=4
  res = _slideRowLeft([2, 0, 2, 4]);
  console.assert(
    JSON.stringify(res.row) === JSON.stringify([4, 4, 0, 0]) && res.score === 4,
    `Test 3 FAIL: ${JSON.stringify(res)}`
  );
  // 测试 4：[2,2,2,0] → [4,2,0,0], score=4 （不链式合并）
  res = _slideRowLeft([2, 2, 2, 0]);
  console.assert(
    JSON.stringify(res.row) === JSON.stringify([4, 2, 0, 0]) && res.score === 4,
    `Test 4 FAIL: ${JSON.stringify(res)}`
  );
  // 测试 5：[4,4,4,4] → [8,8,0,0], score=16
  res = _slideRowLeft([4, 4, 4, 4]);
  console.assert(
    JSON.stringify(res.row) === JSON.stringify([8, 8, 0, 0]) && res.score === 16,
    `Test 5 FAIL: ${JSON.stringify(res)}`
  );
  // ---- Board 类测试 ----
  const board = new _Board(4);
  console.assert(board.size === 4, 'Board size should be 4');
  console.assert(board.grid.length === 4, 'Grid should have 4 rows');
  console.assert(board.grid[0].length === 4, 'Each row should have 4 columns');
  console.assert(board.get(0, 0) === 0, 'All cells should be 0 initially');

  board.set(1, 2, 8);
  console.assert(board.get(1, 2) === 8, 'get/set should work');

  const cloned = board.clone();
  console.assert(cloned.get(1, 2) === 8, 'Clone should preserve values');
  cloned.set(1, 2, 16);
  console.assert(board.get(1, 2) === 8, 'Clone should be independent from original');

  const emptyCells = board.getEmptyCells();
  console.assert(emptyCells.length === 15, 'Should have 15 empty cells (one is 8)');

  // ---- moveLeft 集成测试 ----
  const testGrid = [
    [0, 2, 0, 2],
    [2, 2, 4, 4],
    [2, 0, 2, 4],
    [2, 2, 2, 0],
  ];
  const moveResult = _moveLeft(testGrid);
  const expectedGrid = [
    [4, 0, 0, 0],
    [4, 8, 0, 0],
    [4, 4, 0, 0],
    [4, 2, 0, 0],
  ];
  console.assert(
    JSON.stringify(moveResult.grid) === JSON.stringify(expectedGrid),
    `moveLeft integration FAIL: ${JSON.stringify(moveResult.grid)}`
  );
  console.assert(moveResult.score === 4 + 12 + 4 + 4, `moveLeft score FAIL: ${moveResult.score}`);
  console.assert(moveResult.moved === true, 'moveLeft should report moved=true');

  // 测试无变化的情况
  const noMoveGrid = [
    [4, 0, 0, 0],
    [4, 8, 0, 0],
  ];
  const noMoveResult = _moveLeft(noMoveGrid);
  console.assert(noMoveResult.moved === false, 'No-move grid should report moved=false');

  // ---- isGameOver 测试 ----
  // 可继续移动的棋盘 — 有空格
  const notFullGrid = [
    [2, 4, 8, 16],
    [32, 64, 128, 256],
    [512, 1024, 0, 2],
    [4, 8, 16, 32],
  ];
  console.assert(_isGameOver(notFullGrid) === false, 'Grid with empty cell should NOT be game over');

  // 满格但仍有相邻相同
  const fullWithMergeGrid = [
    [2, 4, 8, 16],
    [32, 64, 128, 256],
    [512, 1024, 2, 2],
    [4, 8, 16, 32],
  ];
  console.assert(_isGameOver(fullWithMergeGrid) === false, 'Full grid with adjacent equal should NOT be game over');

  // 真正游戏结束：无空格，无相邻相同
  const deadGrid = [
    [2, 4, 8, 16],
    [32, 64, 128, 256],
    [512, 1024, 2, 4],
    [8, 16, 32, 64],
  ];
  console.assert(_isGameOver(deadGrid) === true, 'Dead grid should be game over');

  // ---- hasWon 测试 ----
  const notWonGrid = [
    [2, 4, 8, 16],
    [32, 64, 128, 256],
  ];
  console.assert(_hasWon(notWonGrid) === false, 'No 2048 should not be won');

  const wonGrid = [
    [2, 4, 8, 16],
    [32, 64, 128, 256],
    [512, 1024, 2048, 0],
    [0, 0, 0, 0],
  ];
  console.assert(_hasWon(wonGrid) === true, 'Grid with 2048 should be won');

  // ---- moveRight / moveUp / moveDown 基础测试 ----
  const simpleGrid = [
    [0, 0, 0, 2],
    [0, 0, 0, 2],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
  ];

  // moveRight: reverse → left → reverse 后应无变化
  const rightRes = _moveRight(simpleGrid);
  console.assert(rightRes.moved === false, 'moveRight: single tile on right edge should not move');

  // moveUp: 转置后左滑，列 3 的两个 2 会滑动合并到 (0, 3)
  const upRes = _moveUp(simpleGrid);
  console.assert(upRes.moved === true, 'moveUp should merge the two 2s');
  console.assert(upRes.grid[0][3] === 4, `moveUp should merge to 4 at (0,3), got ${JSON.stringify(upRes.grid)}`);
  console.assert(upRes.score === 4, 'moveUp score should be 4');

  // ---- GameEngine 基础测试 ----
  const engine = new _GameEngine();
  console.assert(engine.score === 0, 'Initial score should be 0');
  console.assert(engine.isGameOver === false, 'Initial game should not be over');
  console.assert(engine.hasWon === false, 'Initial game should not be won');

  engine.setupNewGame();
  console.assert(engine.score === 0, 'After setup, score should be 0');

  // 检查 setupNewGame 后棋盘有两个非零格子
  let nonZeroCount = 0;
  engine.grid.forEach((r, c, v) => {
    if (v !== 0) nonZeroCount++;
  });
  console.assert(nonZeroCount === 2, `After setup, should have 2 tiles, got ${nonZeroCount}`);

  // 测试移动拒绝：游戏结束时
  engine.isGameOver = true;
  const moveResult2 = engine.move('left');
  console.assert(moveResult2.moved === false, 'Should reject move when game is over');
  engine.isGameOver = false;

})();
*/
