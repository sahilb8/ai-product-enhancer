from fastapi import FastAPI
from app.routers import products,agents

app = FastAPI()

app.include_router(products.router)
app.include_router(agents.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}