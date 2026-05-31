// ===== CryptoQuant API 客户端 =====

const API = {
    async request(path, options = {}) {
        const token = localStorage.getItem('token');
        const headers = { 'Content-Type': 'application/json', ...options.headers };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch(path, { ...options, headers });
        if (res.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/';
            return;
        }
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
            return {
                error: data.detail || data.error || `请求失败: HTTP ${res.status}`,
                status: res.status,
            };
        }
        return data;
    },

    get(path) { return this.request(path); },
    post(path, data) { return this.request(path, { method: 'POST', body: JSON.stringify(data) }); },
    put(path, data) { return this.request(path, { method: 'PUT', body: JSON.stringify(data) }); },
    del(path) { return this.request(path, { method: 'DELETE' }); },

    // 市场数据
    getTickers() { return this.get('/api/market/tickers'); },
    getKlines(symbol, tf, limit) { return this.get(`/api/market/klines/${symbol}?timeframe=${tf}&limit=${limit}`); },
    getIndicators(symbol, tf, limit) { return this.get(`/api/market/indicators/${symbol}?timeframe=${tf}&limit=${limit}`); },

    // 策略
    getStrategies() { return this.get('/api/strategies'); },
    createStrategy(data) { return this.post('/api/strategies', data); },
    toggleStrategy(id) { return this.post(`/api/strategies/${id}/toggle`); },
    deleteStrategy(id) { return this.del(`/api/strategies/${id}`); },
    runStrategy(id) { return this.post(`/api/strategies/${id}/run`); },
    getAvailableStrategies() { return this.get('/api/strategies/list-available'); },

    // 设置
    getExchangeStatus() { return this.get('/api/exchange/status'); },
    saveExchangeKeys(data) { return this.post('/api/exchange/keys', data); },
    getLLMStatus() { return this.get('/api/llm/status'); },
    saveLLMKeys(data) { return this.post('/api/llm/keys', data); },

    // 数据
    getPortfolio() { return this.get('/api/portfolio'); },
    getOrders() { return this.get('/api/orders'); },
    getTradeLogs() { return this.get('/api/trade-logs'); },
    getEngineStatus() { return this.get('/api/engine/status'); },
};
