import json
import boto3
import configparser

client=boto3.client('ssm')
ssm_path='/poc/ssm-path'
ssm_full_path=ssm_path+'/write'
c=boto3.client('ecs')

config = configparser.ConfigParser()

class RunDocker:
    
    def __init__(self):
        my_param=client.get_parameters_by_path(
            Path=ssm_path,
            Recursive=False,
            WithDecryption=True
        )
        
        print(my_param)
        print(my_param.get('Parameters'))
        
        if 'Parameters' in my_param and len(my_param.get('Parameters')) > 0:
            for param in my_param.get('Parameters'):
                section_name =  param.get('Name')
                config_values = json.loads(param.get('Value'))
                config_dict = {section_name: config_values}
                config.read_dict(config_dict) 
    
    def run_docker_image(self, my_parameters):
        try:
            
            my_task_definition_name = config[ssm_full_path]['my_task_definition_name']
            cluster_name = config[ssm_full_path]['cluster']
            what_is_launch_type = config[ssm_full_path]['launchType']
            who_started = config[ssm_full_path]['startedBy']
            
            container_name = config[ssm_full_path]['container_name']
            DOCKER_CLIENT_TIMEOUT = config[ssm_full_path]['DOCKER_CLIENT_TIMEOUT']
            COMPOSE_HTTP_TIMEOUT = config[ssm_full_path]['COMPOSE_HTTP_TIMEOUT']
            sg_name = config[ssm_full_path]['security_group']
            
            subnets_detais = config[ssm_full_path]['subnets_detais']
            list_of_subnets=subnets_detais.split(',')
            
            subnet_1=list_of_subnets[0]
            subnet_2=list_of_subnets[1]
            
            public_ip = config[ssm_full_path]['public_ip']
            
            print(my_task_definition_name)
            response = c.run_task(
            cluster=cluster_name,
            taskDefinition=my_task_definition_name,
            count=1,
            launchType=what_is_launch_type,
            startedBy=who_started,
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets_detais': [
                         subnet_1,subnet_2
                    ],
                    'securityGroups': [
                       sg_name
                    ],
                    'assignPublicIp': public_ip
                }
            },
            
            overrides={
                'containerOverrides': [
                    {
                        'name': container_name,
                        'command': [
                            "python","some_folder/calc.py",my_parameters
                        ],
                        'environment': [
                    {
                        'name': 'COMPOSE_HTTP_TIMEOUT',
                        'value':COMPOSE_HTTP_TIMEOUT
                    },
                    {
                        'name':'DOCKER_CLIENT_TIMEOUT',
                        'value':DOCKER_CLIENT_TIMEOUT
                    }
                ],
                'cpu': 4096,
                
                    },
                ],
                
            })
            
            return str(response)
            
        except Exception as ex:
            
            print(ex)
            print('error in running docker file...')
            raise
        finally:
            print('executing the docker file')
