from fastapi import APIRouter, HTTPException, Request
from services.predictionService import predict
from models.dataModel import preprocess_input
from services.inferenceLogsToDynamo import log_access

router = APIRouter()

@router.post("/api/v1/predict")
async def predict(request: Request):
    try:
        sent_data = await request.json()

        processed_data = preprocess_input(sent_data)
        response = await predict(processed_data)

        await log_access(sent_data, response)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



