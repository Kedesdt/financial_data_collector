"""
Exemplo 1: Coleta básica de dados de câmbio
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cambio_api import CambioAPI

def exemplo_cambio_basico():
    """Exemplo básico de uso da API de câmbio"""
    
    print("💱 Exemplo: Cotações de Câmbio")
    print("=" * 40)
    
    # Inicializa a API
    cambio = CambioAPI()
    
    # Pega todas as cotações disponíveis
    cotacoes = cambio.get_all_rates()
    
    # Exibe as cotações
    for par, dados in cotacoes.items():
        simbolo = "📈" if dados['change'] >= 0 else "📉"
        print(f"{par}: {dados['rate']:.4f} {simbolo} {dados['change_percent']:+.2f}%")
        print(f"   Fonte: {dados['source']}")
        print(f"   Última atualização: {dados['timestamp'][:19]}")
        print()

def exemplo_usd_brl_oficial():
    """Exemplo usando apenas dados oficiais do Banco Central"""
    
    print("🏦 Exemplo: USD/BRL Oficial (BCB)")
    print("=" * 40)
    
    cambio = CambioAPI()
    
    # Pega cotação oficial do BCB
    usd_brl = cambio.get_usd_brl_bcb()
    
    if 'USD-BRL' in usd_brl:
        dados = usd_brl['USD-BRL']
        print(f"💰 Dólar Americano (USD)")
        print(f"   Cotação: R$ {dados['rate']:.4f}")
        print(f"   Fonte: {dados['source']}")
        print(f"   Data: {dados['date']}")
    else:
        print("❌ Não foi possível obter cotação do BCB")

def exemplo_multiplas_fontes():
    """Exemplo comparando cotações de diferentes fontes"""
    
    print("🔄 Exemplo: Comparação de Fontes")
    print("=" * 40)
    
    cambio = CambioAPI()
    
    # Testa diferentes fontes
    fontes = {
        'Yahoo Finance': cambio.get_exchange_rates_yahoo(['BRL', 'EUR', 'JPY']),
        'ExchangeRate-API': cambio.get_exchange_rates_exchangerate(),
        'BCB (USD/BRL)': cambio.get_usd_brl_bcb()
    }
    
    for nome_fonte, dados in fontes.items():
        print(f"📊 {nome_fonte}:")
        
        if dados:
            for par, info in dados.items():
                print(f"   {par}: {info['rate']:.4f}")
        else:
            print("   ❌ Sem dados disponíveis")
        print()

if __name__ == "__main__":
    # Executa todos os exemplos
    exemplo_cambio_basico()
    print("\n" + "="*60 + "\n")
    
    exemplo_usd_brl_oficial()
    print("\n" + "="*60 + "\n")
    
    exemplo_multiplas_fontes()