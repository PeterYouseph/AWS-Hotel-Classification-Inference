import json
import boto3
import tarfile
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
        local_path = './assets/models/model.tar.gz'
        download_dir = './assets/models/'
        # Faz o download do arquivo do S3
        self.s3.download_file(self.bucket_name, self.model_key, local_path)
        # Carrega o modelo do arquivo local
        # Extract compressed file
        compressed_model = tarfile.open('./assets/models/model.tar.gz','r:gz')
        compressed_model.extractall(path=download_dir)
        return download_dir + 'xgboost-model'

    def access_bucket(self):
        try:
            model_path = self.download_model()
            # Caso precise resserializar
            # model_base64 = base64.b64encode(pickle.dumps(model)).decode('utf-8')

            response = {
                'statusCode': 200,
                'body': json.dumps({'model_path': str(model_path)})  
            }
        except Exception as e:
            response = {
                'statusCode': 500,
                'body': json.dumps({'error': 'Erro ao baixar o modelo: ' + str(e)})
            }
        return response

