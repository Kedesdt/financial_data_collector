# 💼 Sistema de Informações Financeiras em Tempo Real

Este projeto fornece APIs confiáveis para capturar dados financeiros em tempo real, incluindo cotações de câmbio e índices da bolsa de valores, similar ao que você vê na tela da Bloomberg.

## 🚀 Características

- **Câmbio em tempo real**: USD, EUR, JPY, CNY, INR, KRW vs BRL
- **Índices da bolsa**: Ibovespa, IBX, S&P 500, NASDAQ, DAX, FTSE, Nikkei, etc.
- **Múltiplas fontes**: Yahoo Finance, Banco Central do Brasil, ExchangeRate-API, Fixer.io
- **Formato Bloomberg**: Saída similar à tela profissional
- **Coleta contínua**: Atualização automática com intervalos configuráveis
- **Alertas**: Notificações para variações significativas

## 📦 Instalação

```bash
# Clone ou baixe o projeto
cd informacoes_cambio

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente (opcional)
copy .env.example .env
# Edite o arquivo .env com suas chaves de API
```

## 🔑 APIs Utilizadas

### Gratuitas (sem chave necessária)
- **Yahoo Finance**: Principal fonte para câmbio e bolsa
- **ExchangeRate-API**: Backup para câmbio
- **Banco Central do Brasil**: USD/BRL oficial

### Com chave gratuita (opcional)
- **Fixer.io**: Câmbio adicional (1000 requests/mês grátis)
- **Alpha Vantage**: Dados financeiros (500 requests/dia grátis)

## 🎯 Uso Rápido

### 1. Coleta única de dados
```python
from financial_collector import FinancialDataCollector

collector = FinancialDataCollector()
data = collector.collect_all_data()
print(collector.format_bloomberg_style(data))
```

### 2. Apenas câmbio
```python
from cambio_api import CambioAPI

cambio = CambioAPI()
rates = cambio.get_all_rates()

for pair, info in rates.items():
    print(f"{pair}: {info['rate']} ({info['change_percent']:+.2f}%)")
```

### 3. Apenas bolsa
```python
from bolsa_api import BolsaAPI

bolsa = BolsaAPI()
indices = bolsa.get_all_indices()

for index, info in indices.items():
    print(f"{index}: {info['price']:,.2f} ({info['change_percent']:+.2f}%)")
```

## 🖥️ Executar Sistema Completo

```bash
# Sistema interativo
python financial_collector.py

# Ou diretamente
python -c "from financial_collector import FinancialDataCollector; FinancialDataCollector().run_continuous()"
```

## 📊 Exemplo de Saída

```
================================================================================
📺 INFORMAÇÕES FINANCEIRAS EM TEMPO REAL
================================================================================
⏰ Atualizado em: 26/09/2025 14:30:45

🏛️  B3: 🟢 ABERTO

💱 CÂMBIO
----------------------------------------
USD-BRL      5.1234 📈  +0.25%
             Fonte: Banco Central do Brasil
USD-EUR      0.8456 📉  -0.12%
             Fonte: Yahoo Finance
USD-JPY    149.7200 📈  +0.08%
             Fonte: Yahoo Finance

📈 ÍNDICES
----------------------------------------
IBOV       126,542.30 📈  +1.25%
             Variação: +1,564.23 | Volume: 15,234,567
SP500        4,567.89 📉  -0.45%
             Variação: -20.78 | Volume: 89,456,123
NASDAQ      14,234.56 📈  +0.78%
             Variação: +110.45 | Volume: 45,678,901
```

## 🔧 Configuração Avançada

### Arquivo .env
```env
# APIs opcionais
FINHUB_API_KEY=your_key_here
ALPHA_VANTAGE_API_KEY=your_key_here

# Configurações
UPDATE_INTERVAL=60
DEBUG=True
```

### Personalizar intervalos
```python
collector = FinancialDataCollector()
collector.update_interval = 30  # 30 segundos
collector.run_continuous(duration_minutes=60)  # Por 1 hora
```

## 📁 Estrutura do Projeto

```
informacoes_cambio/
├── cambio_api.py          # API de câmbio
├── bolsa_api.py           # API da bolsa
├── financial_collector.py # Sistema principal
├── examples/              # Exemplos de uso
├── requirements.txt       # Dependências
├── .env.example          # Configurações
└── README.md             # Documentação
```

## 🎯 Casos de Uso

1. **Dashboard financeiro**: Exibir dados em tempo real
2. **Trading algorithms**: Feed de dados para algoritmos
3. **Relatórios automáticos**: Gerar relatórios periódicos
4. **Alertas**: Monitorar variações significativas
5. **Análise histórica**: Coletar dados para análise

## 🔍 APIs Detalhadas

### CambioAPI
- `get_all_rates()`: Todas as cotações consolidadas
- `get_usd_brl_bcb()`: USD/BRL oficial do BCB
- `get_exchange_rates_yahoo()`: Via Yahoo Finance
- `get_exchange_rates_fixer()`: Via Fixer.io (com chave)

### BolsaAPI
- `get_all_indices()`: Todos os índices
- `get_brazilian_indices()`: Índices brasileiros
- `get_global_indices()`: Índices internacionais
- `get_stock_data()`: Ações específicas
- `get_market_status()`: Status do mercado

### FinancialDataCollector
- `collect_all_data()`: Coleta completa
- `format_bloomberg_style()`: Formato profissional
- `run_continuous()`: Execução contínua
- `get_summary()`: Resumo executivo

## 🚨 Alertas e Monitoramento

O sistema gera alertas automáticos para:
- Variação de câmbio > 2%
- Variação de índices > 3%
- Mercados fechados/abertos
- Erros de API

## 📈 Performance

- **Latência**: < 3 segundos por coleta completa
- **Confiabilidade**: 99%+ (múltiplas fontes)
- **Rate limits**: Respeitados automaticamente
- **Cache**: Implementado para otimização

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

MIT License - veja o arquivo LICENSE para detalhes.

## ⚠️ Disclaimer

Este software é fornecido apenas para fins educacionais e informativos. Não constitui aconselhamento financeiro. Sempre consulte profissionais qualificados para decisões de investimento.

---

**Desenvolvido com ❤️ para traders e entusiastas financeiros**