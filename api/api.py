from fastapi import FastAPI
from controllers.controller import router

app = FastAPI()

# Incluindo as rotas
app.include_router(router)

# Definindo um endpoint raiz simples
@app.get("/")
async def read_root():
    return {"message": "API de predição de clientes"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
