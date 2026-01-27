from fastapi import FastAPI
from pydantic import BaseModel
from schemas import SuggestRequest,SuggestResponse,moderationRequest,moderationResponse 

app=FastAPI()


@app.post("/negotiate")
async def negotiate(req:SuggestRequest):
    pass

@app.post("/moderate")
async def moderate(req:moderationRequest)
    pass

if __name__== "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)