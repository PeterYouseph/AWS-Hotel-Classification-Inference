from datetime import datetime, timezone
import json
import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Carrega as variáveis de ambiente
load_dotenv()

# Configura DynamoDB
DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')
AWS_REGION = os.getenv('AWS_REGION')

def log_access(request_data: dict, response_data: dict):
    # Inicializa o recurso do DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)

    # Gerar um identificador único para o log
    log_id = str(datetime.now(timezone.utc).timestamp()).replace('.', '')

    # Preparar o item de log
    item = {
        'log_id': log_id,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'request': json.dumps(request_data),
        'response': json.dumps(response_data)
    }

    try:
        # Inserir o item de log na tabela DynamoDB
        table.put_item(Item=item)
        print("Log de acesso registrado no DynamoDB")
    except ClientError as e:
        print(f"Erro ao registrar o log de acesso no DynamoDB: {e}")