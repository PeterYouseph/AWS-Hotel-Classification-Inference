import json
import aioboto3
import os
from datetime import datetime, timezone
import asyncio

async def inferenceLogsToDynamo(event, context):
    session = aioboto3.Session()
    async with session.resource('dynamodb') as dynamodb:
        # Getting table name as an environment variable
        table_name = os.environ['DYNAMODB_TABLE_NAME']
        table = dynamodb.Table(table_name)

        tasks = []

        for record in event['Records']:
            payload = json.loads(record['body'])
            request = payload.get('request', {})
            response = payload.get('response', {})

            # Generating a unique identifier for the log
            log_id = str(datetime.now(timezone.utc).timestamp()).replace('.', '')

            # Preparing the log item
            item = {
                'log_id': log_id,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'request': json.dumps(request),
                'response': json.dumps(response)
            }

            # Asynchronously put the log item into the DynamoDB table
            tasks.append(table.put_item(Item=item))

        # Await all the tasks to complete
        await asyncio.gather(*tasks)

    return {
        'statusCode': 200,
        'body': json.dumps('Inference logged successfully')
    }
