"""
Exemplo 2: Coleta de dados da bolsa de valores
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bolsa_api import BolsaAPI

def exemplo_indices_principais():
    """Exemplo dos principais índices"""
    
    print("📈 Exemplo: Índices da Bolsa")
    print("=" * 40)
    
    bolsa = BolsaAPI()
    
    # Pega dados de todos os índices
    indices = bolsa.get_all_indices()
    
    # Separa por categoria
    brasileiros = {k: v for k, v in indices.items() if k in ['IBOV', 'IBRX100', 'SMLL']}
    internacionais = {k: v for k, v in indices.items() if k not in brasileiros}
    
    # Exibe índices brasileiros
    print("🇧🇷 Índices Brasileiros:")
    for nome, dados in brasileiros.items():
        tendencia = "📈" if dados['change'] >= 0 else "📉"
        print(f"   {nome}: {dados['price']:,.2f} {tendencia} {dados['change_percent']:+.2f}%")
    
    print("\n🌍 Índices Internacionais:")
    for nome, dados in internacionais.items():
        tendencia = "📈" if dados['change'] >= 0 else "📉"
        print(f"   {nome}: {dados['price']:,.2f} {tendencia} {dados['change_percent']:+.2f}%")

def exemplo_acoes_especificas():
    """Exemplo de ações específicas"""
    
    print("\n🏢 Exemplo: Ações Específicas")
    print("=" * 40)
    
    bolsa = BolsaAPI()
    
    # Ações populares da B3
    acoes = ['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3', 'WEGE3']
    
    dados_acoes = bolsa.get_stock_data(acoes)
    
    for simbolo, dados in dados_acoes.items():
        tendencia = "📈" if dados['change'] >= 0 else "📉"
        print(f"{simbolo}: R$ {dados['price']:.2f} {tendencia} {dados['change_percent']:+.2f}%")
        print(f"   {dados['company_name']}")
        print(f"   Volume: {dados['volume']:,}")
        print()

def exemplo_status_mercado():
    """Exemplo do status do mercado"""
    
    print("🏛️ Exemplo: Status do Mercado")
    print("=" * 40)
    
    bolsa = BolsaAPI()
    
    status = bolsa.get_market_status()
    
    if status and 'B3' in status:
        b3_info = status['B3']
        status_icon = "🟢" if b3_info['is_open'] else "🔴"
        status_text = "ABERTO" if b3_info['is_open'] else "FECHADO"
        
        print(f"B3 (Bolsa Brasileira): {status_icon} {status_text}")
        
        if b3_info['is_open']:
            print(f"   Fechamento: {b3_info['next_close']}")
        else:
            print(f"   Próxima abertura: {b3_info['next_open']}")
    else:
        print("❌ Não foi possível verificar o status do mercado")

def exemplo_ranking_performance():
    """Exemplo de ranking por performance"""
    
    print("\n🏆 Exemplo: Ranking por Performance")
    print("=" * 40)
    
    bolsa = BolsaAPI()
    
    # Pega dados dos índices
    indices = bolsa.get_all_indices()
    
    # Ordena por performance (variação percentual)
    ranking = sorted(
        indices.items(), 
        key=lambda x: x[1]['change_percent'], 
        reverse=True
    )
    
    print("🥇 Maiores altas:")
    for i, (nome, dados) in enumerate(ranking[:3]):
        medal = ["🥇", "🥈", "🥉"][i]
        print(f"   {medal} {nome}: {dados['change_percent']:+.2f}%")
    
    print("\n📉 Maiores baixas:")
    for i, (nome, dados) in enumerate(ranking[-3:]):
        print(f"   📉 {nome}: {dados['change_percent']:+.2f}%")

if __name__ == "__main__":
    # Executa todos os exemplos
    exemplo_indices_principais()
    print("\n" + "="*60)
    
    exemplo_acoes_especificas()
    print("="*60)
    
    exemplo_status_mercado()
    print("="*60)
    
    exemplo_ranking_performance()