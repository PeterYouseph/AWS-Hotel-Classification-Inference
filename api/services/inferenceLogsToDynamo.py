from datetime import datetime, timezone
import json
import aioboto3
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configura DynamoDB
DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')
AWS_REGION = os.getenv('AWS_REGION')

# Inicializa o cliente boto3
dynamodb_resource = aioboto3.resource('dynamodb', region_name=AWS_REGION)

async def log_access(request_data: dict, response_data: dict):
    async with dynamodb_resource.Table(DYNAMODB_TABLE_NAME) as table:
        # Gerar um identificador único para o log
        log_id = str(datetime.now(timezone.utc).timestamp()).replace('.', '')

        # Preparar o item de log
        item = {
            'log_id': log_id,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'request': json.dumps(request_data),
            'response': json.dumps(response_data)
        }

        # Inserir o item de log na tabela DynamoDB de forma assíncrona
        await table.put_item(Item=item)