from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from controllers.controller import router as controller

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
app.include_router(controller, tags=["prediction"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)