<<<<<<< HEAD
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import Flask, jsonify,request
from Selectel import app
import Selectel_api
import json
import requests
from flask_pymongo import PyMongo
import psycopg2

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



@app.route('/project', methods=['POST'])
def get_tasks():


    if not request.json:
        abort(400)
    print (request.json)
    answer=request.json
   
    value={}
    value['resource']=answer['resource']
     
    if answer['resource']=='Selectel':
        if answer['task']=='create':
             conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
             try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
             except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
             qoutas={}
             project=mongo.db.projects.find({'name':answer['name']}).count()
             if project!=0:
                return jsonify({'project': 'already exist'})
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
               ## project=Selectel_api.CreateProject(answer['name'],qoutas)
                mongo.db.projects.insert({'name':project['name'],'id_company':answer['id'],'resource':answer['resource'],'id':project['id'],'url':project['url'],'enabled':project['enabled'],'quotas':project['quotas']})
                value={}
                value['resource']=answer['resource']
                value['task']='create'
                value['id_company']=answer['id']
                value['id_project']=project['id']
                value['bill']=data['bill']
                value=json.dumps(value)
             
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r=requests.post('http://localhost:5500/bill',json=value)
                data=r.text
                responce=data.replace('\n','')
                data=json.loads(responce)
                conn.close()
                if data['report']=='Ok':
                    return jsonify({'project': 'create'})
                elif data['report']=='error':
                    return jsonify({'project': 'error'})
             
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
        elif answer['task']=='delete':
            try:
              project=mongo.db.projects.find_one({'name':answer['name']})
              if project is not None:
                answer=mongo.db.projects.delete_one({'name':answer['name']})
                Selectel_api.DeleteProject(project['id'])
                if answer.delete_count>0:
                    return jsonify({'project': 'delete'})
                else:
                   return jsonify({'project': 'not found'})
            except:
                return jsonify({'project': 'error'})
        elif answer['task']=='subnet':
            conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
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
            subnet={}
            subnet['subnets']=[]
            Subnet={}
            Subnet['region']=region
            Subnet['prefix_length']=prefix
            Subnet['type']='ipv4'
            Subnet['quantity']=1
            
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
               ## Subnet=Selectel_api.Add_Subset(answer['name'],subnet)
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
        elif answer['task']=='floating_ip':
            conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
            try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
            except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
          
            
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

            region=data[0][0]
            floating={}
            floating['floatingips']=[]
            Floating={}
            Floating['region']=region
            
         
            Floating['quantity']=answer['count_ip']
            
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
               ## Subnet=Selectel_api.Add_Subset(answer['name'],subnet)
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
        elif answer['task']=='delete_sub':
            
            subnet=mongo.db.projects.find_one({'name':answer['name']})
            subnet=subnet['subnet']
            ##subnet.remove(subnet[0])
            ##mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
            for sub in subnet:
                if sub['id']==answer['id_services']:
                    Sub=Selectel_api.Delete_Subset(sub)
                    subnet.remove(sub)
                    break
            try:
                mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
                return jsonify({'report': 'delete'}) 
            except:
                return jsonify({'report': 'error'})
        elif answer['task']=='delete_ip':
            floating_ip=mongo.db.projects.find_one({'name':answer['name']})
            floating_ip=floating_ip['floating_ip']
            ##subnet.remove(subnet[0])
            ##mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
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
            ##subnet.remove(subnet[0])
            ##mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
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
        elif answer['task']=='delete_project':
            project=mongo.db.projects.find_one({'name':answer['name']})
           
            for pj in subnet:
               
                if pj['id']==project['id']:
                   
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



@app.route('/user', methods=['POST'])
def users():

    if not request.json:
        abort(400)
    print (request.json)
    answer=request.json
    if answer['resource']=='Selectel':
        if answer['task']=='create':
            
            user=Selectel_api.CreateUser(answer['name'],answer['password'])
            
            if user==-1:
                return jsonify({'user': 'error'})
            else:
                mongo.db.users.insert({'name':answer['name'],'id_company':answer['id'],'resource':answer['resource'],'enabled':'True'})
                return jsonify({'user': 'create'})
        elif answer['task']=='add_project':
            name_project=answer['name_project']
            id=mongo.db.projects.find_one({"name":name_project})
            update_user=mongo.db.users.find_one({'name':answer['name']})
            if update_user is None:
                return jsonify({'user': 'not found user'})
            id=id['id']
           
            
            
            if id is not None:
                
                user=Selectel_api.Add_user_in_project(id,answer['name'])
                update_user=mongo.db.users.find_one({'name':answer['name']})
                users_project=[]
             
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
         


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
=======
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import Flask, jsonify,request
from Selectel import app
import Selectel_api
import json
import requests
from flask_pymongo import PyMongo
import psycopg2

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



@app.route('/project', methods=['POST'])
def get_tasks():


    if not request.json:
        abort(400)
    print (request.json)
    answer=request.json
   
    value={}
    value['resource']=answer['resource']
     
    if answer['resource']=='Selectel':
        if answer['task']=='create':
             conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
             try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
             except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
             qoutas={}
             project=mongo.db.projects.find({'name':answer['name']}).count()
             if project!=0:
                return jsonify({'project': 'already exist'})
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
               ## project=Selectel_api.CreateProject(answer['name'],qoutas)
                mongo.db.projects.insert({'name':project['name'],'id_company':answer['id'],'resource':answer['resource'],'id':project['id'],'url':project['url'],'enabled':project['enabled'],'quotas':project['quotas']})
                value={}
                value['resource']=answer['resource']
                value['task']='create'
                value['id_company']=answer['id']
                value['id_project']=project['id']
                value['bill']=data['bill']
                value=json.dumps(value)
             
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r=requests.post('http://localhost:5500/bill',json=value)
                data=r.text
                responce=data.replace('\n','')
                data=json.loads(responce)
                conn.close()
                if data['report']=='Ok':
                    return jsonify({'project': 'create'})
                elif data['report']=='error':
                    return jsonify({'project': 'error'})
             
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
        elif answer['task']=='delete':
            try:
              project=mongo.db.projects.find_one({'name':answer['name']})
              if project is not None:
                answer=mongo.db.projects.delete_one({'name':answer['name']})
                Selectel_api.DeleteProject(project['id'])
                if answer.delete_count>0:
                    return jsonify({'project': 'delete'})
                else:
                   return jsonify({'project': 'not found'})
            except:
                return jsonify({'project': 'error'})
        elif answer['task']=='subnet':
            conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
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
            subnet={}
            subnet['subnets']=[]
            Subnet={}
            Subnet['region']=region
            Subnet['prefix_length']=prefix
            Subnet['type']='ipv4'
            Subnet['quantity']=1
            
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
               ## Subnet=Selectel_api.Add_Subset(answer['name'],subnet)
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
        elif answer['task']=='floating_ip':
            conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
            try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
            except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
          
            
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

            region=data[0][0]
            floating={}
            floating['floatingips']=[]
            Floating={}
            Floating['region']=region
            
         
            Floating['quantity']=answer['count_ip']
            
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
               ## Subnet=Selectel_api.Add_Subset(answer['name'],subnet)
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
        elif answer['task']=='delete_sub':
            
            subnet=mongo.db.projects.find_one({'name':answer['name']})
            subnet=subnet['subnet']
            ##subnet.remove(subnet[0])
            ##mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
            for sub in subnet:
                if sub['id']==answer['id_services']:
                    Sub=Selectel_api.Delete_Subset(sub)
                    subnet.remove(sub)
                    break
            try:
                mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
                return jsonify({'report': 'delete'}) 
            except:
                return jsonify({'report': 'error'})
        elif answer['task']=='delete_ip':
            floating_ip=mongo.db.projects.find_one({'name':answer['name']})
            floating_ip=floating_ip['floating_ip']
            ##subnet.remove(subnet[0])
            ##mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
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
            ##subnet.remove(subnet[0])
            ##mongo.db.projects.update({'name':answer['name']},{'$set':{'subnet':subnet}},multi=False)
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
        elif answer['task']=='delete_project':
            project=mongo.db.projects.find_one({'name':answer['name']})
           
            for pj in subnet:
               
                if pj['id']==project['id']:
                   
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



@app.route('/user', methods=['POST'])
def users():

    if not request.json:
        abort(400)
    print (request.json)
    answer=request.json
    if answer['resource']=='Selectel':
        if answer['task']=='create':
            
            user=Selectel_api.CreateUser(answer['name'],answer['password'])
            
            if user==-1:
                return jsonify({'user': 'error'})
            else:
                mongo.db.users.insert({'name':answer['name'],'id_company':answer['id'],'resource':answer['resource'],'enabled':'True'})
                return jsonify({'user': 'create'})
        elif answer['task']=='add_project':
            name_project=answer['name_project']
            id=mongo.db.projects.find_one({"name":name_project})
            update_user=mongo.db.users.find_one({'name':answer['name']})
            if update_user is None:
                return jsonify({'user': 'not found user'})
            id=id['id']
           
            
            
            if id is not None:
                
                user=Selectel_api.Add_user_in_project(id,answer['name'])
                update_user=mongo.db.users.find_one({'name':answer['name']})
                users_project=[]
             
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
         


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
>>>>>>> 26930c4ad8cdd2ff3fd0e989b3c4c206e9b0fedf
