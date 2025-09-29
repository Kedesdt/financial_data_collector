"""
Sistema principal para coleta de informações financeiras em tempo real
Integra dados de câmbio e bolsa de valores
"""

import json
import time
from datetime import datetime
from typing import Dict, Optional
import os
from dotenv import load_dotenv

from cambio_api import CambioAPI
from bolsa_api import BolsaAPI


class FinancialDataCollector:
    """Classe principal para coleta de dados financeiros"""
    
    def __init__(self, config_file: Optional[str] = None):
        # Carrega variáveis de ambiente
        load_dotenv()
        
        self.cambio_api = CambioAPI()
        self.bolsa_api = BolsaAPI()
        
        # Configurações
        self.update_interval = int(os.getenv('UPDATE_INTERVAL', 60))  # segundos
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        # APIs keys opcionais
        self.fixer_api_key = os.getenv('FINHUB_API_KEY')
        
    def collect_all_data(self) -> Dict:
        """
        Coleta todos os dados financeiros disponíveis
        """
        if self.debug:
            print(f"🔄 Coletando dados em {datetime.now().strftime('%H:%M:%S')}")
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'cambio': {},
            'bolsa': {},
            'market_status': {}
        }
        
        try:
            # Dados de câmbio
            cambio_data = self.cambio_api.get_all_rates(self.fixer_api_key)
            data['cambio'] = cambio_data
            
            # Dados da bolsa
            bolsa_data = self.bolsa_api.get_all_indices()
            data['bolsa'] = bolsa_data
            
            # Status do mercado
            market_status = self.bolsa_api.get_market_status()
            data['market_status'] = market_status
            
            if self.debug:
                print(f"✅ Coletados {len(cambio_data)} pares de moedas e {len(bolsa_data)} índices")
                
        except Exception as e:
            print(f"❌ Erro na coleta: {e}")
            
        return data
    
    def format_bloomberg_style(self, data: Dict) -> str:
        """
        Formata os dados no estilo Bloomberg (similar à tela mostrada)
        """
        output = []
        output.append("=" * 80)
        output.append("📺 INFORMAÇÕES FINANCEIRAS EM TEMPO REAL")
        output.append("=" * 80)
        
        # Timestamp
        timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
        output.append(f"⏰ Atualizado em: {timestamp.strftime('%d/%m/%Y %H:%M:%S')}")
        output.append("")
        
        # Status do mercado
        if 'market_status' in data and data['market_status']:
            status = data['market_status']['B3']
            status_icon = "🟢" if status['is_open'] else "🔴"
            output.append(f"🏛️  B3: {status_icon} {'ABERTO' if status['is_open'] else 'FECHADO'}")
            output.append("")
        
        # Dados de Câmbio (estilo Bloomberg)
        output.append("💱 CÂMBIO")
        output.append("-" * 40)
        
        if 'cambio' in data:
            for pair, info in data['cambio'].items():
                trend = "📈" if info['change'] >= 0 else "📉"
                output.append(f"{pair:12} {info['rate']:8.4f} {trend} {info['change_percent']:+6.2f}%")
                output.append(f"             Fonte: {info['source']}")
        
        output.append("")
        
        # Dados da Bolsa
        output.append("📈 ÍNDICES")
        output.append("-" * 40)
        
        if 'bolsa' in data:
            for index, info in data['bolsa'].items():
                trend = "📈" if info['change'] >= 0 else "📉"
                output.append(f"{index:12} {info['price']:10,.2f} {trend} {info['change_percent']:+6.2f}%")
                output.append(f"             Variação: {info['change']:+,.2f} | Volume: {info['volume']:,}")
        
        output.append("")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    def save_to_file(self, data: Dict, filename: Optional[str] = None) -> str:
        """
        Salva dados em arquivo JSON
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"financial_data_{timestamp}.json"
        
        filepath = os.path.join(os.getcwd(), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def get_summary(self, data: Dict) -> Dict:
        """
        Cria um resumo executivo dos dados
        """
        summary = {
            'timestamp': data['timestamp'],
            'market_open': False,
            'top_currencies': {},
            'top_indices': {},
            'alerts': []
        }
        
        # Status do mercado
        if 'market_status' in data:
            summary['market_open'] = data['market_status'].get('B3', {}).get('is_open', False)
        
        # Top moedas por variação
        if 'cambio' in data:
            cambio_sorted = sorted(
                data['cambio'].items(), 
                key=lambda x: abs(x[1]['change_percent']), 
                reverse=True
            )
            summary['top_currencies'] = dict(cambio_sorted[:5])
        
        # Top índices por variação
        if 'bolsa' in data:
            bolsa_sorted = sorted(
                data['bolsa'].items(), 
                key=lambda x: abs(x[1]['change_percent']), 
                reverse=True
            )
            summary['top_indices'] = dict(bolsa_sorted[:5])
        
        # Alertas para variações significativas
        alerts = []
        
        # Alerta para câmbio com variação > 2%
        for pair, info in data.get('cambio', {}).items():
            if abs(info['change_percent']) > 2:
                alerts.append(f"🚨 {pair}: {info['change_percent']:+.2f}%")
        
        # Alerta para bolsa com variação > 3%
        for index, info in data.get('bolsa', {}).items():
            if abs(info['change_percent']) > 3:
                alerts.append(f"🚨 {index}: {info['change_percent']:+.2f}%")
        
        summary['alerts'] = alerts
        
        return summary
    
    def run_continuous(self, duration_minutes: Optional[int] = None):
        """
        Executa coleta contínua de dados
        """
        print("🚀 Iniciando coleta contínua de dados financeiros...")
        print(f"📊 Intervalo de atualização: {self.update_interval} segundos")
        
        if duration_minutes:
            print(f"⏱️  Duração: {duration_minutes} minutos")
        
        print("=" * 60)
        
        start_time = time.time()
        
        try:
            while True:
                # Coleta dados
                data = self.collect_all_data()
                
                # Exibe no formato Bloomberg
                formatted_output = self.format_bloomberg_style(data)
                
                # Limpa tela (Windows)
                os.system('cls' if os.name == 'nt' else 'clear')
                print(formatted_output)
                
                # Verifica alertas
                summary = self.get_summary(data)
                if summary['alerts']:
                    print("\n🔔 ALERTAS:")
                    for alert in summary['alerts']:
                        print(f"   {alert}")
                
                # Salva dados (opcional)
                if self.debug:
                    self.save_to_file(data, "latest_data.json")
                
                # Verifica se deve parar
                if duration_minutes:
                    elapsed_minutes = (time.time() - start_time) / 60
                    if elapsed_minutes >= duration_minutes:
                        print(f"\n✅ Coleta finalizada após {duration_minutes} minutos")
                        break
                
                # Aguarda próxima atualização
                time.sleep(self.update_interval)
                
        except KeyboardInterrupt:
            print("\n⏹️  Coleta interrompida pelo usuário")
        except Exception as e:
            print(f"\n❌ Erro durante execução contínua: {e}")


def main():
    """Função principal"""
    collector = FinancialDataCollector()
    
    print("💼 Sistema de Coleta de Dados Financeiros")
    print("=" * 50)
    print("1. Coleta única")
    print("2. Coleta contínua")
    print("3. Coleta por tempo determinado")
    print("=" * 50)
    
    choice = input("Escolha uma opção (1-3): ").strip()
    
    if choice == "1":
        # Coleta única
        data = collector.collect_all_data()
        formatted = collector.format_bloomberg_style(data)
        print("\n" + formatted)
        
        # Salva arquivo
        filepath = collector.save_to_file(data)
        print(f"\n💾 Dados salvos em: {filepath}")
        
    elif choice == "2":
        # Coleta contínua
        collector.run_continuous()
        
    elif choice == "3":
        # Coleta por tempo determinado
        try:
            minutes = int(input("Quantos minutos? "))
            collector.run_continuous(duration_minutes=minutes)
        except ValueError:
            print("❌ Valor inválido!")
            
    else:
        print("❌ Opção inválida!")


if __name__ == "__main__":
    main()