"""
Módulo para capturar dados da bolsa de valores em tempo real
Inclui Ibovespa, IBX e índices globais
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional, List
import yfinance as yf


class BolsaAPI:
    """Classe para capturar dados da bolsa de múltiplas fontes"""
    
    def __init__(self):
        # Símbolos dos principais índices
        self.indices = {
            'IBOV': '^BVSP',      # Ibovespa
            'IBX': 'IBX.SA',      # IBX
            'IBRX': '^BVSP',      # IBRX 100 (usando Ibovespa como proxy)
            'SP500': '^GSPC',     # S&P 500
            'NASDAQ': '^IXIC',    # NASDAQ
            'DOW': '^DJI',        # Dow Jones
            'DAX': '^GDAXI',      # DAX (Alemanha)
            'FTSE': '^FTSE',      # FTSE 100 (Reino Unido)
            'NIKKEI': '^N225',    # Nikkei 225 (Japão)
            'HANG_SENG': '^HSI'   # Hang Seng (Hong Kong)
        }
    
    def get_index_data_yahoo(self, symbols: List[str]) -> Dict:
        """
        Pega dados dos índices usando Yahoo Finance
        """
        try:
            data = {}
            
            for name, symbol in symbols.items():
                ticker = yf.Ticker(symbol)
                
                # Pega dados históricos do dia
                hist = ticker.history(period="1d", interval="5m")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    open_price = hist['Open'].iloc[0]
                    high_price = hist['High'].max()
                    low_price = hist['Low'].min()
                    volume = hist['Volume'].sum()
                    
                    change = current_price - open_price
                    change_percent = (change / open_price) * 100 if open_price != 0 else 0
                    
                    data[name] = {
                        'price': round(current_price, 2),
                        'open': round(open_price, 2),
                        'high': round(high_price, 2),
                        'low': round(low_price, 2),
                        'change': round(change, 2),
                        'change_percent': round(change_percent, 2),
                        'volume': int(volume) if volume > 0 else 0,
                        'timestamp': datetime.now().isoformat(),
                        'source': 'Yahoo Finance',
                        'symbol': symbol
                    }
            
            return data
        except Exception as e:
            print(f"Erro ao buscar dados do Yahoo Finance: {e}")
            return {}
    
    def get_ibovespa_b3(self) -> Dict:
        """
        Pega dados do Ibovespa direto da B3 (fonte oficial)
        Nota: Esta é uma implementação simplificada
        """
        try:
            # A B3 não tem uma API pública simples, então usamos Yahoo como fonte confiável
            # Mas podemos implementar web scraping se necessário
            return self.get_index_data_yahoo({'IBOV': '^BVSP'})
        except Exception as e:
            print(f"Erro ao buscar dados da B3: {e}")
            return {}
    
    def get_global_indices(self) -> Dict:
        """
        Pega dados dos principais índices globais
        """
        global_indices = {
            'SP500': '^GSPC',
            'NASDAQ': '^IXIC',
            'DOW': '^DJI',
            'DAX': '^GDAXI',
            'FTSE': '^FTSE',
            'NIKKEI': '^N225',
            'HANG_SENG': '^HSI'
        }
        
        return self.get_index_data_yahoo(global_indices)
    
    def get_brazilian_indices(self) -> Dict:
        """
        Pega dados dos índices brasileiros
        """
        brazilian_indices = {
            'IBOV': '^BVSP',
            'IBRX100': '^BVSP',  # Proxy - idealmente seria um símbolo específico
            'SMLL': '^BVSP'      # Proxy para Small Cap
        }
        
        return self.get_index_data_yahoo(brazilian_indices)
    
    def get_stock_data(self, symbols: List[str]) -> Dict:
        """
        Pega dados de ações específicas
        """
        try:
            data = {}
            
            for symbol in symbols:
                # Adiciona .SA para ações brasileiras se não tiver sufixo
                if '.' not in symbol and len(symbol) <= 6:
                    ticker_symbol = f"{symbol}.SA"
                else:
                    ticker_symbol = symbol
                
                ticker = yf.Ticker(ticker_symbol)
                info = ticker.info
                hist = ticker.history(period="1d", interval="1m")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    open_price = hist['Open'].iloc[0]
                    change = current_price - open_price
                    change_percent = (change / open_price) * 100 if open_price != 0 else 0
                    
                    data[symbol] = {
                        'price': round(current_price, 2),
                        'open': round(open_price, 2),
                        'high': round(hist['High'].max(), 2),
                        'low': round(hist['Low'].min(), 2),
                        'change': round(change, 2),
                        'change_percent': round(change_percent, 2),
                        'volume': int(hist['Volume'].sum()),
                        'market_cap': info.get('marketCap', 'N/A'),
                        'company_name': info.get('longName', symbol),
                        'timestamp': datetime.now().isoformat(),
                        'source': 'Yahoo Finance',
                        'symbol': ticker_symbol
                    }
            
            return data
        except Exception as e:
            print(f"Erro ao buscar dados de ações: {e}")
            return {}
    
    def get_all_indices(self) -> Dict:
        """
        Consolida dados de todos os índices
        """
        all_data = {}
        
        # Índices brasileiros
        brazilian_data = self.get_brazilian_indices()
        all_data.update(brazilian_data)
        
        # Índices globais
        global_data = self.get_global_indices()
        all_data.update(global_data)
        
        return all_data
    
    def get_market_status(self) -> Dict:
        """
        Verifica status dos mercados (aberto/fechado)
        """
        try:
            # Verifica horário de funcionamento da B3 (9h às 18h, horário de Brasília)
            now = datetime.now()
            
            # Simplificado - em produção, considerar feriados e fusos horários
            is_weekday = now.weekday() < 5  # Segunda a sexta
            current_hour = now.hour
            
            b3_open = is_weekday and 9 <= current_hour < 18
            
            return {
                'B3': {
                    'is_open': b3_open,
                    'next_open': '09:00' if not b3_open else 'Aberto',
                    'next_close': '18:00' if b3_open else 'Fechado'
                },
                'timestamp': now.isoformat()
            }
        except Exception as e:
            print(f"Erro ao verificar status do mercado: {e}")
            return {}


def main():
    """Exemplo de uso"""
    bolsa = BolsaAPI()
    
    print("📈 Dados da Bolsa em Tempo Real")
    print("=" * 50)
    
    # Status do mercado
    status = bolsa.get_market_status()
    if status:
        b3_status = "🟢 ABERTO" if status['B3']['is_open'] else "🔴 FECHADO"
        print(f"Status B3: {b3_status}")
        print()
    
    # Índices principais
    indices = bolsa.get_all_indices()
    
    print("📊 Índices Principais:")
    for name, data in indices.items():
        trend = "📈" if data['change'] >= 0 else "📉"
        print(f"{name}: {data['price']:,.2f} {trend} {data['change_percent']:+.2f}%")
        print(f"   Variação: {data['change']:+,.2f} pontos")
        print(f"   Volume: {data['volume']:,}")
        print(f"   Fonte: {data['source']}")
        print()
    
    # Exemplo de ações específicas
    print("🏢 Ações em Destaque:")
    stocks = bolsa.get_stock_data(['PETR4', 'VALE3', 'ITUB4', 'BBDC4'])
    
    for symbol, data in stocks.items():
        trend = "📈" if data['change'] >= 0 else "📉"
        print(f"{symbol}: R$ {data['price']:.2f} {trend} {data['change_percent']:+.2f}%")
        print(f"   {data['company_name']}")
        print(f"   Volume: {data['volume']:,}")
        print()


if __name__ == "__main__":
    main()