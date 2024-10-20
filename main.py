from fastapi import FastAPI

app = FastAPI()


@app.get("/plm")
async def root():
    return {"message": "Welcome to the PLM World!!!"}


@app.get("/plm/api/getParts")
async def getParts():
    return {"parts": f"Wheel"}

