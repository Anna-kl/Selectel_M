<<<<<<< HEAD


from datetime import datetime
from flask import render_template
from flask import Flask, jsonify,request
from Selectel import app
import Selectel_api
import json
import requests
from flask_pymongo import PyMongo
import psycopg2

def Settings(file_path):
   
    file = file_path
    try:
     with open(file, 'r', encoding='utf8') as f:
        data = f.read()
    except:
         file = file_path

         with open(file, 'r', encoding='utf8') as f:
                data = f.read()
    data = data.split('\n')
    setting = {}
    setting['dbname']=data[0].replace('dbname:','').replace(' ','')
    setting['host'] = data[1].replace('host:', '').replace(' ', '')
    setting['user']=data[2].replace('user:','').replace(' ','')

    setting['password'] = data[3].replace('password:', '').replace(' ', '')
    return setting
## конфигурация базы данных MongoDB
app.config['MONGO_DBNAME'] = 'selectel'
app.config["MONGO_URI"] = "mongodb://localhost:27017/selectel"
mongo = PyMongo(app)
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]
@app.route('/')


## метод для работы с проектом
@app.route('/project', methods=['POST'])
def task_project():


    if not request.json:
        abort(400)
   ## print (request.json)
    answer=request.json
    ## декодруем json запрос
    value={}
    value['resource']=answer['resource']
     
    if answer['resource']=='Selectel':
        ## создание проекта
        if answer['task']=='create':
            ## подключение к базе данных
             conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
             try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
             except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
             qoutas={}
             ## поиск проекта с таким же именем
             project=mongo.db.projects.find({'name':answer['name']}).count()
             ## возвращает ошибку, если есть совпадение имен
             if project!=0:
                return jsonify({'project': 'already exist'})
            ## подставляем нужную зону в метод создания по коду из таблицы
             zona=answer['zona']
             sql='''SELECT region, "zone" FROM resources.region where id=test'''
             sql=sql.replace('test',str(zona))
             try:
                cur = conn.cursor()
     
                cur.execute(sql)
                data= cur.fetchall()
             except psycopg2.Error as err:
                    jsonify({'report': err})
            ## создаем словарь квот в нужном формате, на основе запроса пользователя
             qoutas['compute_cores']=[]
             comp=answer['quotas']['compute_cores']
             comp[0]['zone']=data[0][1]
             comp[0]['region']=data[0][0]
             qoutas['compute_cores']=comp
             try:
                comp=answer['quotas']['compute_ram']
                comp[0]['zone']=data[0][1]
                comp[0]['region']=data[0][0]
                qoutas['compute_ram']=comp
             except:
                 d=0
             try:
                comp=answer['quotas']['volume_gigabytes_universal']
                comp[0]['zone']=data[0][1]
                comp[0]['region']=data[0][0]
                qoutas['volume_gigabytes_universal']=comp
             except:
                 d=0
             try:
                comp=answer['quotas']['volume_gigabytes_fast']
                comp[0]['zone']=data[0][1]
                comp[0]['region']=data[0][0]
                qoutas['volume_gigabytes_fast']=comp
             except:
                 d=0
             try:
                comp=answer['qoutas']['volume_gigabytes_basic']
                comp[0]['zone']=data[0][1]
                comp[0]['region']=data[0][0]
                qoutas['volume_gigabytes_basic']=comp
             except:
                 d=0
              ## формирование запроса к системе биллинга для проверки баланса
             value['task']='bill'
             value['quotas']=qoutas
             value['id']=answer['id']
             value=json.dumps(value)
             
             headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
             r=requests.post('http://localhost:5500/bill',json=value)
             data=r.text
             responce=data.replace('\n','')
             data=json.loads(responce)
             if data['status']=='Ok':
                 ## создаем проект
                project=Selectel_api.CreateProject(answer['name'],qoutas)
                ## добавляем запись в MongoDB
                mongo.db.projects.insert({'name':project['name'],'id_company':answer['id'],'resource':answer['resource'],'id':project['id'],'url':project['url'],'enabled':project['enabled'],'quotas':project['quotas']})
                ## формируем запрос на запись информации о проекте в системе биллинга
                value={}
                value['resource']=answer['resource']
                value['task']='create_project'
                value['id_company']=answer['id']
                value['id_project']=project['id']
                value['bill']=data['bill']
                value['full']=project['quotas']
                value=json.dumps(value)
             
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r=requests.post('http://localhost:5500/information',json=value)
                data=r.text
                responce=data.replace('\n','')
                data=json.loads(responce)
                conn.close()
                ## формирование ответа на запрос
                if data['report']=='Ok':
                    return jsonify({'project': project['url']})
                elif data['report']=='error':
                    return jsonify({'project': 'error'})
           ## обработка запроса на обновление квот  
        elif answer['task']=='update':
             conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
             try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
             except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
             qoutas={}
             project=mongo.db.projects.find_one({'name':answer['name']})
             qoutas_now=project['quotas']
             
             if project==0:
                return jsonify({'project': 'project not find'})
             zona=answer['zona']
             sql='''SELECT region, "zone" FROM resources.region where id=test'''
             sql=sql.replace('test',str(zona))
             try:
                cur = conn.cursor()
     
                cur.execute(sql)
                data= cur.fetchall()
             except psycopg2.Error as err:
                    jsonify({'report': err})
             qoutas['compute_cores']=[]
             comp=qoutas_now['compute_cores']
             comp[0]['zone']=qoutas_now['compute_cores'][0]['zone']
             comp[0]['region']=qoutas_now['compute_cores'][0]['region']
             qoutas['compute_cores']=comp
             try:
                comp=qoutas_now['compute_ram']
                comp[0]['zone']=qoutas_now['compute_ram'][0]['zone']
                comp[0]['region']=qoutas_now['compute_ram'][0]['region']
                qoutas['compute_ram']=comp
             except:
                 d=0
             try:
                comp=qoutas_now['volume_gigabytes_universal']
                comp[0]['zone']=qoutas_now['volume_gigabytes_universal'][0]['zone']
                comp[0]['region']=qoutas_now['volume_gigabytes_universal'][0]['region']
                qoutas['volume_gigabytes_universal']=comp
             except:
                 d=0
             try:
                comp=qoutas_now['volume_gigabytes_fast']
                comp[0]['zone']=qoutas_now['volume_gigabytes_universal'][0]['zone']
                comp[0]['region']=qoutas_now['volume_gigabytes_universal'][0]['region']
                qoutas['volume_gigabytes_fast']=comp
             except:
                 d=0
             try:
                comp=qoutas_now['volume_gigabytes_basic']
                comp[0]['zone']=qoutas_now['volume_gigabytes_basic'][0]['zone']
                comp[0]['region']=qoutas_now['volume_gigabytes_basic'][0]['region']
                qoutas['volume_gigabytes_basic']=comp
             except:
                 d=0
             value['task']='bill'
             value['quotas']=qoutas
             value['id']=answer['id']
             value=json.dumps(value)
             
             headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
             project=Selectel_api.UpdateQoatas(answer['name'],qoutas)
          
             jsonify({'project': 'error'})
        ## запрос на удалениt проекта
        elif answer['task']=='delete':
            try:
            ## поиск проект по названию
              project=mongo.db.projects.find_one({'name':answer['name']})
              if project is not None:
                  ## удаление проекта из базы MongoDB и из Selectel
                answer=mongo.db.projects.delete_one({'name':answer['name']})
                Selectel_api.DeleteProject(project['id'])
                if answer.count()>0:
                    return jsonify({'project': 'delete'})
                else:
                   return jsonify({'project': 'not found'})
            except:
                return jsonify({'project': 'error'})
        ## добавление подсети в проект
        elif answer['task']=='subnet':
            setting=Settings('D://settings_selectel.txt')
            conn_string = "dbname=\'"+setting['dbname']+'" user=\'"' + setting['user'] + '\'' + " host=\'" + setting['host'] + '\'' + ' password=\'' + setting['password'] + '\''
            try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
            except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
          
            sub={
                "subnets": [
                    {
                         "region": "ru-1",
                         "quantity": 1,
                         "type": "ipv4",
                         "prefix_length": 29
                    }
                           ]
                }

            count=answer['count_ip']
            sql='''SELECT prefix FROM resources.prefix where count_ip=test1'''
            sql=sql.replace('test1',str(count))
            try:
                cur = conn.cursor()
     
                cur.execute(sql)
                data=cur.fetchall()
            except psycopg2.Error as err:
                    jsonify({'report': err})
            ## определение зоны для подсети на основе кода
            prefix=data[0][0]
            zona=answer['zona']
            sql='''SELECT region FROM resources.region where id=test'''
            sql=sql.replace('test',str(zona))
            try:
                cur = conn.cursor()
     
                cur.execute(sql)
                data= cur.fetchall()
            except psycopg2.Error as err:
                    jsonify({'report': err})

            region=data[0][0]
            ## формирование квоты подсети для добавления в базу MongoDB
            subnet={}
            subnet['subnets']=[]
            Subnet={}
            Subnet['region']=region
            Subnet['prefix_length']=prefix
            Subnet['type']='ipv4'
            Subnet['quantity']=1
            ## формирование запроса к системе биллинга
            value={}
            value['resource']='Selectel'
            value['task']='subnet'
            value['prefix']=prefix
            value['id']=answer['id']
            value=json.dumps(value)
            subnet['subnets'].append(Subnet)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r=requests.post('http://localhost:5500/bill',json=value)
            data=r.text
            responce=data.replace('\n','')
            data=json.loads(responce) 
            if data['report']=='Ok':
               ## добавление записи в базу MongoDB и создание подсети в Selectel
                project=mongo.db.projects.find_one({'name':answer['name']})
                if project is None:
                    return jsonify({'report': 'project not found'})
                try:
                 Sub=Selectel_api.Add_Subset(answer['name'],subnet)
                 try:
                    Subnet['cidr']=Sub[0]['cidr']
                    Subnet['id']=Sub[0]['id']
                    Subnet['status']=Sub[0]['status']
                 except:
                     return jsonify({'report': 'error'})
                 ## формирование запроса в системе биллинга для добавлени информации в базу
                 value={}
                 value['bill']=data['bill']
                 value['task']='subnet'
                 value['full']='subnet:'+json.dumps(Subnet)
                 value['name']=answer['name']
                 value['status']='buy'
                 value['id_services']=Subnet['id']
                 value['id_project']=project['id']
                 value['id_company']=answer['id']
                 value=json.dumps(value)
                 headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                 r=requests.post('http://localhost:5500/information',json=value)
                
                 data=r.text
                 responce=data.replace('\n','')
                 data=json.loads(responce) 
                except:
                    return jsonify({'report': 'error'})
                try:
                    project['subnet'].append(Subnet)
                except:

                    project['subnet']=[]
                    project['subnet'].append(Subnet)
                try:

               
                    mongo.db.projects.update({'name':project['name']},{'$set':{'subnet':project['subnet']}},multi=False)
                    
                    return jsonify({'report': 'create'})
                except:
                    return jsonify({'report': 'error'})
        ## метод для создания плавающего ip
        elif answer['task']=='floating_ip':
            conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
            try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
            except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
          
            ## Пример структуры для ip
            ip={
               
                "floatingips": [
                    {
                        "region": "ru-1",
                        "quantity": 4
                    }
                                ]
               }
            count=answer['count_ip']
           
            zona=answer['zona']
            sql='''SELECT region FROM resources.region where id=test'''
            sql=sql.replace('test',str(zona))
            try:
                cur = conn.cursor()
     
                cur.execute(sql)
                data= cur.fetchall()
            except psycopg2.Error as err:
                    jsonify({'report': err})
            ## формирование параметров для создания Ip
            region=data[0][0]
            floating={}
            floating['floatingips']=[]
            Floating={}
            Floating['region']=region
            
         
            Floating['quantity']=answer['count_ip']
            ## формирование запроса к системе биллинга для проверки баланса
            value={}
            value['resource']='Selectel'
            value['task']='floating_ip'
            value['count_ip']=answer['count_ip']
            value['id']=answer['id']
            value=json.dumps(value)
            floating['floatingips'].append(Floating)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r=requests.post('http://localhost:5500/bill',json=value)
            data=r.text
            responce=data.replace('\n','')
            data=json.loads(responce) 
            if data['report']=='Ok':
               ## добавление записи в базу данных MongoDB и создание ip  в Selectel
                project=mongo.db.projects.find_one({'name':answer['name']})
                if project is None:
                    return jsonify({'report': 'project not found'})
                try:
                    Sub=Selectel_api.Add_Ip(answer['name'],floating)
                    try:
                        Floating['id']=Sub['id']
                        Floating['floating_ip_address']=Sub['floating_ip_address']
                        Floating['status']=Sub['status']
                    except:
                         jsonify({'report': 'error'})
                    ## формирование запроса для записи в системе биллинга
                    value={}
                    value['bill']=data['bill']
                    value['task']='floating_ip'
                    value['full']='floating_ip:'+json.dumps(Floating)
                    value['name']=answer['name']
                    value['status']='buy'
                    value['id_services']=Floating['id']
                    value['id_project']=project['id']
                    value['id_company']=answer['id']
                    value=json.dumps(value)
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r=requests.post('http://localhost:5500/information',json=value)
                
                    data=r.text
                    responce=data.replace('\n','')
                    data=json.loads(responce) 
                    if data['report']=='Ok':
                        try:
                            project['floating_ip'].append(Floating)
                        except:

                            project['floating_ip']=[]
                            project['floating_ip'].append(Floating)
                        try:

               
                            mongo.db.projects.update({'name':project['name']},{'$set':{'floating_ip':project['floating_ip']}},multi=False)
                            return jsonify({'report': 'create'})
                        except:
                            return jsonify({'report': 'error'})
                except:
                    return jsonify({'report': 'error'})
                
            else:
                jsonify({'report': 'enough'})
        ## метод для удаления подсети
        elif answer['task']=='delete_sub':
            
            subnet=mongo.db.projects.find_one({'name':answer['name']})
            subnet=subnet['subnet']
            
            for sub in subnet:
                if sub['id']==answer['id_services']:
                    Sub=Selectel_api.Delete_Subset(sub)
                    subnet.remove(sub)
                    value={}
                 
                  
                   
               
                    value['id_services']=sub['id']
                    value['status']='delete'
                    value=json.dumps(value)
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r=requests.post('http://localhost:5500/information',json=value)
                
                    data=r.text
                    value=json.dumps(value)
                    break
            try:
                mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
                return jsonify({'report': 'delete'}) 
            except:
                return jsonify({'report': 'error'})
        ## метод для удаления ip
        elif answer['task']=='delete_ip':
            ## поиск ip в базе данных
            floating_ip=mongo.db.projects.find_one({'name':answer['name']})
            floating_ip=floating_ip['floating_ip']
            
            for ip in floating_ip:
               
                if ip['id']==answer['id_services']:
                   
                    Sub=Selectel_api.Delete_Ip(ip)
                    if Sub==-1:
                         floating_ip.remove(ip)
                         mongo.db.projects.update({'name':answer['name']},{'$set':{'floating_ip':floating_ip}},multi=False)
                         return jsonify({'report': 'not found'})
                    else:
                        floating_ip.remove(ip)
                    break
           
            try:
                mongo.db.projects.update({'name':answer['name']},{'$set':{'floating_ip':floating_ip}},multi=False)
                return jsonify({'report': 'delete'}) 
            except:
                return jsonify({'report': 'error'})
        elif answer['task']=='delete_sub':
            subnet=mongo.db.projects.find_one({'name':answer['name']})
            subnet=subnet['subnet']
            
            for sub in subnet:
               
                if sub['id']==answer['id_services']:
                   
                    Sub=Selectel_api.Delete_Subset(sub)
                    if Sub==-1:
                         subnet.remove(ip)
                         mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
                         return jsonify({'report': 'not found'})
                    else:
                        subnet.remove(ip)
                    break
           
            try:
                mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
                return jsonify({'report': 'delete'}) 
            except:
                return jsonify({'report': 'error'})
        ## метод для удаления проекта
        elif answer['task']=='delete_project':
            project=mongo.db.projects.find_one({'name':answer['name']})
           
     
               
                   
            Project=Selectel_api.Delete_Project(project)

            if Project!=-1:
                         project.remove(pj)
                         mongo.db.projects.delete_one({'name':pj['name']})
                         return jsonify({'report': 'not found'})
            else:
                        ## формирование запроса для
                         value={}
                         value['resource']='Selectel'
                         value['task']='delete_project'
                       
                         value['id_project']=project['id']
                         value=json.dumps(value)
                      
                         headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                         r=requests.post('http://localhost:5500/information',json=value)
                         data=r.text
                         responce=data.replace('\n','')
                         data=json.loads(responce) 
                         if data['report']=='Ok':
                            
                   
           
                            try:
                                mongo.db.projects.delete_one({'name':project['name']})
                                return jsonify({'report': 'delete'}) 
                            except:
                                return jsonify({'report': 'error'})
            
            


@app.route('/customers', methods=['POST'])
def create_customers():
    if not request.json:
        abort(400)
    print (request.json)
    answer=request.json
    customer={}
    if answer['task']=='create':
        customer['name']=answer['name']
        customer['password']=answer['password']
        customer['bill']=0
        customer['project']=[]
    

    customer=mongo.db.customers.insert(customer)
    return jsonify({'customer': 'create'})


## методы для работы с пользователями
@app.route('/user', methods=['POST'])
def users():

    if not request.json:
        abort(400)
    print (request.json)
    answer=request.json
    if answer['resource']=='Selectel':
        ## создание нового пользователя
        if answer['task']=='create':
            ## запрос в Selectel на создание
            user=Selectel_api.CreateUser(answer['name'],answer['password'])
            
            if user==-1:
                return jsonify({'user': 'error'})
            else:
                ## запись в базу MongoDB о том, что создан новый пользователь
                mongo.db.users.insert({'name':answer['name'],'id_user':user['id'],'id_company':answer['id'],'resource':answer['resource'],'enabled':'True'})
                return jsonify({'user': 'create'})
        ## метод для добавления пользователя в проект
        elif answer['task']=='add_project':
            name_project=answer['name_project']
            ## поиск проекта и пользователя в базе
            project=mongo.db.projects.find_one({"name":name_project})
            update_user=mongo.db.users.find_one({'name':answer['name']})
            if update_user is None:
                return jsonify({'user': 'not found user'})
          
           
            
            
            if project is not None:
                ## метод для добавления пользователя в проект
                user=Selectel_api.Add_user_in_project(project['id'],answer['name'])
                try:
                    users_project=user['project']
                except:
                    users_project=[]
                    users_project.append(project['id'])
             
                try:
                    if len(update_user['projects'])>0:
                        for p in update_user['projects']:
                            users_project.append(p)
                except:
                    d=0
                users_project.append(id)
                try:
                    update_user=mongo.db.users.update({'name':answer['name']},{'name':answer['name'],'id_company':answer['id_company'],'resource':answer['resource'],'enabled':'True','projects':users_project})
                except:
                    new_data=mongo.db.users.find_one({'name':answer['name']})

            else:
                return jsonify({'user': 'not found project'})
        ## метод для удаления пользователя 
        elif answer['task']=='delete_user':
            user=mongo.db.users.find_one({'name':answer['name']})
            if user is not None:
                try:
                    
                    answer=Selectel_api.DeleteUser(user['id_user'])
                    if answer==-1:
                        return jsonify({'user': 'not found user'})
                    mongo.db.users.delete_one({'name':user['name']})
                    return jsonify({'user': 'delete'})
                except:
                    return jsonify({'user': 'not found user'})
        ## метод для удаления пользователя из проекта
        elif answer['task']=='user_delete_from_project':
            user=mongo.db.users.find_one({'name':answer['name']})
            if user is not None:
                try:
                    
                    answer=Selectel_api.DeleteUser(user['id_user'])
                    if answer==-1:
                        return jsonify({'user': 'not found user'})
                    mongo.db.users.delete_one({'name':user['name']})
                    return jsonify({'user': 'delete'})
                except:
                    return jsonify({'user': 'not found user'})
                   
=======


from datetime import datetime
from flask import render_template
from flask import Flask, jsonify,request
from Selectel import app
import Selectel_api
import json
import requests
from flask_pymongo import PyMongo
import psycopg2

def Settings(file_path):
   
    file = file_path
    try:
     with open(file, 'r', encoding='utf8') as f:
        data = f.read()
    except:
         file = file_path

         with open(file, 'r', encoding='utf8') as f:
                data = f.read()
    data = data.split('\n')
    setting = {}
    setting['dbname']=data[0].replace('dbname:','').replace(' ','')
    setting['host'] = data[1].replace('host:', '').replace(' ', '')
    setting['user']=data[2].replace('user:','').replace(' ','')

    setting['password'] = data[3].replace('password:', '').replace(' ', '')
    return setting
## конфигурация базы данных MongoDB
app.config['MONGO_DBNAME'] = 'selectel'
app.config["MONGO_URI"] = "mongodb://localhost:27017/selectel"
mongo = PyMongo(app)
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]
@app.route('/')


## метод для работы с проектом
@app.route('/project', methods=['POST'])
def task_project():


    if not request.json:
        abort(400)
   ## print (request.json)
    answer=request.json
    ## декодруем json запрос
    value={}
    value['resource']=answer['resource']
     
    if answer['resource']=='Selectel':
        ## создание проекта
        if answer['task']=='create':
            ## подключение к базе данных
             conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
             try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
             except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
             qoutas={}
             ## поиск проекта с таким же именем
             project=mongo.db.projects.find({'name':answer['name']}).count()
             ## возвращает ошибку, если есть совпадение имен
             if project!=0:
                return jsonify({'project': 'already exist'})
            ## подставляем нужную зону в метод создания по коду из таблицы
             zona=answer['zona']
             sql='''SELECT region, "zone" FROM resources.region where id=test'''
             sql=sql.replace('test',str(zona))
             try:
                cur = conn.cursor()
     
                cur.execute(sql)
                data= cur.fetchall()
             except psycopg2.Error as err:
                    jsonify({'report': err})
            ## создаем словарь квот в нужном формате, на основе запроса пользователя
             qoutas['compute_cores']=[]
             comp=answer['quotas']['compute_cores']
             comp[0]['zone']=data[0][1]
             comp[0]['region']=data[0][0]
             qoutas['compute_cores']=comp
             try:
                comp=answer['quotas']['compute_ram']
                comp[0]['zone']=data[0][1]
                comp[0]['region']=data[0][0]
                qoutas['compute_ram']=comp
             except:
                 d=0
             try:
                comp=answer['quotas']['volume_gigabytes_universal']
                comp[0]['zone']=data[0][1]
                comp[0]['region']=data[0][0]
                qoutas['volume_gigabytes_universal']=comp
             except:
                 d=0
             try:
                comp=answer['quotas']['volume_gigabytes_fast']
                comp[0]['zone']=data[0][1]
                comp[0]['region']=data[0][0]
                qoutas['volume_gigabytes_fast']=comp
             except:
                 d=0
             try:
                comp=answer['qoutas']['volume_gigabytes_basic']
                comp[0]['zone']=data[0][1]
                comp[0]['region']=data[0][0]
                qoutas['volume_gigabytes_basic']=comp
             except:
                 d=0
              ## формирование запроса к системе биллинга для проверки баланса
             value['task']='bill'
             value['quotas']=qoutas
             value['id']=answer['id']
             value=json.dumps(value)
             
             headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
             r=requests.post('http://localhost:5500/bill',json=value)
             data=r.text
             responce=data.replace('\n','')
             data=json.loads(responce)
             if data['status']=='Ok':
                 ## создаем проект
                project=Selectel_api.CreateProject(answer['name'],qoutas)
                ## добавляем запись в MongoDB
                mongo.db.projects.insert({'name':project['name'],'id_company':answer['id'],'resource':answer['resource'],'id':project['id'],'url':project['url'],'enabled':project['enabled'],'quotas':project['quotas']})
                ## формируем запрос на запись информации о проекте в системе биллинга
                value={}
                value['resource']=answer['resource']
                value['task']='create_project'
                value['id_company']=answer['id']
                value['id_project']=project['id']
                value['bill']=data['bill']
                value['full']=project['quotas']
                value=json.dumps(value)
             
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r=requests.post('http://localhost:5500/information',json=value)
                data=r.text
                responce=data.replace('\n','')
                data=json.loads(responce)
                conn.close()
                ## формирование ответа на запрос
                if data['report']=='Ok':
                    return jsonify({'project': project['url']})
                elif data['report']=='error':
                    return jsonify({'project': 'error'})
           ## обработка запроса на обновление квот  
        elif answer['task']=='update':
             conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
             try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
             except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
             qoutas={}
             project=mongo.db.projects.find_one({'name':answer['name']})
             qoutas_now=project['quotas']
             
             if project==0:
                return jsonify({'project': 'project not find'})
             zona=answer['zona']
             sql='''SELECT region, "zone" FROM resources.region where id=test'''
             sql=sql.replace('test',str(zona))
             try:
                cur = conn.cursor()
     
                cur.execute(sql)
                data= cur.fetchall()
             except psycopg2.Error as err:
                    jsonify({'report': err})
             qoutas['compute_cores']=[]
             comp=qoutas_now['compute_cores']
             comp[0]['zone']=qoutas_now['compute_cores'][0]['zone']
             comp[0]['region']=qoutas_now['compute_cores'][0]['region']
             qoutas['compute_cores']=comp
             try:
                comp=qoutas_now['compute_ram']
                comp[0]['zone']=qoutas_now['compute_ram'][0]['zone']
                comp[0]['region']=qoutas_now['compute_ram'][0]['region']
                qoutas['compute_ram']=comp
             except:
                 d=0
             try:
                comp=qoutas_now['volume_gigabytes_universal']
                comp[0]['zone']=qoutas_now['volume_gigabytes_universal'][0]['zone']
                comp[0]['region']=qoutas_now['volume_gigabytes_universal'][0]['region']
                qoutas['volume_gigabytes_universal']=comp
             except:
                 d=0
             try:
                comp=qoutas_now['volume_gigabytes_fast']
                comp[0]['zone']=qoutas_now['volume_gigabytes_universal'][0]['zone']
                comp[0]['region']=qoutas_now['volume_gigabytes_universal'][0]['region']
                qoutas['volume_gigabytes_fast']=comp
             except:
                 d=0
             try:
                comp=qoutas_now['volume_gigabytes_basic']
                comp[0]['zone']=qoutas_now['volume_gigabytes_basic'][0]['zone']
                comp[0]['region']=qoutas_now['volume_gigabytes_basic'][0]['region']
                qoutas['volume_gigabytes_basic']=comp
             except:
                 d=0
             value['task']='bill'
             value['quotas']=qoutas
             value['id']=answer['id']
             value=json.dumps(value)
             
             headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
             project=Selectel_api.UpdateQoatas(answer['name'],qoutas)
          
             jsonify({'project': 'error'})
        ## запрос на удалениt проекта
        elif answer['task']=='delete':
            try:
            ## поиск проект по названию
              project=mongo.db.projects.find_one({'name':answer['name']})
              if project is not None:
                  ## удаление проекта из базы MongoDB и из Selectel
                answer=mongo.db.projects.delete_one({'name':answer['name']})
                Selectel_api.DeleteProject(project['id'])
                if answer.count()>0:
                    return jsonify({'project': 'delete'})
                else:
                   return jsonify({'project': 'not found'})
            except:
                return jsonify({'project': 'error'})
        ## добавление подсети в проект
        elif answer['task']=='subnet':
            setting=Settings('D://settings_selectel.txt')
            conn_string = "dbname=\'"+setting['dbname']+'" user=\'"' + setting['user'] + '\'' + " host=\'" + setting['host'] + '\'' + ' password=\'' + setting['password'] + '\''
            try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
            except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
          
            sub={
                "subnets": [
                    {
                         "region": "ru-1",
                         "quantity": 1,
                         "type": "ipv4",
                         "prefix_length": 29
                    }
                           ]
                }

            count=answer['count_ip']
            sql='''SELECT prefix FROM resources.prefix where count_ip=test1'''
            sql=sql.replace('test1',str(count))
            try:
                cur = conn.cursor()
     
                cur.execute(sql)
                data=cur.fetchall()
            except psycopg2.Error as err:
                    jsonify({'report': err})
            ## определение зоны для подсети на основе кода
            prefix=data[0][0]
            zona=answer['zona']
            sql='''SELECT region FROM resources.region where id=test'''
            sql=sql.replace('test',str(zona))
            try:
                cur = conn.cursor()
     
                cur.execute(sql)
                data= cur.fetchall()
            except psycopg2.Error as err:
                    jsonify({'report': err})

            region=data[0][0]
            ## формирование квоты подсети для добавления в базу MongoDB
            subnet={}
            subnet['subnets']=[]
            Subnet={}
            Subnet['region']=region
            Subnet['prefix_length']=prefix
            Subnet['type']='ipv4'
            Subnet['quantity']=1
            ## формирование запроса к системе биллинга
            value={}
            value['resource']='Selectel'
            value['task']='subnet'
            value['prefix']=prefix
            value['id']=answer['id']
            value=json.dumps(value)
            subnet['subnets'].append(Subnet)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r=requests.post('http://localhost:5500/bill',json=value)
            data=r.text
            responce=data.replace('\n','')
            data=json.loads(responce) 
            if data['report']=='Ok':
               ## добавление записи в базу MongoDB и создание подсети в Selectel
                project=mongo.db.projects.find_one({'name':answer['name']})
                if project is None:
                    return jsonify({'report': 'project not found'})
                try:
                 Sub=Selectel_api.Add_Subset(answer['name'],subnet)
                 try:
                    Subnet['cidr']=Sub[0]['cidr']
                    Subnet['id']=Sub[0]['id']
                    Subnet['status']=Sub[0]['status']
                 except:
                     return jsonify({'report': 'error'})
                 ## формирование запроса в системе биллинга для добавлени информации в базу
                 value={}
                 value['bill']=data['bill']
                 value['task']='subnet'
                 value['full']='subnet:'+json.dumps(Subnet)
                 value['name']=answer['name']
                 value['status']='buy'
                 value['id_services']=Subnet['id']
                 value['id_project']=project['id']
                 value['id_company']=answer['id']
                 value=json.dumps(value)
                 headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                 r=requests.post('http://localhost:5500/information',json=value)
                
                 data=r.text
                 responce=data.replace('\n','')
                 data=json.loads(responce) 
                except:
                    return jsonify({'report': 'error'})
                try:
                    project['subnet'].append(Subnet)
                except:

                    project['subnet']=[]
                    project['subnet'].append(Subnet)
                try:

               
                    mongo.db.projects.update({'name':project['name']},{'$set':{'subnet':project['subnet']}},multi=False)
                    
                    return jsonify({'report': 'create'})
                except:
                    return jsonify({'report': 'error'})
        ## метод для создания плавающего ip
        elif answer['task']=='floating_ip':
            conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
            try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
            except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
          
            ## Пример структуры для ip
            ip={
               
                "floatingips": [
                    {
                        "region": "ru-1",
                        "quantity": 4
                    }
                                ]
               }
            count=answer['count_ip']
           
            zona=answer['zona']
            sql='''SELECT region FROM resources.region where id=test'''
            sql=sql.replace('test',str(zona))
            try:
                cur = conn.cursor()
     
                cur.execute(sql)
                data= cur.fetchall()
            except psycopg2.Error as err:
                    jsonify({'report': err})
            ## формирование параметров для создания Ip
            region=data[0][0]
            floating={}
            floating['floatingips']=[]
            Floating={}
            Floating['region']=region
            
         
            Floating['quantity']=answer['count_ip']
            ## формирование запроса к системе биллинга для проверки баланса
            value={}
            value['resource']='Selectel'
            value['task']='floating_ip'
            value['count_ip']=answer['count_ip']
            value['id']=answer['id']
            value=json.dumps(value)
            floating['floatingips'].append(Floating)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r=requests.post('http://localhost:5500/bill',json=value)
            data=r.text
            responce=data.replace('\n','')
            data=json.loads(responce) 
            if data['report']=='Ok':
               ## добавление записи в базу данных MongoDB и создание ip  в Selectel
                project=mongo.db.projects.find_one({'name':answer['name']})
                if project is None:
                    return jsonify({'report': 'project not found'})
                try:
                    Sub=Selectel_api.Add_Ip(answer['name'],floating)
                    try:
                        Floating['id']=Sub['id']
                        Floating['floating_ip_address']=Sub['floating_ip_address']
                        Floating['status']=Sub['status']
                    except:
                         jsonify({'report': 'error'})
                    ## формирование запроса для записи в системе биллинга
                    value={}
                    value['bill']=data['bill']
                    value['task']='floating_ip'
                    value['full']='floating_ip:'+json.dumps(Floating)
                    value['name']=answer['name']
                    value['status']='buy'
                    value['id_services']=Floating['id']
                    value['id_project']=project['id']
                    value['id_company']=answer['id']
                    value=json.dumps(value)
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r=requests.post('http://localhost:5500/information',json=value)
                
                    data=r.text
                    responce=data.replace('\n','')
                    data=json.loads(responce) 
                    if data['report']=='Ok':
                        try:
                            project['floating_ip'].append(Floating)
                        except:

                            project['floating_ip']=[]
                            project['floating_ip'].append(Floating)
                        try:

               
                            mongo.db.projects.update({'name':project['name']},{'$set':{'floating_ip':project['floating_ip']}},multi=False)
                            return jsonify({'report': 'create'})
                        except:
                            return jsonify({'report': 'error'})
                except:
                    return jsonify({'report': 'error'})
                
            else:
                jsonify({'report': 'enough'})
        ## метод для удаления подсети
        elif answer['task']=='delete_sub':
            
            subnet=mongo.db.projects.find_one({'name':answer['name']})
            subnet=subnet['subnet']
            
            for sub in subnet:
                if sub['id']==answer['id_services']:
                    Sub=Selectel_api.Delete_Subset(sub)
                    subnet.remove(sub)
                    value={}
                 
                  
                   
               
                    value['id_services']=sub['id']
                    value['status']='delete'
                    value=json.dumps(value)
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r=requests.post('http://localhost:5500/information',json=value)
                
                    data=r.text
                    value=json.dumps(value)
                    break
            try:
                mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
                return jsonify({'report': 'delete'}) 
            except:
                return jsonify({'report': 'error'})
        ## метод для удаления ip
        elif answer['task']=='delete_ip':
            ## поиск ip в базе данных
            floating_ip=mongo.db.projects.find_one({'name':answer['name']})
            floating_ip=floating_ip['floating_ip']
            
            for ip in floating_ip:
               
                if ip['id']==answer['id_services']:
                   
                    Sub=Selectel_api.Delete_Ip(ip)
                    if Sub==-1:
                         floating_ip.remove(ip)
                         mongo.db.projects.update({'name':answer['name']},{'$set':{'floating_ip':floating_ip}},multi=False)
                         return jsonify({'report': 'not found'})
                    else:
                        floating_ip.remove(ip)
                    break
           
            try:
                mongo.db.projects.update({'name':answer['name']},{'$set':{'floating_ip':floating_ip}},multi=False)
                return jsonify({'report': 'delete'}) 
            except:
                return jsonify({'report': 'error'})
        elif answer['task']=='delete_sub':
            subnet=mongo.db.projects.find_one({'name':answer['name']})
            subnet=subnet['subnet']
            
            for sub in subnet:
               
                if sub['id']==answer['id_services']:
                   
                    Sub=Selectel_api.Delete_Subset(sub)
                    if Sub==-1:
                         subnet.remove(ip)
                         mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
                         return jsonify({'report': 'not found'})
                    else:
                        subnet.remove(ip)
                    break
           
            try:
                mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
                return jsonify({'report': 'delete'}) 
            except:
                return jsonify({'report': 'error'})
        ## метод для удаления проекта
        elif answer['task']=='delete_project':
            project=mongo.db.projects.find_one({'name':answer['name']})
           
     
               
                   
            Project=Selectel_api.Delete_Project(project)

            if Project!=-1:
                         project.remove(pj)
                         mongo.db.projects.delete_one({'name':pj['name']})
                         return jsonify({'report': 'not found'})
            else:
                        ## формирование запроса для
                         value={}
                         value['resource']='Selectel'
                         value['task']='delete_project'
                       
                         value['id_project']=project['id']
                         value=json.dumps(value)
                      
                         headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                         r=requests.post('http://localhost:5500/information',json=value)
                         data=r.text
                         responce=data.replace('\n','')
                         data=json.loads(responce) 
                         if data['report']=='Ok':
                            
                   
           
                            try:
                                mongo.db.projects.delete_one({'name':project['name']})
                                return jsonify({'report': 'delete'}) 
                            except:
                                return jsonify({'report': 'error'})
            
            


@app.route('/customers', methods=['POST'])
def create_customers():
    if not request.json:
        abort(400)
    print (request.json)
    answer=request.json
    customer={}
    if answer['task']=='create':
        customer['name']=answer['name']
        customer['password']=answer['password']
        customer['bill']=0
        customer['project']=[]
    

    customer=mongo.db.customers.insert(customer)
    return jsonify({'customer': 'create'})


## методы для работы с пользователями
@app.route('/user', methods=['POST'])
def users():

    if not request.json:
        abort(400)
    print (request.json)
    answer=request.json
    if answer['resource']=='Selectel':
        ## создание нового пользователя
        if answer['task']=='create':
            ## запрос в Selectel на создание
            user=Selectel_api.CreateUser(answer['name'],answer['password'])
            
            if user==-1:
                return jsonify({'user': 'error'})
            else:
                ## запись в базу MongoDB о том, что создан новый пользователь
                mongo.db.users.insert({'name':answer['name'],'id_user':user['id'],'id_company':answer['id'],'resource':answer['resource'],'enabled':'True'})
                return jsonify({'user': 'create'})
        ## метод для добавления пользователя в проект
        elif answer['task']=='add_project':
            name_project=answer['name_project']
            ## поиск проекта и пользователя в базе
            project=mongo.db.projects.find_one({"name":name_project})
            update_user=mongo.db.users.find_one({'name':answer['name']})
            if update_user is None:
                return jsonify({'user': 'not found user'})
          
           
            
            
            if project is not None:
                ## метод для добавления пользователя в проект
                user=Selectel_api.Add_user_in_project(project['id'],answer['name'])
                try:
                    users_project=user['project']
                except:
                    users_project=[]
                    users_project.append(project['id'])
             
                try:
                    if len(update_user['projects'])>0:
                        for p in update_user['projects']:
                            users_project.append(p)
                except:
                    d=0
                users_project.append(id)
                try:
                    update_user=mongo.db.users.update({'name':answer['name']},{'name':answer['name'],'id_company':answer['id_company'],'resource':answer['resource'],'enabled':'True','projects':users_project})
                except:
                    new_data=mongo.db.users.find_one({'name':answer['name']})

            else:
                return jsonify({'user': 'not found project'})
        ## метод для удаления пользователя 
        elif answer['task']=='delete_user':
            user=mongo.db.users.find_one({'name':answer['name']})
            if user is not None:
                try:
                    
                    answer=Selectel_api.DeleteUser(user['id_user'])
                    if answer==-1:
                        return jsonify({'user': 'not found user'})
                    mongo.db.users.delete_one({'name':user['name']})
                    return jsonify({'user': 'delete'})
                except:
                    return jsonify({'user': 'not found user'})
        ## метод для удаления пользователя из проекта
        elif answer['task']=='user_delete_from_project':
            user=mongo.db.users.find_one({'name':answer['name']})
            if user is not None:
                try:
                    
                    answer=Selectel_api.DeleteUser(user['id_user'])
                    if answer==-1:
                        return jsonify({'user': 'not found user'})
                    mongo.db.users.delete_one({'name':user['name']})
                    return jsonify({'user': 'delete'})
                except:
                    return jsonify({'user': 'not found user'})
                   
>>>>>>> 32b0634e1288189bfd588c1ab891b13786d783ae
