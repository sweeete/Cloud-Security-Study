/**
 * 2048 Game - Input Module
 *
 * 负责键盘和触屏事件处理。
 * 依赖全局 game.js 和 ui.js（game.js → ui.js → input.js 加载顺序）。
 *
 * 暴露全局：window.Input
 */
window.Input = {};

/**
 * 初始化输入模块
 * - 获取 engine（由 ui.js 创建并存到 window.engine）
 * - 绑定键盘事件（keydown）到 document
 * - 绑定触屏事件（touchstart, touchend）到 board 元素
 * - 注意：按钮事件（新游戏、再来一局、继续挑战）统一在 ui.js 中绑定，
 *   本模块只负责键盘和触屏输入，避免重复绑定。
 */
Input.init = function () {
  const engine = window.engine;
  const UI = window.UI;
  const board = document.getElementById('board');

  // 输入节流锁：动画播放期间忽略输入，防止动画重叠
  let _throttled = false;
  const ANIM_LOCK_MS = 200;

  function throttledMove(direction) {
    if (_throttled) return;
    _throttled = true;
    const result = engine.move(direction);
    if (result && result.moved) {
      UI.update(engine.getState(), result);
    }
    setTimeout(function () {
      _throttled = false;
    }, ANIM_LOCK_MS);
  }

  if (!engine) {
    console.warn('[Input] window.engine 未就绪，将在 DOMContentLoaded 后重试。');
    return;
  }
  if (!UI) {
    console.warn('[Input] window.UI 未就绪，将在 DOMContentLoaded 后重试。');
    return;
  }

  // ---------- 键盘事件 ----------
  document.addEventListener('keydown', function (event) {
    // 如果在输入框中触发，不处理
    const tag = event.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA') {
      return;
    }

    const key = event.key;
    let direction = null;

    switch (key) {
      case 'ArrowUp':
      case 'w':
      case 'W':
        direction = 'up';
        break;
      case 'ArrowDown':
      case 's':
      case 'S':
        direction = 'down';
        break;
      case 'ArrowLeft':
      case 'a':
      case 'A':
        direction = 'left';
        break;
      case 'ArrowRight':
      case 'd':
      case 'D':
        direction = 'right';
        break;
      case 'r':
      case 'R':
        // 重新开始 — 阻止默认行为防止页面刷新
        event.preventDefault();
        engine.setupNewGame();
        UI.update(engine.getState());
        return;
      default:
        // 非游戏按键，不处理
        return;
    }

    // 阻止方向键默认行为（页面滚动）
    if (direction) {
      event.preventDefault();
      throttledMove(direction);
    }
  });

  // ---------- 触屏事件 ----------
  let startX = 0;
  let startY = 0;

  board.addEventListener('touchstart', function (event) {
    // 仅处理单点触控
    if (event.touches.length !== 1) return;
    startX = event.touches[0].clientX;
    startY = event.touches[0].clientY;
  }, { passive: true });

  board.addEventListener('touchend', function (event) {
    // 阻止默认行为（阻止页面滑动）
    event.preventDefault();

    // 仅处理单点触控
    if (event.changedTouches.length !== 1) return;

    const endX = event.changedTouches[0].clientX;
    const endY = event.changedTouches[0].clientY;

    const deltaX = endX - startX;
    const deltaY = endY - startY;

    const absDeltaX = Math.abs(deltaX);
    const absDeltaY = Math.abs(deltaY);

    // 阈值 30px，低于阈值不触发
    if (Math.max(absDeltaX, absDeltaY) < 30) return;

    let direction = null;

    if (absDeltaX > absDeltaY) {
      // 水平方向
      direction = deltaX > 0 ? 'right' : 'left';
    } else {
      // 垂直方向
      direction = deltaY > 0 ? 'down' : 'up';
    }

    throttledMove(direction);
  }, { passive: false });
};

// ---------- 初始化执行（使用 DOMContentLoaded 确保 engine 已就绪）----------
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function () {
    // 等待 engine 创建完成（由 ui.js 在同一事件中创建）
    // 使用 requestAnimationFrame 确保 UI.init 已执行
    requestAnimationFrame(function () {
      Input.init();
    });
  });
} else {
  // DOM 已就绪，立即初始化
  Input.init();
}
