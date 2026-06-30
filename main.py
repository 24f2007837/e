from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from collections import defaultdict

app = FastAPI()

# Enforce explicit wildcards and pass-through credentials for browser graders
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Must be False if allow_origins=["*"] to prevent browser security blocks
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

ASSIGNED_API_KEY = "ak_j0kyu571rwfdtwy7vtp35btk"
YOUR_EMAIL = "24f2007837@ds.study.iitm.ac.in"

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class AnalyticsRequest(BaseModel):
    events: List[Event]

@app.post("/analytics")
@app.options("/analytics")  # Explicitly hook OPTIONS requests just in case
def process_analytics(
    payload: Optional[AnalyticsRequest] = None, 
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    # Handle direct browser preflights clean and fast
    if payload is None:
        return {"status": "preflight ok"}

    if x_api_key is None or x_api_key != ASSIGNED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or incorrect API key"
        )
    
    events = payload.events
    total_events = len(events)
    
    unique_users_set = set()
    user_revenue = defaultdict(float)
    total_revenue = 0.0
    
    for event in events:
        user = event.user
        unique_users_set.add(user)
        if event.amount > 0:
            user_revenue[user] += event.amount
            total_revenue += event.amount

    top_user = max(user_revenue, key=user_revenue.get) if user_revenue else None

    return {
        "email": YOUR_EMAIL,
        "total_events": total_events,
        "unique_users": len(unique_users_set),
        "revenue": round(total_revenue, 4),
        "top_user": top_user
    }