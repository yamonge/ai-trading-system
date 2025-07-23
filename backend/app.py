"""
AI Trading System - FastAPI Backend
자비스처럼 똑똑한 AI 어시스턴트가 만든 백엔드 API

TODO: PostgreSQL 데이터베이스 연결 추가
TODO: 사용자 인증 시스템 구현  
TODO: WebSocket 실시간 데이터 스트리밍
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List
import yfinance as yf
import asyncio
from datetime import datetime
import uvicorn

# 보안 설정
security = HTTPBearer()

# FastAPI 앱 생성
app = FastAPI(
    title="AI Trading System API",
    description="자비스처럼 똑똑한 AI가 만든 주식 트레이딩 API",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# CORS 설정 (프론트엔드 연결용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용, 실제 배포시 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 모델들
class StockPrice(BaseModel):
    symbol: str
    company_name: str
    current_price: float
    open_price: float
    high_price: float
    low_price: float
    volume: int
    change: float
    change_percent: float
    timestamp: str

class StockRequest(BaseModel):
    symbol: str

class MultiStockRequest(BaseModel):
    symbols: List[str]

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# 메모리 기반 사용자 저장소 (개발용)
fake_users_db = {}

# 루트 엔드포인트
@app.get("/")
async def root():
    """
    API 상태 확인
    자비스: "시스템 온라인 상태입니다, Sir."
    """
    return {
        "message": "🤖 AI Trading System API - Online",
        "status": "operational",
        "version": "1.0.0",
        "jarvis_mode": "activated",
        "timestamp": datetime.now().isoformat()
    }

# 헬스체크
@app.get("/health")
async def health_check():
    """시스템 헬스체크"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "jarvis_response": "All systems operational, Sir."
    }

# 단일 주식 가격 조회
@app.get("/api/stocks/{symbol}", response_model=StockPrice)
async def get_stock_price(symbol: str):
    """
    특정 주식의 실시간 가격 정보 조회
    자비스처럼 빠르고 정확한 데이터 제공
    """
    try:
        symbol = symbol.upper()
        stock = yf.Ticker(symbol)
        info = stock.info
        hist = stock.history(period="1d")
        
        if hist.empty:
            raise HTTPException(
                status_code=404,
                detail=f"Stock symbol '{symbol}' not found. Jarvis suggests checking the symbol."
            )
        
        current_price = hist['Close'].iloc[-1]
        open_price = hist['Open'].iloc[-1]
        high_price = hist['High'].iloc[-1]
        low_price = hist['Low'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        
        stock_data = StockPrice(
            symbol=symbol,
            company_name=info.get('longName', 'N/A'),
            current_price=round(current_price, 2),
            open_price=round(open_price, 2),
            high_price=round(high_price, 2),
            low_price=round(low_price, 2),
            volume=int(volume),
            change=round(current_price - open_price, 2),
            change_percent=round(((current_price - open_price) / open_price) * 100, 2),
            timestamp=datetime.now().isoformat()
        )
        
        return stock_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching stock data: {str(e)}. Jarvis is investigating."
        )

# 다중 주식 가격 조회
@app.post("/api/stocks/batch", response_model=List[StockPrice])
async def get_multiple_stocks(request: MultiStockRequest):
    """
    여러 주식의 가격을 한번에 조회
    자비스의 멀티태스킹 능력처럼 동시 처리
    """
    results = []
    
    async def fetch_stock(symbol: str):
        try:
            stock_data = await get_stock_price(symbol)
            return stock_data
        except HTTPException:
            return None
    
    # 비동기로 동시 처리 (자비스의 병렬 처리)
    tasks = [fetch_stock(symbol) for symbol in request.symbols]
    stock_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for result in stock_results:
        if result and not isinstance(result, Exception):
            results.append(result)
    
    return results

# 인기 주식 조회
@app.get("/api/stocks/popular", response_model=List[StockPrice])
async def get_popular_stocks():
    """
    인기 주식들의 가격 정보
    자비스가 추천하는 주요 종목들
    """
    popular_symbols = ['AAPL', 'TSLA', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'META']
    request = MultiStockRequest(symbols=popular_symbols)
    return await get_multiple_stocks(request)

# 주식 검색
@app.get("/api/stocks/search/{query}")
async def search_stocks(query: str):
    """
    주식 심볼 또는 회사명으로 검색
    자비스의 스마트 검색 기능
    """
    # 간단한 검색 구현 (실제로는 더 복잡한 검색 로직 필요)
    common_stocks = {
        'apple': 'AAPL',
        'tesla': 'TSLA',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'amazon': 'AMZN',
        'nvidia': 'NVDA',
        'meta': 'META',
        'netflix': 'NFLX'
    }
    
    query_lower = query.lower()
    suggestions = []
    
    for name, symbol in common_stocks.items():
        if query_lower in name or query_lower == symbol.lower():
            suggestions.append({
                "symbol": symbol,
                "name": name.title(),
                "confidence": 1.0 if query_lower == symbol.lower() else 0.8
            })
    
    return {
        "query": query,
        "suggestions": suggestions,
        "jarvis_note": f"Found {len(suggestions)} matches for '{query}', Sir."
    }

# 사용자 등록 (미래 기능)
@app.post("/api/auth/register")
async def register_user(user: UserCreate):
    """
    사용자 등록
    자비스가 사용자 정보를 안전하게 관리
    """
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=400,
            detail="Username already exists. Jarvis suggests choosing a different one."
        )
    
    # 실제로는 비밀번호 해싱 필요
    fake_users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "created_at": datetime.now().isoformat()
    }
    
    return {
        "message": f"User {user.username} registered successfully",
        "jarvis_response": f"Welcome aboard, {user.username}. Your account is now active."
    }

# API 정보
@app.get("/api/info")
async def api_info():
    """
    API 정보 및 사용 가능한 엔드포인트
    자비스의 매뉴얼
    """
    return {
        "api_name": "AI Trading System",
        "version": "1.0.0",
        "jarvis_mode": "Fully Operational",
        "endpoints": {
            "stocks": {
                "single": "/api/stocks/{symbol}",
                "batch": "/api/stocks/batch",
                "popular": "/api/stocks/popular",
                "search": "/api/stocks/search/{query}"
            },
            "auth": {
                "register": "/api/auth/register"
            },
            "system": {
                "health": "/health",
                "info": "/api/info"
            }
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "jarvis_capabilities": [
            "Real-time stock data retrieval",
            "Multi-stock parallel processing",
            "Smart search functionality",
            "Auto-documentation",
            "Error handling with style"
        ]
    }

if __name__ == "__main__":
    print("🤖 자비스 모드 활성화: AI Trading System Backend 시작")
    print("📊 실시간 주식 데이터 API 서버 준비 완료")
    print("🔗 API 문서: http://localhost:8000/docs")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 개발 모드
        log_level="info"
    )
