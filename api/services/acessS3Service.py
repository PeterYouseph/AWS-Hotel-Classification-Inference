import json
import boto3
import pickle
import os
from dotenv import load_dotenv

class ModelManager:
    def __init__(self):
        # Carrega as variáveis de ambiente
        load_dotenv()

        # Configura S3
        self.s3 = boto3.client('s3')
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.model_key = os.getenv('MODEL_KEY')

        # Verifica se as variáveis de ambiente foram setadas
        if not self.bucket_name or not self.model_key:
            raise ValueError("BUCKET_NAME and MODEL_KEY must be set in the environment variables")
        
    def download_model(self):
        # Definição de caminho para o arquivo local do modelo
        local_path = '/tmp/modelo.pkl'
        # Faz o download do arquivo do S3
        self.s3.download_file(self.bucket_name, self.model_key, local_path)
        # Carrega o modelo do arquivo local
        with open(local_path, 'rb') as file:
            model = pickle.load(file)
        return model

    def access_bucket(self):
        try:
            model = self.download_model()
            
            # Caso precise resserializar
            # model_base64 = base64.b64encode(pickle.dumps(model)).decode('utf-8')

            response = {
                'statusCode': 200,
                'body': json.dumps({'model': str(model)})  # Convertendo o modelo para string para JSON
            }
        except Exception as e:
            response = {
                'statusCode': 500,
                'body': json.dumps({'error': 'Erro ao baixar o modelo: ' + str(e)})
            }
        return response

