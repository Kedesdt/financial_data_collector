"""
Módulo para capturar cotações de câmbio em tempo real
Suporta múltiplas fontes de dados confiáveis
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional, List
import yfinance as yf


class CambioAPI:
    """Classe para capturar dados de câmbio de múltiplas fontes"""
    
    def __init__(self):
        self.base_currency = 'USD'
        
    def get_exchange_rates_yahoo(self, currencies: List[str]) -> Dict:
        """
        Pega cotações usando Yahoo Finance (gratuito e confiável)
        """
        try:
            rates = {}
            for currency in currencies:
                if currency != 'USD':
                    # Para moedas vs USD
                    symbol = f"USD{currency}=X" if currency in ['BRL', 'JPY', 'CNY', 'INR', 'KRW'] else f"{currency}USD=X"
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="1d", interval="1m")
                    
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        prev_close = hist['Close'].iloc[0] if len(hist) > 1 else current_price
                        change = current_price - prev_close
                        change_percent = (change / prev_close) * 100 if prev_close != 0 else 0
                        
                        rates[f'USD-{currency}'] = {
                            'rate': round(current_price, 4),
                            'change': round(change, 4),
                            'change_percent': round(change_percent, 2),
                            'timestamp': datetime.now().isoformat(),
                            'source': 'Yahoo Finance'
                        }
                        
            return rates
        except Exception as e:
            print(f"Erro ao buscar dados do Yahoo Finance: {e}")
            return {}
    
    def get_exchange_rates_fixer(self, api_key: Optional[str] = None) -> Dict:
        """
        Pega cotações usando Fixer.io API (requer chave, mas tem plano gratuito)
        """
        if not api_key:
            return {}
            
        try:
            url = f"http://data.fixer.io/api/latest?access_key={api_key}&base=USD&symbols=BRL,EUR,JPY,CNY,INR,KRW"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('success'):
                rates = {}
                for currency, rate in data['rates'].items():
                    rates[f'USD-{currency}'] = {
                        'rate': rate,
                        'change': 0,  # Fixer não fornece mudança
                        'change_percent': 0,
                        'timestamp': datetime.now().isoformat(),
                        'source': 'Fixer.io'
                    }
                return rates
        except Exception as e:
            print(f"Erro ao buscar dados do Fixer: {e}")
            return {}
    
    def get_exchange_rates_exchangerate(self) -> Dict:
        """
        Pega cotações usando ExchangeRate-API (gratuito, sem chave necessária)
        """
        try:
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            rates = {}
            currencies = ['BRL', 'EUR', 'JPY', 'CNY', 'INR', 'KRW']
            
            for currency in currencies:
                if currency in data['rates']:
                    rates[f'USD-{currency}'] = {
                        'rate': data['rates'][currency],
                        'change': 0,  # API não fornece mudança
                        'change_percent': 0,
                        'timestamp': datetime.now().isoformat(),
                        'source': 'ExchangeRate-API'
                    }
                    
            return rates
        except Exception as e:
            print(f"Erro ao buscar dados do ExchangeRate-API: {e}")
            return {}
    
    def get_usd_brl_bcb(self) -> Dict:
        """
        Pega cotação USD/BRL direto do Banco Central do Brasil (fonte oficial)
        """
        try:
            # API do BCB para dólar comercial
            url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados/ultimos/1?formato=json"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data:
                latest = data[0]
                return {
                    'USD-BRL': {
                        'rate': float(latest['valor']),
                        'change': 0,
                        'change_percent': 0,
                        'timestamp': datetime.now().isoformat(),
                        'source': 'Banco Central do Brasil',
                        'date': latest['data']
                    }
                }
        except Exception as e:
            print(f"Erro ao buscar dados do BCB: {e}")
            return {}
    
    def get_all_rates(self, fixer_api_key: Optional[str] = None) -> Dict:
        """
        Consolida cotações de todas as fontes disponíveis
        """
        all_rates = {}
        
        # Yahoo Finance (principal fonte - gratuita e confiável)
        currencies = ['BRL', 'EUR', 'JPY', 'CNY', 'INR', 'KRW']
        yahoo_rates = self.get_exchange_rates_yahoo(currencies)
        all_rates.update(yahoo_rates)
        
        # BCB para USD/BRL (fonte oficial brasileira)
        bcb_rates = self.get_usd_brl_bcb()
        if bcb_rates:
            # Substitui o Yahoo com dados oficiais do BCB
            all_rates.update(bcb_rates)
        
        # ExchangeRate-API como backup
        if not all_rates:
            exchange_rates = self.get_exchange_rates_exchangerate()
            all_rates.update(exchange_rates)
        
        # Fixer como fonte adicional se houver chave
        if fixer_api_key:
            fixer_rates = self.get_exchange_rates_fixer(fixer_api_key)
            # Adiciona apenas se não temos dados para essas moedas
            for key, value in fixer_rates.items():
                if key not in all_rates:
                    all_rates[key] = value
        
        return all_rates


def main():
    """Exemplo de uso"""
    cambio = CambioAPI()
    
    print("🏦 Cotações de Câmbio em Tempo Real")
    print("=" * 50)
    
    rates = cambio.get_all_rates()
    
    for pair, data in rates.items():
        change_symbol = "📈" if data['change'] >= 0 else "📉"
        print(f"{pair}: {data['rate']:.4f} {change_symbol} {data['change_percent']:+.2f}%")
        print(f"   Fonte: {data['source']}")
        print(f"   Atualizado: {data['timestamp'][:19]}")
        print()


if __name__ == "__main__":
    main()