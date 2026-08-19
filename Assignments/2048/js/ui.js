/**
 * 2048 Game - UI Rendering Module
 *
 * 负责将 GameEngine 的状态渲染到 DOM。
 * 所有 DOM 操作集中在此模块中。
 */

(function () {
  'use strict';

  // ============================================================
  //  UI 对象 — 全局暴露
  // ============================================================

  window.UI = {};

  /**
   * 初始化 UI 模块
   * @param {import('./game.js').GameEngine} engine - GameEngine 实例
   */
  UI.init = function (engine) {
    UI.engine = engine;

    // 缓存 DOM 引用
    UI.boardEl = document.getElementById('board');
    UI.scoreEl = document.getElementById('score');
    UI.bestScoreEl = document.getElementById('best-score');
    UI.gameOverEl = document.getElementById('game-over-overlay');
    UI.winEl = document.getElementById('win-overlay');
    UI.restartBtn = document.getElementById('restart-btn');
    UI.tryAgainBtn = document.getElementById('try-again-btn');
    UI.continueBtn = document.getElementById('continue-btn');
    UI.finalScoreEl = document.getElementById('final-score');
    UI.winScoreEl = document.getElementById('win-score');

    // 初始化 tiles 二维数组
    UI.tiles = [];

    // 上一次 grid 快照（用于判断新方块和合并动画）
    UI.prevGrid = Array.from({ length: 4 }, () => Array(4).fill(0));

    // 构建网格 DOM
    buildGrid();

    // 绑定事件

    // 重新开始（新游戏按钮 & 游戏结束覆盖层按钮）
    UI.restartBtn.addEventListener('click', function () {
      UI.engine.setupNewGame();
      UI.update(UI.engine.getState());
    });

    UI.tryAgainBtn.addEventListener('click', function () {
      UI.engine.setupNewGame();
      UI.update(UI.engine.getState());
    });

    // 继续游戏（获胜覆盖层）— 解除获胜状态并隐藏覆盖层
    UI.continueBtn.addEventListener('click', function () {
      UI.engine.continueGame();
      UI.winEl.classList.add('hidden');
      UI.update(UI.engine.getState()); // 同步状态刷新
    });

    // 初始渲染
    UI.update(engine.getState());
  };

  /**
   * 构建网格 DOM — 在 boardEl 内创建 16 个格子
   * 注意：boardEl 内含覆盖层元素，不可整体 innerHTML 清空，
   * 需要保留覆盖层并只重建 tile 格子。
   */
  function buildGrid() {
    UI.tiles = [];

    // 清除所有现有 tile 元素（保留覆盖层和非 tile 元素）
    const existingTiles = UI.boardEl.querySelectorAll('.tile');
    existingTiles.forEach(function (t) { t.remove(); });

    // 创建 16 个新 tile
    for (let row = 0; row < 4; row++) {
      UI.tiles[row] = [];
      for (let col = 0; col < 4; col++) {
        const tile = document.createElement('div');
        tile.className = 'tile tile-empty';
        // 在第一个覆盖层之前插入（保持覆盖层在最后）
        const firstOverlay = UI.boardEl.querySelector('#game-over-overlay, #win-overlay');
        if (firstOverlay) {
          UI.boardEl.insertBefore(tile, firstOverlay);
        } else {
          UI.boardEl.appendChild(tile);
        }
        UI.tiles[row][col] = tile;
      }
    }
  }

  UI.buildGrid = buildGrid;

  /**
   * 用当前游戏状态更新 DOM
   * @param {{ grid: number[][], score: number, bestScore: number, isGameOver: boolean, hasWon: boolean }} state
   * @param {{ newTile: {row:number,col:number,value:number}|null, mergedPositions: Array<{row:number,col:number,value:number}> }} [moveResult]
   *   可选参数，由 engine.move() 返回。传入后使用精确位置信息添加动画类，替代猜测逻辑。
   */
  UI.update = function (state, moveResult) {
    const grid = state.grid;

    // 构建合并位置集合，方便 O(1) 查找
    const mergedSet = new Set();
    if (moveResult && moveResult.mergedPositions) {
      moveResult.mergedPositions.forEach(function (pos) {
        mergedSet.add(pos.row + ',' + pos.col);
      });
    }

    // 新方块位置
    let newTileKey = null;
    if (moveResult && moveResult.newTile) {
      newTileKey = moveResult.newTile.row + ',' + moveResult.newTile.col;
    }

    // 更新每个格子的内容和样式
    for (let row = 0; row < 4; row++) {
      for (let col = 0; col < 4; col++) {
        const tile = UI.tiles[row][col];
        const value = grid[row][col];
        const tileKey = row + ',' + col;

        // 设置文字内容
        tile.textContent = value > 0 ? String(value) : '';

        // 清除所有 tile-x 和 tile-empty 类，重新设置
        tile.className = 'tile';

        if (value > 0) {
          tile.classList.add('tile-' + value);

          // 超大数字兜底样式
          if (value > 262144) {
            tile.classList.add('tile-super');
          }

          // === 精确动画标记（基于 engine 返回的精确位置）===
          // 1) 新生成的方块（由 addRandomTile 产生）
          if (tileKey === newTileKey) {
            tile.classList.add('tile-new');
          }
          // 2) 合并产生的方块（值翻倍的位置）
          else if (mergedSet.has(tileKey)) {
            tile.classList.add('tile-merged');
          }
          // ================================================
        } else {
          tile.classList.add('tile-empty');
        }
      }
    }

    // 动画结束后的清理 — 使用 animationend 事件（精确）
    // 为每个有动画类的 tile 绑定一次性 animationend 事件
    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 4; c++) {
        const tile = UI.tiles[r][c];
        if (tile.classList.contains('tile-new') || tile.classList.contains('tile-merged')) {
          tile.addEventListener('animationend', function handler() {
            tile.classList.remove('tile-new', 'tile-merged');
            tile.removeEventListener('animationend', handler);
          });
        }
      }
    }

    // 保留 setTimeout 作为兼容性兜底（旧浏览器不支持 animationend）
    clearTimeout(UI._animTimer);
    UI._animTimer = setTimeout(function () {
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) {
          const tile = UI.tiles[r][c];
          if (tile.classList.contains('tile-new') || tile.classList.contains('tile-merged')) {
            tile.classList.remove('tile-new', 'tile-merged');
          }
        }
      }
    }, 300); // 略长于动画时长，仅作为 animationend 未触发的兜底

    // 更新分数
    UI.scoreEl.textContent = state.score;
    UI.bestScoreEl.textContent = state.bestScore;

    // 控制覆盖层显隐
    if (state.isGameOver) {
      UI.finalScoreEl.textContent = state.score;
      UI.gameOverEl.classList.remove('hidden');
    } else {
      UI.gameOverEl.classList.add('hidden');
    }

    if (state.hasWon) {
      UI.winScoreEl.textContent = state.score;
      UI.winEl.classList.remove('hidden');
    } else {
      UI.winEl.classList.add('hidden');
    }
  };

  // ============================================================
  //  自动初始化
  // ============================================================

  document.addEventListener('DOMContentLoaded', function () {
    const engine = new window.GameEngine();
    engine.setupNewGame();
    window.engine = engine; // 暴露到全局，方便调试

    // UI.init 只负责渲染；
    // 输入绑定在 input.js 中完成（可能尚未加载）
    UI.init(engine);
  });

})();
