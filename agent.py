from dotenv import load_dotenv
from typing import Optional, Dict, Any

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_tavily import TavilySearch

import json

load_dotenv()


class MarketplaceAssistantSimple:
    def __init__(self):
        self.llm = init_chat_model(model_provider="groq", model="llama-3.3-70b-versatile")
        self.search = TavilySearch(max_results=5, topic="general")
        
    def clean_json_response(self, content: str) -> str:
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        return content.strip()
    
    def classify_message(self, user_query: str) -> Dict[str, bool]:        
        SYSTEM_PROMPT = """
        You are an AI assistant.
        Classify the user query into exactly ONE category.

        Return ONLY valid JSON:
        {
            "is_price_suggestion": true/false,
            "is_chat_monitoring": true/false
        }

        Rules:
        - price_suggestion: user asking price of a product / selling / buying / worth / valuation.
        - chat_monitoring: user gives chat message and wants moderation or toxicity check.
        - Always set one true and the other false.
        """
        
        try:
            resp = self.llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_query)
            ])
            
            content = self.clean_json_response(resp.content)
            data = json.loads(content)
            
            return {
                "is_price_suggestion": bool(data.get("is_price_suggestion", False)),
                "is_chat_monitoring": bool(data.get("is_chat_monitoring", False))
            }
        except Exception as e:
            print(f"Classification error: {e}")
            return {"is_price_suggestion": True, "is_chat_monitoring": False}

    
    def extract_search_query(self, user_query: str) -> str:        
        SYSTEM_PROMPT = """
        You are a search query generator for a second-hand marketplace.

        Given a user query about product pricing, extract the key information and create a concise search query.
        Focus on: brand, model, condition, location.

        Return ONLY the search query text (no JSON, no extra explanation).
        Example: "iPhone 13 Pro 256GB price OLX Cashify India"
        """
        
        try:
            resp = self.llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_query)
            ])
            return resp.content.strip()
        except Exception as e:
            print(f"Search query extraction error: {e}")
            return user_query
    
    def price_suggestion(self, user_query: str) -> Dict[str, str]:
        
        try:
            search_query = self.extract_search_query(user_query)
            print(f"Searching for: {search_query}")
            
            search_results = self.search.invoke({"query": search_query})
            
            ANALYSIS_PROMPT = """
            You are a helpful AI assistant for a second-hand marketplace.

            User Query: {user_query}

            Web Search Results:
            {search_results}

            Based on the search results, analyze the market prices and provide a price suggestion.
            Don't tell about you searching on other platforms like olx, cashify for this product in the reasoning.
            Return ONLY valid JSON in this format:
            {{
            "price_range": "25000-30000",
            "reason_price_range": "Based on the condition of the product and the price of this product in market lies in that range only"
            }}
            """
            
            resp = self.llm.invoke([
                HumanMessage(content=ANALYSIS_PROMPT.format(
                    user_query=user_query,
                    search_results=str(search_results)
                ))
            ])
            
            content = self.clean_json_response(resp.content)
            
            if "{" in content and "}" in content:
                start_idx = content.find("{")
                end_idx = content.rfind("}") + 1
                json_str = content[start_idx:end_idx]
                data = json.loads(json_str)
                
                return {
                    "price_range": data.get("price_range", "Unable to determine"),
                    "reason_price_range": data.get("reason_price_range", "Analysis completed")
                }
            else:
                return {
                    "price_range": "Unable to determine",
                    "reason_price_range": content[:300]
                }
                
        except Exception as e:
            print(f"Price suggestion error: {e}")
            return {
                "price_range": "Error",
                "reason_price_range": f"Failed to process: {str(e)}"
            }
    
    def chat_monitoring(self, user_query: str) -> Dict[str, str]:        
        SYSTEM_PROMPT = """
        You are a chat moderation assistant.

        Check if message contains:
        - abusive language
        - phone number / email / personal identity info

        Return ONLY valid JSON:
        {
        "chat_monitor": "Abusive" OR "invalid message" OR "clean",
        "reason_chat_monitor": "short reason"
        }
        """
        
        try:
            resp = self.llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_query)
            ])
            
            content = self.clean_json_response(resp.content)
            data = json.loads(content)
            
            return {
                "chat_monitor": data.get("chat_monitor", "unknown"),
                "reason_chat_monitor": data.get("reason_chat_monitor", "Analysis completed")
            }
        except Exception as e:
            print(f"Chat monitoring error: {e}")
            return {
                "chat_monitor": "error",
                "reason_chat_monitor": f"Failed to analyze: {str(e)}"
            }
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        
        print("Classifying message...")
        classification = self.classify_message(user_query)
        
        if classification["is_price_suggestion"]:
            print("Route: Price Suggestion")
            result = self.price_suggestion(user_query)
            return {
                "type": "price_suggestion",
                **result
            }
        else:
            print("Route: Chat Monitoring")
            result = self.chat_monitoring(user_query)
            return {
                "type": "chat_monitoring",
                **result
            }
