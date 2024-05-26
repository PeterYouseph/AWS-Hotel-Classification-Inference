import json
import boto3
import tarfile
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

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

        # Certificar que o diretório de download existe
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        try:
            # Faz o download do arquivo do S3
            self.s3.download_file(self.bucket_name, self.model_key, local_path)
            print("Model downloaded successfully")
        except NoCredentialsError as e:
            raise Exception("Credentials not available: " + str(e))
        except Exception as e:
            raise Exception("Erro ao baixar o modelo: " + str(e))

        try:
            # Carrega o modelo do arquivo local e extrai os arquivos
            compressed_model = tarfile.open(local_path, 'r:gz')
            compressed_model.extractall(path=download_dir)
        except Exception as e:
            raise Exception("Erro ao extrair o modelo: " + str(e))

        # Retorna o caminho do modelo extraído
        return os.path.join(download_dir, 'xgboost-model')

    def access_bucket(self):
        try:
            model_path = self.download_model()
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
