"""
Exemplo 3: Sistema completo com alertas e monitoramento
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import json
from datetime import datetime
from financial_collector import FinancialDataCollector

def exemplo_coleta_simples():
    """Exemplo de coleta simples de dados"""
    
    print("📊 Exemplo: Coleta Completa de Dados")
    print("=" * 50)
    
    # Inicializa o coletor
    collector = FinancialDataCollector()
    
    # Coleta todos os dados
    dados = collector.collect_all_data()
    
    # Formata no estilo Bloomberg
    formatado = collector.format_bloomberg_style(dados)
    print(formatado)
    
    # Salva em arquivo
    arquivo = collector.save_to_file(dados)
    print(f"\n💾 Dados salvos em: {arquivo}")

def exemplo_alertas():
    """Exemplo de sistema de alertas"""
    
    print("🚨 Exemplo: Sistema de Alertas")
    print("=" * 50)
    
    collector = FinancialDataCollector()
    
    # Coleta dados
    dados = collector.collect_all_data()
    
    # Gera resumo com alertas
    resumo = collector.get_summary(dados)
    
    print(f"⏰ Timestamp: {resumo['timestamp']}")
    print(f"🏛️ Mercado: {'🟢 ABERTO' if resumo['market_open'] else '🔴 FECHADO'}")
    print()
    
    # Mostra top moedas por variação
    print("💱 Top Câmbio por Variação:")
    for par, dados_moeda in list(resumo['top_currencies'].items())[:3]:
        simbolo = "📈" if dados_moeda['change_percent'] >= 0 else "📉"
        print(f"   {par}: {simbolo} {dados_moeda['change_percent']:+.2f}%")
    
    print("\n📈 Top Índices por Variação:")
    for indice, dados_indice in list(resumo['top_indices'].items())[:3]:
        simbolo = "📈" if dados_indice['change_percent'] >= 0 else "📉"
        print(f"   {indice}: {simbolo} {dados_indice['change_percent']:+.2f}%")
    
    # Mostra alertas
    if resumo['alerts']:
        print(f"\n🔔 Alertas ({len(resumo['alerts'])}):")
        for alerta in resumo['alerts']:
            print(f"   {alerta}")
    else:
        print("\n✅ Nenhum alerta no momento")

def exemplo_monitoramento_continuo():
    """Exemplo de monitoramento contínuo por 5 minutos"""
    
    print("🔄 Exemplo: Monitoramento Contínuo")
    print("=" * 50)
    print("⏱️ Executando por 5 minutos...")
    print("💡 Pressione Ctrl+C para parar")
    print()
    
    collector = FinancialDataCollector()
    collector.update_interval = 30  # 30 segundos
    
    try:
        collector.run_continuous(duration_minutes=5)
    except KeyboardInterrupt:
        print("\n⏹️ Monitoramento interrompido")

def exemplo_dados_especificos():
    """Exemplo focando em dados específicos"""
    
    print("🎯 Exemplo: Dados Específicos")
    print("=" * 50)
    
    collector = FinancialDataCollector()
    
    # Coleta dados completos
    dados = collector.collect_all_data()
    
    # Foca no USD/BRL e Ibovespa
    print("💰 Foco: USD/BRL e Ibovespa")
    print("-" * 30)
    
    # USD/BRL
    if 'USD-BRL' in dados.get('cambio', {}):
        usd_brl = dados['cambio']['USD-BRL']
        trend = "📈" if usd_brl['change'] >= 0 else "📉"
        print(f"USD/BRL: R$ {usd_brl['rate']:.4f} {trend} {usd_brl['change_percent']:+.2f}%")
        print(f"Fonte: {usd_brl['source']}")
    
    # Ibovespa
    if 'IBOV' in dados.get('bolsa', {}):
        ibov = dados['bolsa']['IBOV']
        trend = "📈" if ibov['change'] >= 0 else "📉"
        print(f"IBOVESPA: {ibov['price']:,.2f} {trend} {ibov['change_percent']:+.2f}%")
        print(f"Volume: {ibov['volume']:,}")
    
    print()

def exemplo_export_csv():
    """Exemplo de exportação para CSV"""
    
    print("📁 Exemplo: Exportação CSV")
    print("=" * 50)
    
    import pandas as pd
    
    collector = FinancialDataCollector()
    dados = collector.collect_all_data()
    
    # Converte câmbio para DataFrame
    cambio_df = pd.DataFrame.from_dict(dados['cambio'], orient='index')
    cambio_df.index.name = 'Par'
    
    # Converte bolsa para DataFrame
    bolsa_df = pd.DataFrame.from_dict(dados['bolsa'], orient='index')
    bolsa_df.index.name = 'Indice'
    
    # Salva CSVs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    cambio_file = f"cambio_{timestamp}.csv"
    bolsa_file = f"bolsa_{timestamp}.csv"
    
    cambio_df.to_csv(cambio_file)
    bolsa_df.to_csv(bolsa_file)
    
    print(f"✅ Câmbio exportado: {cambio_file}")
    print(f"✅ Bolsa exportada: {bolsa_file}")
    
    # Mostra preview
    print(f"\n📊 Preview Câmbio:")
    print(cambio_df[['rate', 'change_percent', 'source']].head())
    
    print(f"\n📈 Preview Bolsa:")
    print(bolsa_df[['price', 'change_percent', 'volume']].head())

def menu_exemplos():
    """Menu interativo dos exemplos"""
    
    exemplos = {
        "1": ("Coleta simples", exemplo_coleta_simples),
        "2": ("Sistema de alertas", exemplo_alertas),
        "3": ("Monitoramento contínuo", exemplo_monitoramento_continuo),
        "4": ("Dados específicos", exemplo_dados_especificos),
        "5": ("Exportação CSV", exemplo_export_csv),
    }
    
    print("🎮 Menu de Exemplos")
    print("=" * 30)
    
    for key, (name, _) in exemplos.items():
        print(f"{key}. {name}")
    
    print("0. Sair")
    print("=" * 30)
    
    while True:
        try:
            escolha = input("\nEscolha um exemplo (0-5): ").strip()
            
            if escolha == "0":
                print("👋 Até logo!")
                break
            elif escolha in exemplos:
                nome, funcao = exemplos[escolha]
                print(f"\n🚀 Executando: {nome}")
                print("="*60)
                funcao()
                print("="*60)
                print("✅ Exemplo concluído!")
                
                input("\n⏎ Pressione Enter para continuar...")
            else:
                print("❌ Opção inválida!")
                
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    menu_exemplos()