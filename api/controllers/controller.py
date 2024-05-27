from fastapi import APIRouter, HTTPException, Request
from services.predictionService import predict
from models.dataModel import preprocess_input
from services.inferenceLogsToDynamo import log_access
from os import environ
from services.predictionService import predict, check_credentials
import xgboost as xgb

router = APIRouter()

@router.post("/api/v1/predict")
async def predict_endpoint(request: Request):
    try:
        # Recebe os dados de entrada
        sent_data = await request.json()
        
        # Preprocessa os dados de entrada e converte xgboost.DMatrix para predição
        
        processed_data = preprocess_input(sent_data)

        dmatrix_data = xgb.DMatrix(processed_data, feature_names=processed_data.columns)

        # Realiza a predição com os dados processados
        response = await predict(dmatrix_data)

        # Loga a requisição e a resposta no DynamoDB
        log_access(sent_data, response)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/check_credentials")
async def check_credentials_endpoint():
    try:
        response = check_credentials()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))