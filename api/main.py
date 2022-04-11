from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import itlapi

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    usage = """GET: /entrant/<entrant_id>"""
    return usage

@app.get("/leaderboard")
def leaderboard():
    return "This API has been discontinued."

@app.get("/entrant/{entrant_id}")
def get_entrant(entrant_id: int, q: Optional[str] = None):
    try:
        entrant = itlapi.get_entrant(entrant_id)
        return entrant
    except:
        raise HTTPException(status_code=500, detail="Failed to retrieve entrant information.")

@app.get("/v2/entrant/{entrant_id}")
def v2_get_entrant(entrant_id: int, q: Optional[str] = None):
    try:
        entrant = itlapi.get_entrant(entrant_id)
        return entrant
    except:
        raise HTTPException(status_code=500, detail="Failed to retrieve entrant information.")

@app.get("/versus/entrant/{entrant_id}")
def get_versus_info(entrant_id: int, q: Optional[str] = None):
    try:
        versus_info = itlapi.get_versus_info(entrant_id)
        return versus_info
    except:
        raise HTTPException(status_code=500, detail="Failed to retrieve versus information.")
    return entrant_id