import json
from services.acessS3Service import ModelManager
import xgboost as xgb
import numpy as np 


model_manager = ModelManager()

async def model_retrieve():
    response = await model_manager.access_bucket()
    if response['statusCode'] == 200:
        return json.loads(response['body'])
    else:
        raise Exception(json.loads(response['body'])['error'])

def loadxgboostmodel(model_path):
    model = xgb.Booster()
    model.loadmodel(model_path)
    return model


# Função para predizer
def predict(data):
    try:
        # Recupera o caminho do modelo
        model_path = model_retrieve()
        model = loadxgboostmodel(model_path)

        # Verifica se o modelo foi carregado
        if model is None:
            raise ValueError("Model not found in response")

        # Realiza a predição
        prediction = model.predict(data)

        # Mapear rótulos de volta ao original
        inverse_label_mapping = {0: 1, 1: 2, 2: 3}
        predicted_labels = int(inverse_label_mapping.get(np.argmax(prediction, axis=1)[0]))

        return json.dumps({"result": predicted_labels})

    except KeyError as ke:
        return {"error": f"KeyError: {str(ke)}"}
    except AttributeError as ae:
        return {"error": f"AttributeError: {str(ae)}"}
    except Exception as e:
        return {"error": str(e)}
