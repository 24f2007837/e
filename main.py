from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from collections import defaultdict

app = FastAPI()

# Enable global CORS so the grader browser can check it directly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Your Assigned Values ---
ASSIGNED_API_KEY = "ak_j0kyu571rwfdtwy7vtp35btk"
YOUR_EMAIL = "24f2007837@ds.study.iitm.ac.in"

# --- Request Schemas ---
class Event(BaseModel):
    user: str
    amount: float
    ts: int

class AnalyticsRequest(BaseModel):
    events: List[Event]

# --- Analytics Endpoint ---
@app.post("/analytics")
def process_analytics(
    payload: AnalyticsRequest, 
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    # Enforce strict API key authentication
    if x_api_key is None or x_api_key != ASSIGNED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or incorrect API key"
        )
    
    events = payload.events
    total_events = len(events)
    
    # Track unique users and calculate positive revenue per user
    unique_users_set = set()
    user_revenue = defaultdict(float)
    total_revenue = 0.0
    
    for event in events:
        user = event.user
        unique_users_set.add(user)
        
        # Aggregation rules: sum amount values where amount > 0 only
        if event.amount > 0:
            user_revenue[user] += event.amount
            total_revenue += event.amount

    # Determine top_user (user with the highest positive-amount total)
    if user_revenue:
        top_user = max(user_revenue, key=user_revenue.get)
    else:
        top_user = None

    return {
        "email": YOUR_EMAIL,
        "total_events": total_events,
        "unique_users": len(unique_users_set),
        "revenue": round(total_revenue, 4),
        "top_user": top_user
    }