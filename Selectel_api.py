import logging
import os

from selvpcclient.client import Client, setup_http_client

logging.basicConfig(level=logging.INFO)



#
# You can create and get api token here
# https://support.selectel.ru/keys
#
VPC_TOKEN = os.getenv('SEL_TOKEN', None)

#
# You can get actual api URL here
# https://support.selectel.ru/vpc/docs
#
VPC_URL = "https://api.selectel.ru/vpc/resell"

def CreateProject(project):
    http_client = setup_http_client(api_url=VPC_URL, api_token='G7MeHkggaaQDV6DP8ZQx8S3Dp_82142')
    selvpc = Client(client=http_client)
    project1 = selvpc.projects.create(project['name'],project['quatas'],return_raw=True)
def CreateUser(user):
    http_client = setup_http_client(api_url=VPC_URL, api_token='G7MeHkggaaQDV6DP8ZQx8S3Dp_82142')
    selvpc = Client(client=http_client)
    user=selvpc.users.create(user['name'],user['password'],return_raw=True)
def RoleManager():
    http_client = setup_http_client(api_url=VPC_URL, api_token='G7MeHkggaaQDV6DP8ZQx8S3Dp_82142')
    selvpc = Client(client=http_client)
    role=selvpc.users.roles_manager
    print(role)
def CreateIp_floating():
    REGION = "ru-1"
    http_client = setup_http_client(api_url=VPC_URL, api_token='G7MeHkggaaQDV6DP8ZQx8S3Dp_82142')
    selvpc = Client(client=http_client)
    project=selvpc.projects.list()[0]
    floating_ips = {
        "floatingips": [
            {
                "region": REGION,
                "quantity": 1
            }
        ]
    }
    project.add_floating_ips(floating_ips)
def UpdateQoatas(Qoates):

    REGION = "ru-1"
    ZONE = "ru-1a"

    http_client = setup_http_client(api_url=VPC_URL, api_token='G7MeHkggaaQDV6DP8ZQx8S3Dp_82142')
    selvpc = Client(client=http_client)

    Quatas=project.update_quotas(Qoates)

    return Quatas

##users=selvpc.users.list()[0]
##users.add_to_project('43a224ce69744e0a994e1e7b8bc7e3b7',return_raw=True)
##users=selvpc.users.list()[0]
REGION = "ru-1"
ZONE = "ru-1a"
project={}
project['name']='Mandarin'

Quotas= {
            "compute_cores": [
                {
                    "region": REGION,
                    "zone": ZONE,
                    "value": 5
                }
            ],
            "compute_ram": [
                {
                    "region": REGION,
                    "zone": ZONE,
                    "value": 512
                }
            ]}

project['quatas']=Quotas
##UpdateQoatas('TEstAnn')