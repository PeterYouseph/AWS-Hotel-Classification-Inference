from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from predictionService  import predict    

app = FastAPI()

# Configurando o CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# endpoint principal para a predição
@app.post("/api/v1/predict")
async def predict(request: Request):
    data = await request.json()
    response = predict(data)

    return response