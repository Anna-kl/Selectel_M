import logging
import os

from selvpcclient.client import Client, setup_http_client

logging.basicConfig(level=logging.INFO)

def Settings(file_path):
    try:
     with open(file_path, 'r', encoding='utf8') as f:
        data = f.read()
        settings={}
        data=data.split('\n')
        VPC_URL=data[0].replace('api_url:','').replace(' ','')
        settings['api_token']=data[1].replace('api_token:','').replace(' ','')
        return settings
    except:
         return 'error'
    

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


def Add_Subset(name, subnet):
    settings=Settings('D://selectel.txt')
    http_client = setup_http_client(api_url=VPC_URL, api_token=settings['api_token'])
    selvpc = Client(client=http_client)
    project=selvpc.projects.list()
    for l in project:
        if l['name']==name:
            answer=l.add_subnet(subnet,return_raw=True)
            return answer;
    return -1
def Delete_Subset(subnet):
    settings=Settings('D://selectel.txt')
    http_client = setup_http_client(api_url=VPC_URL, api_token=settings['api_token'])
    selvpc = Client(client=http_client)
   
    try:
        answer=selvpc.subnets.delete(subnet['id'])
        return answer
    except:
       
        return -1

def Delete_Project(project):
    settings=Settings('D://selectel.txt')
    http_client = setup_http_client(api_url=VPC_URL, api_token=settings['api_token'])
    selvpc = Client(client=http_client)
   
    try:
        answer=selvpc.projects.delete(project['id'])
        return answer
    except:
       
        return -1

def Delete_Ip(ip):
    settings=Settings('D://selectel.txt')
    http_client = setup_http_client(api_url=VPC_URL, api_token=settings['api_token'])
    selvpc = Client(client=http_client)
   
    try:
        answer=selvpc.floatingips.delete(ip['id'])
        return answer
    except:
       
        return -1


## Добавление ip в проект
def Add_Ip(name, ip):
    settings=Settings('D://selectel.txt')
    http_client = setup_http_client(api_url=VPC_URL, api_token=settings['api_token'])
    selvpc = Client(client=http_client)
    project=selvpc.projects.list()
    for l in project:
        if l['name']==name:
            answer=l.add_floating_ips(ip, return_raw=True)[0]
            return answer;
    return -1

## метод для создания проекта
def CreateProject(name,quotas):
    settings=Settings('D://selectel.txt')
    http_client = setup_http_client(api_url=VPC_URL, api_token=settings['api_token'])
    selvpc = Client(client=http_client)
    if quotas=='0':
        project1 = selvpc.projects.create(name,return_raw=True)
    else:
        project1 = selvpc.projects.create(name,quotas,return_raw=True)
    return project1

## метод удаления проекта
def DeleteProject(id):
    settings=Settings('D://selectel.txt')
    http_client = setup_http_client(api_url=VPC_URL, api_token=settings['api_token'])
    selvpc = Client(client=http_client)
    try:
     project1 = selvpc.projects.delete(id)
   
     return project1
    except:
        return -1

## метод для создания пользователя
def CreateUser(name, password):
    settings=Settings('D://selectel.txt')
    http_client = setup_http_client(api_url=VPC_URL, api_token='G7MeHkggaaQDV6DP8ZQx8S3Dp_82142')
    selvpc = Client(client=http_client)
    try:
        user=selvpc.users.create(name,password,enabled=True,return_raw=True)
        return user
    except:
        return -1

## метод удаления пользователя
def DeleteUser(id):
    settings=Settings('D://selectel.txt')
    http_client = setup_http_client(api_url=VPC_URL, api_token=settings['api_token'])
    selvpc = Client(client=http_client)
    try:
        user=selvpc.users.delete(id)
        return user
    except:
        return -1
## метод добавления пользователя в проект
def Add_user_in_project(id,name):
    settings=Settings('D://selectel.txt')
    http_client = setup_http_client(api_url=VPC_URL, api_token=settings['api_token'])
    selvpc = Client(client=http_client)
    user = selvpc.users.list()
    for i in user:
        if i['name']==name:
            user=i.add_to_project(id,return_raw=True)
            return user
    else:
        return -1



## метод для получения роли пользователя
def RoleManager():
    settings=Settings('D://selectel.txt')
    http_client = setup_http_client(api_url=VPC_URL, api_token=settings['api_token'])
    selvpc = Client(client=http_client)
    role=selvpc.users.roles_manager
    print(role)

## метод создания плавающего ip
def CreateIp_floating():
    settings=Settings('D://selectel.txt')
    http_client = setup_http_client(api_url=VPC_URL, api_token=settings['api_token'])
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
## метод для обновления квот в проекте
def UpdateQoatas(name,Qoates):
    settings=Settings('D://selectel.txt')
    REGION = "ru-1"
    ZONE = "ru-1a"

    http_client = setup_http_client(api_url=VPC_URL, api_token=settings['api_token'])
    selvpc = Client(client=http_client)
    project=selvpc.projects.list()
    for l in project:
        if l['name']==name:
            quotas=l.update_quotas(Qoates)
            return quotas

    return -1

