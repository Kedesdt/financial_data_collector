# 🚀 GUIA RÁPIDO DE USO

## Para executar AGORA:

### Opção 1: Launcher Principal
```bash
python run.py
```

### Opção 2: Sistema Completo
```bash
python financial_collector.py
```

### Opção 3: Apenas Câmbio
```bash
python examples/exemplo_cambio.py
```

### Opção 4: Apenas Bolsa
```bash
python examples/exemplo_bolsa.py
```

## 📊 O que você vai ver:

```
================================================================================
📺 INFORMAÇÕES FINANCEIRAS EM TEMPO REAL
================================================================================
⏰ Atualizado em: 26/09/2025 22:03:45

🏛️  B3: 🟢 ABERTO

💱 CÂMBIO
----------------------------------------
USD-BRL      5.3439 📈  +0.25%
             Fonte: Banco Central do Brasil
USD-EUR      0.8550 📉  -0.12%
             Fonte: Yahoo Finance
USD-JPY    149.5800 📈  +0.08%
             Fonte: Yahoo Finance

📈 ÍNDICES
----------------------------------------
IBOV       126,542.30 📈  +1.25%
             Variação: +1,564.23 | Volume: 15,234,567
```

## 🔧 APIs Utilizadas:

✅ **Yahoo Finance** - Principal fonte (gratuita)
✅ **Banco Central do Brasil** - USD/BRL oficial  
✅ **ExchangeRate-API** - Backup gratuito
⚠️ **Fixer.io** - Opcional (requer chave gratuita)

## 🎯 Funcionalidades:

- ✅ Câmbio em tempo real (USD, EUR, JPY, CNY, INR, KRW vs BRL)
- ✅ Ibovespa, IBX e índices globais
- ✅ Atualização automática
- ✅ Alertas para variações significativas
- ✅ Exportação JSON/CSV
- ✅ Formato Bloomberg profissional

## ⚡ Uso Programático:

```python
from financial_collector import FinancialDataCollector

collector = FinancialDataCollector()
data = collector.collect_all_data()
print(collector.format_bloomberg_style(data))
```