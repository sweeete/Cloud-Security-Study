// ===== CryptoQuant 主应用逻辑 =====

let chart = null;
let chartSeries = null;
const REFRESH_INTERVAL = 10000; // 10秒刷新

// ===== 导航 =====
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        this.classList.add('active');
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        document.getElementById('tab-' + this.dataset.tab).classList.add('active');

        // 进入 tab 时加载数据
        const tab = this.dataset.tab;
        if (tab === 'dashboard') loadTickers();
        else if (tab === 'market') loadChart();
        else if (tab === 'strategies') loadStrategies();
        else if (tab === 'portfolio') loadPortfolio();
        else if (tab === 'orders') { loadOrders(); loadTradeLogs(); }
        else if (tab === 'settings') loadSettings();
    });
});

// ===== 定时刷新 =====
setInterval(() => {
    const active = document.querySelector('.nav-item.active');
    if (active) {
        const tab = active.dataset.tab;
        if (tab === 'dashboard') loadTickers();
        else if (tab === 'market') {} // 图表不自动刷新
        else if (tab === 'strategies') loadStrategies();
    }
}, REFRESH_INTERVAL);

// ===== 总览 =====
async function loadTickers() {
    const data = await API.getTickers();
    if (!data || data.error) return;

    const grid = document.getElementById('ticker-grid');
    grid.innerHTML = data.map(t => {
        const change = t.change || 0;
        const cls = change >= 0 ? 'up' : 'down';
        const sign = change >= 0 ? '+' : '';
        return `<div class="ticker-card" onclick="switchToChart('${t.symbol}')">
            <div class="ticker-symbol">${t.symbol}</div>
            <div class="ticker-price">$${formatPrice(t.last)}</div>
            <div class="ticker-change ${cls}">${sign}${change.toFixed(2)}%</div>
            <div class="ticker-volume">24h量: ${fmtVolume(t.volume)}</div>
        </div>`;
    }).join('');

    document.getElementById('overview-time').textContent =
        '更新于 ' + new Date().toLocaleTimeString('zh-CN');

    // 引擎状态
    const status = await API.getEngineStatus();
    if (status && status.active_strategies !== undefined) {
        document.getElementById('engine-status').innerHTML =
            `运行中: ${status.active_strategies} 个策略 | 引擎: ${status.running ? '🟢 运行中' : '🔴 已停止'}`;
    }
}

function switchToChart(symbol) {
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    document.querySelector('[data-tab="market"]').classList.add('active');
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.getElementById('tab-market').classList.add('active');
    document.getElementById('chart-symbol').value = symbol;
    loadChart();
}

function formatPrice(p) {
    if (!p) return '—';
    return p < 1 ? p.toFixed(6) : p < 100 ? p.toFixed(4) : p.toFixed(2);
}

function fmtVolume(v) {
    if (!v) return '—';
    if (v > 1e9) return (v / 1e9).toFixed(2) + 'B';
    if (v > 1e6) return (v / 1e6).toFixed(2) + 'M';
    if (v > 1e3) return (v / 1e3).toFixed(2) + 'K';
    return v.toFixed(2);
}

// ===== K 线图表 =====
async function loadChart() {
    const symbol = document.getElementById('chart-symbol').value;
    const tf = document.getElementById('chart-timeframe').value;

    const data = await API.getKlines(symbol, tf, 200);
    if (!data || data.error) return;

    if (!chart) {
        chart = LightweightCharts.createChart(document.getElementById('kline-chart'), {
            layout: {
                background: { color: '#1e2329' },
                textColor: '#848e9c',
            },
            grid: {
                vertLines: { color: '#2b3139' },
                horzLines: { color: '#2b3139' },
            },
            crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
            timeScale: {
                timeVisible: true,
                borderColor: '#3a3f48',
            },
            rightPriceScale: { borderColor: '#3a3f48' },
            width: document.getElementById('kline-chart').clientWidth || 800,
            height: 500,
        });

        chartSeries = chart.addCandlestickSeries({
            upColor: '#0ecb81',
            downColor: '#f6465d',
            borderDownColor: '#f6465d',
            borderUpColor: '#0ecb81',
            wickDownColor: '#f6465d',
            wickUpColor: '#0ecb81',
        });

        window.addEventListener('resize', () => {
            if (chart) {
                chart.applyOptions({
                    width: document.getElementById('kline-chart').clientWidth || 800
                });
            }
        });
    }

    chartSeries.setData(data);

    // 加载技术指标
    const indicators = await API.getIndicators(symbol, tf, 200);
    if (indicators && !indicators.error) {
        const panel = document.getElementById('indicators-content');
        const items = [
            { label: 'MA7', value: indicators.ma7 },
            { label: 'MA25', value: indicators.ma25 },
            { label: 'MA99', value: indicators.ma99 },
            { label: 'RSI(14)', value: indicators.rsi },
            { label: 'MACD', value: indicators.macd },
            { label: 'MACD Signal', value: indicators.macd_signal },
            { label: '布林上轨', value: indicators.bb_upper },
            { label: '布林下轨', value: indicators.bb_lower },
        ];
        panel.innerHTML = `<div class="indicator-grid">${items.map(i =>
            `<div class="indicator-item">
                <div class="indicator-label">${i.label}</div>
                <div class="indicator-value">${i.value != null ? formatPrice(i.value) : '—'}</div>
            </div>`
        ).join('')}</div>`;
    }
}

// ===== 策略管理 =====
async function loadStrategies() {
    const data = await API.getStrategies();
    if (!data || !data.strategies) return;

    const grid = document.getElementById('strategy-grid');
    if (data.strategies.length === 0) {
        grid.innerHTML = '<p style="color: var(--text-secondary);">暂无策略，点击右上角创建</p>';
        return;
    }

    grid.innerHTML = data.strategies.map(s => {
        const running = s.enabled ? 'running' : '';
        const statusText = s.enabled ? '🟢 运行中' : '🔴 已停止';
        return `<div class="strategy-card ${running}">
            <div class="strat-name">${s.name}</div>
            <div class="strat-type">${s.type}</div>
            <div class="strat-detail">交易对: ${s.symbol} | 状态: ${statusText}</div>
            <div class="strat-actions">
                <button class="btn-sm" onclick="toggleStrat(${s.id})">${s.enabled ? '停止' : '启动'}</button>
                <button class="btn-sm" onclick="runStrat(${s.id})">运行一次</button>
                <button class="btn-sm" style="color: var(--accent-red);" onclick="delStrat(${s.id})">删除</button>
            </div>
        </div>`;
    }).join('');
}

async function toggleStrat(id) {
    await API.toggleStrategy(id);
    loadStrategies();
}

async function runStrat(id) {
    const result = await API.runStrategy(id);
    if (result && result.action) {
        alert(`执行结果: ${result.action}\n${result.reason || ''}`);
    }
    loadStrategies();
}

async function delStrat(id) {
    if (!confirm('确定删除此策略？')) return;
    await API.deleteStrategy(id);
    loadStrategies();
}

// ===== 新建策略 =====
let availableStrategies = [];

async function showCreateStrategy() {
    availableStrategies = (await API.getAvailableStrategies())?.strategies || [];

    const sel = document.getElementById('strat-type');
    sel.innerHTML = availableStrategies.map(s =>
        `<option value="${s.id}">${s.name} - ${s.desc}</option>`
    ).join('');

    onStrategyTypeChange();
    document.getElementById('strategy-modal').classList.remove('hidden');
}

function onStrategyTypeChange() {
    const type = document.getElementById('strat-type').value;
    const paramsDiv = document.getElementById('strat-params');

    const configs = {
        'grid': `<p class="hint">网格交易参数</p>
            <div class="form-group"><label>网格下限（相对比例）</label><input type="number" id="p-lower" value="0.92" step="0.01" /></div>
            <div class="form-group"><label>网格上限（相对比例）</label><input type="number" id="p-upper" value="1.08" step="0.01" /></div>
            <div class="form-group"><label>网格数量</label><input type="number" id="p-count" value="10" /></div>
            <div class="form-group"><label>总投资额 (USDT)</label><input type="number" id="p-invest" value="100" /></div>
            <div class="form-group"><label>K线周期</label><select id="p-interval"><option value="1h">1小时</option><option value="4h">4小时</option><option value="1d">日线</option></select></div>`,
        'ma_cross': `<p class="hint">均线交叉参数</p>
            <div class="form-group"><label>短期均线周期</label><input type="number" id="p-fast" value="7" /></div>
            <div class="form-group"><label>长期均线周期</label><input type="number" id="p-slow" value="25" /></div>
            <div class="form-group"><label>交易数量</label><input type="number" id="p-amount" value="0.001" step="0.001" /></div>
            <div class="form-group"><label>K线周期</label><select id="p-interval"><option value="1h">1小时</option><option value="4h">4小时</option><option value="1d">日线</option></select></div>`,
        'rsi': `<p class="hint">RSI 参数</p>
            <div class="form-group"><label>RSI 周期</label><input type="number" id="p-rsi-period" value="14" /></div>
            <div class="form-group"><label>超卖线</label><input type="number" id="p-oversold" value="30" /></div>
            <div class="form-group"><label>超买线</label><input type="number" id="p-overbought" value="70" /></div>
            <div class="form-group"><label>交易数量</label><input type="number" id="p-amount" value="0.001" step="0.001" /></div>
            <div class="form-group"><label>K线周期</label><select id="p-interval"><option value="1h">1小时</option><option value="4h">4小时</option><option value="1d">日线</option></select></div>`,
        'macd': `<p class="hint">MACD 参数</p>
            <div class="form-group"><label>交易数量</label><input type="number" id="p-amount" value="0.001" step="0.001" /></div>
            <div class="form-group"><label>K线周期</label><select id="p-interval"><option value="1h">1小时</option><option value="4h">4小时</option><option value="1d">日线</option></select></div>`,
        'llm': `<p class="hint">🤖 AI 智能分析 — 需要先在设置中配置 LLM API Key</p>
            <div class="form-group"><label>基础交易数量</label><input type="number" id="p-amount" value="0.001" step="0.001" /></div>
            <div class="form-group"><label>AI 分析周期</label><select id="p-interval"><option value="1h">1小时</option><option value="4h">4小时</option><option value="1d">日线</option></select></div>
            <p class="hint">提示：AI 策略会综合 K 线数据和技术指标，调用大模型分析后决定买卖</p>`,
    };

    paramsDiv.innerHTML = configs[type] || '<p>选择策略类型...</p>';
}

async function createStrategy() {
    const name = document.getElementById('strat-name').value;
    const type = document.getElementById('strat-type').value;
    const symbol = document.getElementById('strat-symbol').value;
    const interval = document.getElementById('p-interval')?.value || '1h';

    let config = { interval };
    if (type === 'grid') {
        config.lower_price = parseFloat(document.getElementById('p-lower').value);
        config.upper_price = parseFloat(document.getElementById('p-upper').value);
        config.grid_count = parseInt(document.getElementById('p-count').value);
        config.investment = parseFloat(document.getElementById('p-invest').value);
    } else if (type === 'ma_cross') {
        config.fast_period = parseInt(document.getElementById('p-fast').value);
        config.slow_period = parseInt(document.getElementById('p-slow').value);
        config.trade_amount = parseFloat(document.getElementById('p-amount').value);
    } else if (type === 'rsi') {
        config.rsi_period = parseInt(document.getElementById('p-rsi-period').value);
        config.oversold = parseInt(document.getElementById('p-oversold').value);
        config.overbought = parseInt(document.getElementById('p-overbought').value);
        config.trade_amount = parseFloat(document.getElementById('p-amount').value);
    } else if (type === 'macd') {
        config.trade_amount = parseFloat(document.getElementById('p-amount').value);
    } else if (type === 'llm') {
        config.base_amount = parseFloat(document.getElementById('p-amount').value);
    }

    if (!name) { document.getElementById('strat-error').textContent = '请输入策略名称'; return; }

    const result = await API.createStrategy({ name, type, symbol, side: 'both', config });
    if (result.ok) {
        closeModal();
        loadStrategies();
    } else {
        document.getElementById('strat-error').textContent = result.detail || '创建失败';
    }
}

function closeModal() {
    document.getElementById('strategy-modal').classList.add('hidden');
}

// ===== 持仓 =====
async function loadPortfolio() {
    const data = await API.getPortfolio();
    if (!data || !data.portfolio) return;

    const tbody = document.getElementById('portfolio-body');
    if (data.portfolio.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:var(--text-secondary);">暂无持仓</td></tr>';
        return;
    }

    const tickers = await API.getTickers();
    const priceMap = {};
    if (Array.isArray(tickers)) {
        tickers.forEach(t => { priceMap[t.symbol] = t.last; });
    }

    tbody.innerHTML = data.portfolio.map(p => {
        const curPrice = priceMap[p.symbol] || 0;
        const pnl = curPrice > 0 && p.avg_price > 0 ?
            (curPrice - p.avg_price) * p.amount : 0;
        const pnlCls = pnl >= 0 ? 'up-text' : 'down-text';
        return `<tr>
            <td><strong>${p.symbol}</strong></td>
            <td>${p.amount.toFixed(6)}</td>
            <td>$${formatPrice(p.avg_price)}</td>
            <td>$${formatPrice(curPrice)}</td>
            <td class="${pnlCls}">${pnl >= 0 ? '+' : ''}$${pnl.toFixed(2)}</td>
        </tr>`;
    }).join('');
}

// ===== 订单 & 日志 =====
async function loadOrders() {
    const data = await API.getOrders();
    if (!data || !data.orders) return;

    const tbody = document.getElementById('orders-body');
    if (data.orders.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--text-secondary);">暂无订单</td></tr>';
        return;
    }

    tbody.innerHTML = data.orders.map(o => {
        const sideCls = o.side === 'buy' ? 'up-text' : 'down-text';
        return `<tr>
            <td>${o.created_at}</td>
            <td>${o.symbol}</td>
            <td class="${sideCls}">${o.side.toUpperCase()}</td>
            <td>$${formatPrice(o.price)}</td>
            <td>${o.amount}</td>
            <td>$${o.cost ? o.cost.toFixed(2) : '—'}</td>
            <td>${o.status}</td>
        </tr>`;
    }).join('');
}

async function loadTradeLogs() {
    const data = await API.getTradeLogs();
    if (!data || !data.logs) return;

    const box = document.getElementById('trade-logs');
    box.innerHTML = data.logs.map(l =>
        `<div class="log-entry">
            <span class="log-time">${l.created_at}</span>
            <span>[${l.action.toUpperCase()}]</span>
            <span>${l.symbol}</span>
            <span>${l.detail}</span>
        </div>`
    ).join('') || '<div style="color:var(--text-secondary);">暂无日志</div>';
}

// ===== 设置 =====
async function loadSettings() {
    const ex = await API.getExchangeStatus();
    if (ex && ex.configured) {
        document.getElementById('ex-status').textContent = '✅ 已配置 ' + ex.exchange + (ex.testnet ? ' (测试网)' : '');
    }

    const llm = await API.getLLMStatus();
    if (llm && llm.configured) {
        document.getElementById('llm-status').textContent = `✅ 已配置: ${llm.provider} / ${llm.model}`;
    }
}

async function saveExchangeKeys() {
    const data = {
        apiKey: document.getElementById('ex-api-key').value,
        secret: document.getElementById('ex-secret').value,
        password: document.getElementById('ex-password').value,
        testnet: document.getElementById('ex-testnet').checked,
    };
    const result = await API.saveExchangeKeys(data);
    document.getElementById('ex-status').textContent = result.ok ? '✅ 保存成功' : '❌ 保存失败';
}

async function saveLLMKeys() {
    const provider = document.getElementById('llm-provider').value;
    const data = {
        provider,
        apiKey: document.getElementById('llm-api-key').value,
        model: document.getElementById('llm-model').value,
    };
    const result = await API.saveLLMKeys(data);
    document.getElementById('llm-status').textContent = result.ok ? '✅ 保存成功' : '❌ 保存失败';
}

// ===== 退出 =====
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = '/';
}

// ===== 初始化 =====
window.onload = function() {
    const token = localStorage.getItem('token');
    if (!token) { window.location.href = '/'; return; }

    document.getElementById('user-display').textContent =
        localStorage.getItem('username') || 'admin';

    loadTickers();
};
