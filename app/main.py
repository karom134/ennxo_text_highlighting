from fastapi import FastAPI
from .services import services

app=FastAPI()

app.include_router(services.router)

@app.get("/")
async def root():
	return {"message":"hello"}