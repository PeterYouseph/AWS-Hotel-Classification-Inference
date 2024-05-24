import json
from acessS3Service import ModelManager

model_manager = ModelManager()

async def model_retrieve():
    response = await model_manager.access_bucket()
    if response['statusCode'] == 200:
        return json.loads(response['body'])
    else:
        raise Exception(json.loads(response['body'])['error'])



# Função para predizer
def predict(data):
    try:
        # Recupera o modelo
        model_response = model_retrieve()

        # Verifica se houve erro na resposta
        if 'error' in model_response['body']:
            return model_response

        # Obtém o modelo da resposta
        model = model_response['body'].get('model', None)
        if model is None:
            raise ValueError("Model not found in response")

        # Realiza a predição
        prediction = model.predict(data)
        return json.dumps({"prediction": prediction})

    except KeyError as ke:
        return {"error": f"KeyError: {str(ke)}"}
    except AttributeError as ae:
        return {"error": f"AttributeError: {str(ae)}"}
    except Exception as e:
        return {"error": str(e)}
