import json
import boto3
from RunDocker import RunDocker
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    
    my_key = event['Records'][0]['s3']['object']['key']  
    my_bucket = event['Records'][0]['s3']['bucket']['name']
    content = s3.Object(my_bucket, my_key)
    file_data = content.get()['Body'].read()
    file_data = file_data.decode('utf-8')
    my_parameters = json.loads(file_data)
    docker_obj=RunDocker()
    run_docker_res=docker_obj.run_docker_image(my_parameters)
    return run_docker_res
