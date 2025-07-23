"""
간단한 주식 가격 조회 프로그램
VS Code의 Python 확장프로그램과 함께 작동합니다.
"""

import yfinance as yf
import datetime
from typing import Dict, Any

class StockAnalyzer:
    def __init__(self):
        """주식 분석기 초기화"""
        self.stocks = {}
    
    def get_stock_price(self, symbol: str) -> Dict[str, Any]:
        """
        주식 심볼을 입력받아 현재 가격 정보를 반환합니다.
        
        Args:
            symbol (str): 주식 심볼 (예: 'AAPL', 'TSLA')
        
        Returns:
            Dict[str, Any]: 주식 정보 딕셔너리
        """
        try:
            # yfinance를 사용해 주식 데이터 가져오기
            stock = yf.Ticker(symbol)
            info = stock.info
            hist = stock.history(period="1d")
            
            if hist.empty:
                return {"error": f"주식 심볼 '{symbol}'을 찾을 수 없습니다."}
            
            current_price = hist['Close'].iloc[-1]
            open_price = hist['Open'].iloc[-1]
            high_price = hist['High'].iloc[-1]
            low_price = hist['Low'].iloc[-1]
            volume = hist['Volume'].iloc[-1]
            
            stock_data = {
                "symbol": symbol,
                "company_name": info.get('longName', 'N/A'),
                "current_price": round(current_price, 2),
                "open_price": round(open_price, 2),
                "high_price": round(high_price, 2),
                "low_price": round(low_price, 2),
                "volume": int(volume),
                "change": round(current_price - open_price, 2),
                "change_percent": round(((current_price - open_price) / open_price) * 100, 2),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return stock_data
            
        except Exception as e:
            return {"error": f"데이터를 가져오는 중 오류 발생: {str(e)}"}
    
    def display_stock_info(self, stock_data: Dict[str, Any]) -> None:
        """주식 정보를 보기 좋게 출력합니다."""
        if "error" in stock_data:
            print(f"❌ 오류: {stock_data['error']}")
            return
        
        print("\n" + "="*50)
        print(f"📊 {stock_data['company_name']} ({stock_data['symbol']})")
        print("="*50)
        print(f"💰 현재가: ${stock_data['current_price']}")
        print(f"📈 시가: ${stock_data['open_price']}")
        print(f"⬆️  고가: ${stock_data['high_price']}")
        print(f"⬇️  저가: ${stock_data['low_price']}")
        print(f"📊 거래량: {stock_data['volume']:,}")
        
        change_emoji = "📈" if stock_data['change'] >= 0 else "📉"
        print(f"{change_emoji} 변동: ${stock_data['change']} ({stock_data['change_percent']}%)")
        print(f"⏰ 조회시간: {stock_data['timestamp']}")
        print("="*50)

def main():
    """메인 실행 함수"""
    print("🚀 AI 트레이딩 - 주식 가격 조회 프로그램")
    print("VS Code Python 확장프로그램과 함께 작동합니다!\n")
    
    analyzer = StockAnalyzer()
    
    # 인기 주식들 예시
    popular_stocks = ['AAPL', 'TSLA', 'GOOGL', 'MSFT', 'AMZN']
    
    while True:
        print("\n📋 메뉴:")
        print("1. 주식 가격 조회")
        print("2. 인기 주식 한번에 보기")
        print("3. 종료")
        
        choice = input("\n선택하세요 (1-3): ").strip()
        
        if choice == '1':
            symbol = input("주식 심볼을 입력하세요 (예: AAPL): ").strip().upper()
            if symbol:
                print(f"\n🔍 {symbol} 정보를 가져오는 중...")
                stock_data = analyzer.get_stock_price(symbol)
                analyzer.display_stock_info(stock_data)
            else:
                print("❌ 올바른 주식 심볼을 입력해주세요.")
                
        elif choice == '2':
            print("\n🔍 인기 주식들 정보를 가져오는 중...")
            for symbol in popular_stocks:
                stock_data = analyzer.get_stock_price(symbol)
                analyzer.display_stock_info(stock_data)
                
        elif choice == '3':
            print("\n👋 프로그램을 종료합니다. 감사합니다!")
            break
            
        else:
            print("❌ 올바른 선택지를 입력해주세요.")

if __name__ == "__main__":
    main()
