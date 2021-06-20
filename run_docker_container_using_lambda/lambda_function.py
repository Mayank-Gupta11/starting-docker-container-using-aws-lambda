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
    file_datadict = json.loads(file_data)
    
    flag=file_datadict['flag']
    
    bucket=file_datadict['bucket']
    if flag=='new':
        time_id=file_datadict['time']
    else:
        print(file_datadict['batch_id'])
        string_format=file_datadict['batch_id']
        string_format=str(string_format)
        time_id=string_format.split('_')[0]
    
    s3_trigger_key='some_path/new_path/'+time_id+'/'
        
    docker_obj=RunDocker()
    run_docker_res=docker_obj.run_docker_image(time_id,s3_trigger_key,bucket,flag)
    
    
    return run_docker_res