"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import Flask, jsonify,request
from Selectel import app
import Selectel_api
import json
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
    if answer['resource']=='Selectel':
        if answer['task']=='create':
            project=Selectel_api.CreateProject(answer['name'],answer['quotas'])
            return jsonify({'project': project})
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
                return -1
            else:
                return 1
         


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
