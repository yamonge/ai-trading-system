import yfinance as yf
from typing import Any, Dict


class StockAnalyzer:
    """
    개선된 주식 분석기 - Local History가 이 변경사항을 자동 추적합니다!
    """
    def __init__(self):
        self.data = {}
        self.cache = {}  # 새로운 캐시 기능 추가

    def get_price(self, symbol: str) -> Dict[str, Any]:
        # 캐시에서 먼저 확인
        if symbol in self.cache:
            print(f"🔄 캐시에서 {symbol} 데이터 반환")
            return self.cache[symbol]
            
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            result = {
                "symbol": symbol,
                "price": info.get("currentPrice", 0),
                "name": info.get("longName", "Unknown"),
                "cached_at": "just_now"
            }
            
            # 캐시에 저장
            self.cache[symbol] = result
            return result
            
        except Exception as e:
            return {"error": f"Failed to fetch data: {str(e)}"}


def main():
    analyzer = StockAnalyzer()
    result = analyzer.get_price("AAPL")
    print(result)
