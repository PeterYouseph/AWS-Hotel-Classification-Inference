import json
import boto3
import tarfile
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class ModelManager:
    def __init__(self):
        # Carrega as variáveis de ambiente
        load_dotenv()

        # Configura S3
        self.s3 = boto3.client('s3')
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.model_key = os.getenv('MODEL_KEY')
        self.profile_name = os.getenv('PROFILE_NAME')

        # Verifica se as variáveis de ambiente foram setadas
        if not self.bucket_name or not self.model_key:
            raise ValueError("BUCKET_NAME and MODEL_KEY must be set in the environment variables")

    def check_aws_credentials(self):
        try:
            session = boto3.Session(profile_name=self.profile_name)
            s3 = session.client('s3')
            response = s3.list_buckets()
            print('Credenciais configuradas corretamente. Buckets disponíveis:')
            for bucket in response['Buckets']:
                print(f'  {bucket["Name"]}')
            return {'status': 'success', 'buckets': [bucket['Name'] for bucket in response['Buckets']]}
        except NoCredentialsError:
            print('Credenciais não encontradas. Configure suas credenciais AWS.')
            return {'status': 'error', 'message': 'Credenciais não encontradas.'}
        except PartialCredentialsError:
            print('Credenciais incompletas. Verifique suas credenciais AWS.')
            return {'status': 'error', 'message': 'Credenciais incompletas.'}
        except Exception as e:
            print(f'Erro ao verificar as credenciais: {e}')
            return {'status': 'error', 'message': f'Erro ao verificar as credenciais: {e}'}
        
    def download_model(self):
        # Definição de caminho para o arquivo local do modelo
        local_path = './assets/models/model.tar.gz'
        download_dir = './assets/models/'

        # Certificar que o diretório de download existe
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        try:
            # Faz o download do arquivo do S3 se o modelo não existir localmente
            if not os.path.exists(local_path):
                print("Model not found locally, downloading from S3")
                session = boto3.Session(profile_name=self.profile_name)
                self.s3 = session.client('s3')
                print(f"Downloading model from bucket: {self.bucket_name}, key: {self.model_key}")
                self.s3.download_file(self.bucket_name, self.model_key, local_path)
                print("Model downloaded successfully")
            else:
                print("Model already exists locally")
        except NoCredentialsError as e:
            raise Exception("Credentials not available: " + str(e))
        except Exception as e:
            raise Exception("Erro ao baixar o modelo: " + str(e))

        try:
            # Carrega o modelo do arquivo local e extrai os arquivos
            print(f"Extracting model from {local_path}")
            with tarfile.open(local_path, 'r:gz') as compressed_model:
                compressed_model.extractall(path=download_dir)
            print("Model extracted successfully")
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
