# # services/predictionService.py

# import json
# import numpy as np
# import xgboost as xgb
# from os import environ
# from services.accessS3Service import ModelManager
# from services.credentialService import refresh_credentials

# model_manager = ModelManager()

# def model_retrieve():
#     response = model_manager.access_bucket()
#     if response['statusCode'] == 200:
#         return json.loads(response['body'])['model_path']
#     else:
#         raise Exception(json.loads(response['body'])['error'])

# def load_xgboost_model(model_path):
#     model = xgb.Booster()
#     model.load_model(model_path)  # Corrigido para load_model
#     return model

# # Função para predizer
# async def predict(data):
#     try:
#         profile_name = environ.get('PROFILE_NAME')
#         print(f"Profile name: {profile_name}")
#         # Atualizando as credenciais do AWS SSO 
#         refresh_credentials(profile_name)
#         # Recupera o caminho do modelo
#         model_path = model_retrieve()
#         model = load_xgboost_model(model_path)

#         # Verifica se o modelo foi carregado
#         if model is None:
#             raise ValueError("Model not found in response")
        
#         # # Realiza a predição
#         # dmatrix = xgb.DMatrix(data)  # Converte os dados para DMatrix
#         prediction = model.predict(data)
#         print(f"Prediction: {prediction}")
#         # Mapear rótulos de volta ao original
#         inverse_label_mapping = {0: 1, 1: 2, 2: 3}
#         predicted_labels = int(inverse_label_mapping.get(np.argmax(prediction, axis=1)[0]))

#         return {"result": predicted_labels}

#     except KeyError as ke:
#         return {"error 1": f"KeyError: {str(ke)}"}
#     except AttributeError as ae:
#         return {"error 2": f"AttributeError: {str(ae)}"}
#     except Exception as e:
#         return {"error 3": str(e)}

# # Função para verificar as credenciais AWS e listar os buckets
# def check_credentials():
#     return model_manager.check_aws_credentials()


import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import pickle
from os import environ
from services.accessS3Service import ModelManager
from services.credentialService import refresh_credentials
from models.dataModel import preprocess_input

model_manager = ModelManager()

def model_retrieve():
    response = model_manager.access_bucket()
    if response['statusCode'] == 200:
        return json.loads(response['body'])['model_path']
    else:
        raise Exception(json.loads(response['body'])['error'])

def load_xgboost_model(model_path):
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

async def predict(data):
    try:
        profile_name = environ.get('PROFILE_NAME')
        print(f"Profile name: {profile_name}")
        
        refresh_credentials(profile_name)
        model_path = model_retrieve()
        model = load_xgboost_model(model_path)

        if model is None:
            raise ValueError("Model not found in response")

        prediction = model.predict(data)
        print(f"Prediction: {prediction}")
        
        inverse_label_mapping = {0: 1, 1: 2, 2: 3}
        predicted_label = int(inverse_label_mapping.get(np.argmax(prediction, axis=1)[0]))

        return {"result": predicted_label}

    except KeyError as ke:
        return {"error 1": f"KeyError: {str(ke)}"}
    except AttributeError as ae:
        return {"error 2": f"AttributeError: {str(ae)}"}
    except Exception as e:
        return {"error 3": str(e)}

def check_credentials():
    return model_manager.check_aws_credentials()
