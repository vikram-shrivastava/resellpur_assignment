from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from schemas import SuggestRequest, SuggestResponse, ModerationRequest, ModerationResponse
import uvicorn

from agent import MarketplaceAssistantSimple

app = FastAPI(title="Marketplace Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

assistant = MarketplaceAssistantSimple()

@app.get("/")
async def root():
    return {
        "message": "Marketplace Assistant API",
        "endpoints": {
            "/negotiate": "POST - Get price suggestions for products",
            "/moderate": "POST - Moderate chat messages"
        }
    }


@app.post("/negotiate", response_model=SuggestResponse)
async def negotiate_price(req: SuggestRequest):

    try:
        query = f""" I want to sell a {req.category}. Here are the details:
            - Model: {req.title}
            - Brand: {req.brand}
            - Condition: {req.condition}
            - Age: {req.age_months} months
            - My asking price: ₹{req.asking_price}
            - Location: {req.location}
        What is a fair price range for this product based on current market conditions?
"""
        
        result = assistant.process_query(query)
        
        if result.get("type") != "price_suggestion":
            raise HTTPException(
                status_code=500,
                detail="Query was not classified as price suggestion"
            )
        
        price_range = result.get("price_range", "Unable to determine")
        reasoning = result.get("reason_price_range", "No reasoning provided")
        
        is_fraud = False
        if price_range != "Unable to determine" and price_range != "Error":
            try:
                if "-" in price_range:
                    low, high = price_range.split("-")
                    low_price = float(low.strip())
                    high_price = float(high.strip())
                    asking = float(req.asking_price)
                    
                    if asking > high_price * 1.5:
                        is_fraud = True
                        reasoning += f" WARNING: Asking price (₹{asking}) is significantly higher than market value."
            except (ValueError, AttributeError):
                pass
        
        return SuggestResponse(
            fair_price_range=price_range,
            reasoning=reasoning,
            is_fraud=is_fraud
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing price suggestion: {str(e)}"
        )


@app.post("/moderate", response_model=ModerationResponse)
async def moderate_message(req: ModerationRequest):
    try:
        query = f"Please moderate this chat message: \"{req.incoming_message}\""
        
        result = assistant.process_query(query)
        
        if result.get("type") != "chat_monitoring":
            raise HTTPException(
                status_code=500,
                detail="Query was not classified as chat monitoring"
            )
        
        chat_monitor = result.get("chat_monitor", "unknown")
        reasoning = result.get("reason_chat_monitor", "No reasoning provided")

        status = chat_monitor.lower()
        
        return ModerationResponse(
            status=status,
            reason=reasoning
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing moderation: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)