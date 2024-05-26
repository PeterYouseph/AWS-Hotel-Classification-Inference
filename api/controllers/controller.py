from fastapi import APIRouter, HTTPException, Request
from services.predictionService import predict
from models.dataModel import preprocess_input
from services.inferenceLogsToDynamo import log_access
from services.credentialService import refresh_credentials
from os import environ

router = APIRouter()

@router.post("/api/v1/predict")
async def predict_endpoint(request: Request):
    try:
        sent_data = await request.json()

        processed_data = preprocess_input(sent_data)
        response = predict(processed_data) 

        # Loga a requisição e a resposta no DynamoDB
        log_access(sent_data, response)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
