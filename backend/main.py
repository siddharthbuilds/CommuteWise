from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

GOOGLE_API_KEY = ''
app = FastAPI(title='CommuteWise')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RouteRequest (BaseModel):
    source:str
    destination:str
    date:str
    time:str

@app.get('/api/home')
def home():
    return {"message": "Backend API works!!"}

@app.post('/api/getroutes')
def get_routes(data:RouteRequest):
    return {data.source}


if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1", port=8000, reload=True)