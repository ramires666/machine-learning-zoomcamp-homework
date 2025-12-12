from http.client import responses

import boto3
import json
import datetime

lambda_client = boto3.client('lambda',region_name='ap-northeast-1')

customer = {
    "customer": {
    "gender": "female",
    "seniorcitizen": 0,
    "partner": "yes",
    "dependents": "yes",
    "phoneservice": "no",
    "multiplelines": "no_phone_service",
    "internetservice": "dsl",
    "onlinesecurity": "no",
    "onlinebackup": "yes",
    "deviceprotection": "no",
    "techsupport": "no",
    "streamingtv": "yes",
    "streamingmovies": "yes",
    "contract": "month-to-month",
    "paperlessbilling": "yes",
    "paymentmethod": "electronic_check",
    "tenure": 16,
    "monthlycharges": 9.85,
    "totalcharges": 2.85
  }
}

start_time = datetime.datetime.now()
response = lambda_client.invoke(
    FunctionName='churn-prediction-v2',
    InvocationType='RequestResponse',
    Payload=json.dumps(customer)
)

result = json.loads(response['Payload'].read())
print(json.dumps(result, indent=2))
print("took: ",datetime.datetime.now() - start_time)