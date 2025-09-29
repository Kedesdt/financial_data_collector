/**
 * Dashboard Financeiro - JavaScript Interativo
 * WebSockets, Charts e UI responsiva
 */

class FinancialDashboard {
    constructor() {
        this.socket = null;
        this.charts = {};
        this.lastData = null;
        this.isConnected = false;
        
        this.init();
    }
    
    init() {
        // Inicializa Socket.IO
        this.initSocket();
        
        // Inicializa event listeners
        this.initEventListeners();
        
        // Inicializa charts
        this.initCharts();
        
        // Carrega dados iniciais
        this.loadInitialData();
        
        // Atualiza relógio
        this.updateClock();
        setInterval(() => this.updateClock(), 1000);
    }
    
    initSocket() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('🔌 Conectado ao servidor');
            this.isConnected = true;
            this.updateStatus('online');
        });
        
        this.socket.on('disconnect', () => {
            console.log('🔌 Desconectado do servidor');
            this.isConnected = false;
            this.updateStatus('offline');
        });
        
        this.socket.on('data_update', (data) => {
            console.log('📊 Dados atualizados via WebSocket');
            this.updateDashboard(data.data);
            this.updateLastUpdateTime(data.timestamp);
        });
        
        this.socket.on('error', (error) => {
            console.error('❌ Erro WebSocket:', error);
            this.showError('Erro na conexão: ' + error.message);
        });
    }
    
    initEventListeners() {
        // Botão refresh
        document.getElementById('refresh-btn').addEventListener('click', () => {
            this.manualRefresh();
        });
        
        // Resize charts
        window.addEventListener('resize', () => {
            Object.values(this.charts).forEach(chart => {
                if (chart) chart.resize();
            });
        });
    }
    
    initCharts() {
        // Chart de câmbio
        const cambioCtx = document.getElementById('cambio-chart');
        if (cambioCtx) {
            this.charts.cambio = new Chart(cambioCtx, {
                type: 'bar',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Variação (%)',
                        data: [],
                        backgroundColor: [],
                        borderColor: [],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(0,0,0,0.8)',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            borderColor: '#007bff',
                            borderWidth: 1
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255,255,255,0.1)' },
                            ticks: { color: '#fff' }
                        },
                        x: {
                            grid: { color: 'rgba(255,255,255,0.1)' },
                            ticks: { color: '#fff' }
                        }
                    }
                }
            });
        }
        
        // Chart da bolsa
        const bolsaCtx = document.getElementById('bolsa-chart');
        if (bolsaCtx) {
            this.charts.bolsa = new Chart(bolsaCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Performance (%)',
                        data: [],
                        borderColor: '#20c997',
                        backgroundColor: 'rgba(32, 201, 151, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(0,0,0,0.8)',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            borderColor: '#20c997',
                            borderWidth: 1
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255,255,255,0.1)' },
                            ticks: { color: '#fff' }
                        },
                        x: {
                            grid: { color: 'rgba(255,255,255,0.1)' },
                            ticks: { color: '#fff' }
                        }
                    }
                }
            });
        }
    }
    
    async loadInitialData() {
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/data');
            const result = await response.json();
            
            if (result.success) {
                this.updateDashboard(result.data);
                this.updateLastUpdateTime(result.last_update);
            } else {
                this.showError('Erro ao carregar dados: ' + result.error);
            }
        } catch (error) {
            console.error('Erro ao carregar dados iniciais:', error);
            this.showError('Erro de conexão com o servidor');
        } finally {
            this.showLoading(false);
        }
    }
    
    updateDashboard(data) {
        this.lastData = data;
        
        // Atualiza status do mercado
        this.updateMarketStatus(data.market_status);
        
        // Atualiza dados de câmbio
        this.updateCambioSection(data.cambio);
        
        // Atualiza dados da bolsa
        this.updateBolsaSection(data.bolsa);
        
        // Atualiza charts
        this.updateCharts(data);
        
        // Verifica alertas
        this.updateAlertas(data);
    }
    
    updateMarketStatus(marketStatus) {
        const statusElement = document.getElementById('market-status');
        
        if (marketStatus && marketStatus.B3) {
            const isOpen = marketStatus.B3.is_open;
            const statusText = isOpen ? 'MERCADO ABERTO' : 'MERCADO FECHADO';
            const statusClass = isOpen ? 'market-open' : 'market-closed';
            const icon = isOpen ? 'fa-check-circle' : 'fa-times-circle';
            
            statusElement.innerHTML = `
                <i class="fas ${icon} me-2"></i>
                B3: ${statusText}
            `;
            statusElement.className = `alert mb-0 text-center ${statusClass}`;
        }
    }
    
    updateCambioSection(cambioData) {
        const grid = document.getElementById('cambio-grid');
        
        if (!cambioData) {
            grid.innerHTML = '<div class="col-12 text-center">Dados de câmbio não disponíveis</div>';
            return;
        }
        
        let html = '';
        
        Object.entries(cambioData).forEach(([pair, data]) => {
            const isPositive = data.change_percent >= 0;
            const trendClass = isPositive ? 'positive' : 'negative';
            const trendIcon = isPositive ? 'fa-arrow-up' : 'fa-arrow-down';
            const flag = this.getCurrencyFlag(pair);
            
            html += `
                <div class="col-lg-4 col-md-6">
                    <div class="cotacao-card">
                        <div class="cotacao-par">
                            ${flag} ${pair}
                        </div>
                        <div class="cotacao-valor">
                            ${this.formatCurrency(data.rate)}
                        </div>
                        <div class="cotacao-variacao ${trendClass}">
                            <i class="fas ${trendIcon}"></i>
                            ${data.change_percent >= 0 ? '+' : ''}${data.change_percent.toFixed(2)}%
                        </div>
                        <div class="cotacao-fonte">
                            <i class="fas fa-database me-1"></i>
                            ${data.source}
                        </div>
                    </div>
                </div>
            `;
        });
        
        grid.innerHTML = html;
    }
    
    updateBolsaSection(bolsaData) {
        const grid = document.getElementById('bolsa-grid');
        
        if (!bolsaData) {
            grid.innerHTML = '<div class="col-12 text-center">Dados da bolsa não disponíveis</div>';
            return;
        }
        
        let html = '';
        
        Object.entries(bolsaData).forEach(([index, data]) => {
            const isPositive = data.change_percent >= 0;
            const trendClass = isPositive ? 'positive' : 'negative';
            const trendIcon = isPositive ? 'fa-arrow-up' : 'fa-arrow-down';
            const indexIcon = this.getIndexIcon(index);
            
            html += `
                <div class="col-lg-4 col-md-6">
                    <div class="cotacao-card">
                        <div class="cotacao-par">
                            ${indexIcon} ${index}
                        </div>
                        <div class="cotacao-valor">
                            ${this.formatNumber(data.price)}
                        </div>
                        <div class="cotacao-variacao ${trendClass}">
                            <i class="fas ${trendIcon}"></i>
                            ${data.change_percent >= 0 ? '+' : ''}${data.change_percent.toFixed(2)}%
                        </div>
                        <div class="cotacao-fonte">
                            <i class="fas fa-chart-line me-1"></i>
                            Volume: ${this.formatVolume(data.volume)}
                        </div>
                    </div>
                </div>
            `;
        });
        
        grid.innerHTML = html;
    }
    
    updateCharts(data) {
        // Atualiza chart de câmbio
        if (this.charts.cambio && data.cambio) {
            const cambioEntries = Object.entries(data.cambio);
            const labels = cambioEntries.map(([pair]) => pair);
            const values = cambioEntries.map(([, info]) => info.change_percent);
            const colors = values.map(val => val >= 0 ? '#20c997' : '#fd7e14');
            
            this.charts.cambio.data.labels = labels;
            this.charts.cambio.data.datasets[0].data = values;
            this.charts.cambio.data.datasets[0].backgroundColor = colors;
            this.charts.cambio.data.datasets[0].borderColor = colors;
            this.charts.cambio.update('none');
        }
        
        // Atualiza chart da bolsa
        if (this.charts.bolsa && data.bolsa) {
            const bolsaEntries = Object.entries(data.bolsa);
            const labels = bolsaEntries.map(([index]) => index);
            const values = bolsaEntries.map(([, info]) => info.change_percent);
            
            this.charts.bolsa.data.labels = labels;
            this.charts.bolsa.data.datasets[0].data = values;
            this.charts.bolsa.update('none');
        }
    }
    
    updateAlertas(data) {
        const alertasSection = document.getElementById('alertas-section');
        const alertasList = document.getElementById('alertas-list');
        
        const alertas = [];
        
        // Alertas de câmbio (variação > 2%)
        if (data.cambio) {
            Object.entries(data.cambio).forEach(([pair, info]) => {
                if (Math.abs(info.change_percent) > 2) {
                    alertas.push(`${pair}: ${info.change_percent >= 0 ? '+' : ''}${info.change_percent.toFixed(2)}%`);
                }
            });
        }
        
        // Alertas de bolsa (variação > 3%)
        if (data.bolsa) {
            Object.entries(data.bolsa).forEach(([index, info]) => {
                if (Math.abs(info.change_percent) > 3) {
                    alertas.push(`${index}: ${info.change_percent >= 0 ? '+' : ''}${info.change_percent.toFixed(2)}%`);
                }
            });
        }
        
        if (alertas.length > 0) {
            let html = '';
            alertas.forEach(alerta => {
                html += `
                    <div class="alert-item">
                        <i class="fas fa-exclamation-triangle"></i>
                        ${alerta}
                    </div>
                `;
            });
            
            alertasList.innerHTML = html;
            alertasSection.style.display = 'block';
        } else {
            alertasSection.style.display = 'none';
        }
    }
    
    manualRefresh() {
        const btn = document.getElementById('refresh-btn');
        btn.classList.add('spinning');
        
        if (this.socket && this.isConnected) {
            this.socket.emit('request_update');
        } else {
            this.loadInitialData();
        }
        
        setTimeout(() => {
            btn.classList.remove('spinning');
        }, 1000);
    }
    
    updateStatus(status) {
        const indicator = document.getElementById('status-indicator');
        
        if (status === 'online') {
            indicator.innerHTML = '<i class="fas fa-circle pulse"></i> Online';
            indicator.className = 'badge bg-success me-3';
        } else {
            indicator.innerHTML = '<i class="fas fa-circle"></i> Offline';
            indicator.className = 'badge bg-danger me-3';
        }
    }
    
    updateLastUpdateTime(timestamp) {
        const element = document.getElementById('last-update');
        
        if (timestamp) {
            const date = new Date(timestamp);
            element.innerHTML = `
                <i class="far fa-clock"></i> 
                ${date.toLocaleTimeString('pt-BR')}
            `;
        }
    }
    
    updateClock() {
        const element = document.getElementById('server-time');
        const now = new Date();
        element.textContent = now.toLocaleTimeString('pt-BR');
    }
    
    showLoading(show) {
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        
        if (show) {
            modal.show();
        } else {
            modal.hide();
        }
    }
    
    showError(message) {
        // Cria toast de erro
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-danger border-0';
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        document.body.appendChild(toast);
        const toastInstance = new bootstrap.Toast(toast);
        toastInstance.show();
        
        // Remove toast após 5 segundos
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 5000);
    }
    
    // Utility functions
    getCurrencyFlag(pair) {
        const flags = {
            'USD-BRL': '🇺🇸🇧🇷',
            'USD-EUR': '🇺🇸🇪🇺',
            'USD-JPY': '🇺🇸🇯🇵',
            'USD-CNY': '🇺🇸🇨🇳',
            'USD-INR': '🇺🇸🇮🇳',
            'USD-KRW': '🇺🇸🇰🇷'
        };
        return flags[pair] || '💱';
    }
    
    getIndexIcon(index) {
        const icons = {
            'IBOV': '🇧🇷',
            'SP500': '🇺🇸',
            'NASDAQ': '🇺🇸',
            'DOW': '🇺🇸',
            'DAX': '🇩🇪',
            'FTSE': '🇬🇧',
            'NIKKEI': '🇯🇵',
            'HANG_SENG': '🇭🇰'
        };
        return icons[index] || '📈';
    }
    
    formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            minimumFractionDigits: 4,
            maximumFractionDigits: 4
        }).format(value);
    }
    
    formatNumber(value) {
        return new Intl.NumberFormat('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(value);
    }
    
    formatVolume(value) {
        if (value >= 1000000000) {
            return (value / 1000000000).toFixed(1) + 'B';
        } else if (value >= 1000000) {
            return (value / 1000000).toFixed(1) + 'M';
        } else if (value >= 1000) {
            return (value / 1000).toFixed(1) + 'K';
        }
        return value.toString();
    }
}

// Inicializa dashboard quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new FinancialDashboard();
});