# 🌐 Dashboard Web Financeiro

Uma aplicação web moderna e responsiva para visualizar dados financeiros em tempo real, desenvolvida com Flask, WebSockets e design moderno.

## ✨ Características

### 🎨 Interface Moderna
- **Design Bloomberg-style** - Interface profissional similar às telas de trading
- **Responsivo** - Funciona perfeitamente em desktop, tablet e mobile
- **Tema escuro** - Reduz fadiga visual para uso prolongado
- **Animações suaves** - Transições fluidas e feedback visual

### 🔄 Tempo Real
- **WebSockets** - Atualizações instantâneas sem refresh da página
- **Auto-refresh** - Dados atualizados a cada 30 segundos
- **Status de conexão** - Indicador visual do status da conexão
- **Refresh manual** - Botão para forçar atualização

### 📊 Visualizações
- **Cards interativos** - Cotações com animações e efeitos hover
- **Gráficos dinâmicos** - Chart.js para visualização de tendências
- **Alertas automáticos** - Notificações para variações significativas
- **Status do mercado** - Indicador se B3 está aberta/fechada

### 📱 Recursos
- **APIs RESTful** - Endpoints para integração externa
- **Dados consolidados** - Múltiplas fontes em uma interface
- **Performance otimizada** - Carregamento rápido e baixo consumo
- **Compatibilidade** - Funciona em qualquer navegador moderno

## 🚀 Como Usar

### Método 1: Launcher Principal
```bash
cd informacoes_cambio
python run.py
# Escolha opção "1" para Dashboard Web
```

### Método 2: Direto
```bash
cd informacoes_cambio/web
python run_web.py
```

### Método 3: Flask CLI
```bash
cd informacoes_cambio/web
set FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

## 🔗 URLs Disponíveis

| Endpoint | Descrição |
|----------|-----------|
| `http://localhost:5000` | Dashboard principal |
| `http://localhost:5000/api/data` | Todos os dados (JSON) |
| `http://localhost:5000/api/cambio` | Apenas câmbio (JSON) |
| `http://localhost:5000/api/bolsa` | Apenas bolsa (JSON) |
| `http://localhost:5000/api/summary` | Resumo executivo (JSON) |

## 📋 Estrutura da Interface

### 🎯 Header
- **Status de conexão** - Online/Offline em tempo real
- **Última atualização** - Timestamp da última coleta
- **Botão refresh** - Atualização manual com animação

### 💱 Seção Câmbio
- **Cards por moeda** - USD/BRL, USD/EUR, USD/JPY, etc.
- **Cotação atual** - Valor formatado com 4 decimais
- **Variação** - Percentual com cores (verde/vermelho)
- **Fonte dos dados** - Banco Central, Yahoo Finance, etc.

### 📈 Seção Bolsa
- **Cards por índice** - IBOV, SP500, NASDAQ, etc.
- **Valor atual** - Pontos formatados
- **Performance** - Variação percentual colorida
- **Volume** - Volume de negociação formatado

### 📊 Gráficos
- **Gráfico de barras** - Variação percentual do câmbio
- **Gráfico de linha** - Performance dos índices
- **Interativo** - Tooltips com detalhes ao passar o mouse
- **Responsivo** - Ajusta automaticamente ao tamanho da tela

### 🚨 Alertas
- **Aparecem automaticamente** - Para variações > 2% (câmbio) ou > 3% (bolsa)
- **Notificações visuais** - Toast messages para erros
- **Status do mercado** - Banner colorido indicando se B3 está aberta

## 🎨 Tecnologias Utilizadas

### Backend
- **Flask** - Framework web Python
- **Flask-SocketIO** - WebSockets em tempo real
- **Flask-CORS** - CORS para APIs
- **Threading** - Atualizações em background

### Frontend
- **Bootstrap 5** - Framework CSS responsivo
- **Font Awesome** - Ícones modernos
- **Chart.js** - Gráficos interativos
- **Socket.IO** - WebSockets no cliente
- **Vanilla JavaScript** - Sem dependências pesadas

### Estilização
- **CSS3 Moderno** - Grid, Flexbox, Animations
- **Gradientes** - Backgrounds elegantes
- **Tema escuro** - Interface profissional
- **Responsivo** - Mobile-first design

## 🔧 Configurações Avançadas

### Personalizar Intervalo de Atualização
```python
# Em web/app.py, linha 20
collector.update_interval = 60  # 60 segundos (padrão: 30)
```

### Alterar Porta do Servidor
```python
# Em web/app.py, última linha
socketio.run(app, host='0.0.0.0', port=8080)  # Porta 8080
```

### Configurar CORS
```python
# Em web/app.py
CORS(app, origins=['http://seu-dominio.com'])
```

## 📱 Responsividade

### Desktop (1920px+)
- Layout de 3 colunas para cards
- Gráficos lado a lado
- Header completo com todos os elementos

### Tablet (768px - 1199px)
- Layout de 2 colunas para cards
- Gráficos empilhados
- Header compacto

### Mobile (< 768px)
- Layout de 1 coluna
- Cards otimizados para touch
- Header minimalista
- Navegação otimizada

## 🚨 Alertas e Notificações

### Tipos de Alerta
1. **Variação de câmbio** > 2%
2. **Variação de bolsa** > 3%
3. **Erros de conexão** com as APIs
4. **Status do mercado** (abertura/fechamento)

### Cores dos Alertas
- 🟢 **Verde** - Variações positivas
- 🔴 **Vermelho** - Variações negativas
- 🟡 **Amarelo** - Avisos e alertas
- 🔵 **Azul** - Informações gerais

## 🔍 APIs para Integração

### Exemplo: Obter todos os dados
```javascript
fetch('http://localhost:5000/api/data')
  .then(response => response.json())
  .then(data => {
    console.log('Câmbio:', data.data.cambio);
    console.log('Bolsa:', data.data.bolsa);
  });
```

### Exemplo: WebSocket
```javascript
const socket = io('http://localhost:5000');
socket.on('data_update', (data) => {
  console.log('Dados atualizados:', data.data);
});
```

## 🎯 Casos de Uso

1. **Trading Desk** - Monitor para traders profissionais
2. **Investimentos** - Acompanhamento de carteiras
3. **Educação** - Ensino de mercados financeiros
4. **Pesquisa** - Coleta de dados para análises
5. **Dashboards corporativos** - Integração em sistemas empresariais

## 🔧 Troubleshooting

### Erro de Porta Ocupada
```bash
# Altere a porta em app.py ou termine o processo
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### WebSocket não conecta
- Verifique se o servidor Flask está rodando
- Desabilite antivírus/firewall temporariamente
- Teste com `http://localhost:5000` direto

### Dados não atualizam
- Verifique conexão com internet
- APIs podem ter rate limits
- Verifique logs do servidor

---

**Dashboard criado com ❤️ para entusiastas financeiros e desenvolvedores**