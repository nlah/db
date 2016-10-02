"""
Routes and views for the flask application.
"""
import sys
from datetime import datetime
from flask import render_template,make_response,session,abort
from flask.json import JSONEncoder
from pr_test import app
from flask import request
sys.path.append(".\pr_test")
from model_vr import *
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, fasad):
            # Implement code to convert Passport object to a dict
            return passport_dict
        else:
            JSONEncoder.default(self, obj)

# Now tell Flask to use the custom class
app.json_encoder = CustomJSONEncoder




@app.route('/')
def start():
        session.clear()
        log=Strategy_data()
        inf=(['start'],'Имя ввидети')
        resp=make_response(render_template(
                'index.html',
                title='Home Page',
                year=datetime.now().year,
                data = None,
                labls_name=inf[1],
                form=inf[0],
                labls=log.label()
            )
        )
        return resp

@app.route('/home/',methods=['POST', 'GET'])
def home():
    log=Strategy_data()
    db_inf=None
    flag=True
    if(request.form.get('start')!=None):
        flag=False
        session['User']=request.form['start']
    if session.get('User')==None:
        abort(404)
    else:
        log.logic(session['User'])
    if request.method=='POST' and flag:
            db_inf= log.create(request.form)
            resp=make_response( render_template(
                    'index.html',
                    title='Home Page',
                    year=datetime.now().year,
                    data = db_inf,
                    form= log.information()[0],
                    labls_name= log.information()[1],
                    labls=log.label()
                )
            )
            return resp
            """Renders the home page."""
    else:
        resp=make_response( render_template(
                    'index.html',
                    title='Home Page',
                    year=datetime.now().year,
                    data = db_inf,
                    form= log.information()[0],
                    labls_name= log.information()[1],
                    labls=log.label()
                )
        )
        return resp

@app.route('/contact/',methods=['POST', 'GET'])
def contact():
    """Renders the contact page."""
    log=Strategy_data()
    if session.get('User')==None:
        abort(404)
    else:
        log.logic(session['User'])
    match_data=log.match_model(0,0)    
    data=['id','name','data']
    if request.method=='POST':
            log.update_N(request.form['id'],request.form['name'],request.form['data']  )
            match_data=log.match_model(0,0)    
            return render_template(
                'contact.html',
                title='Contact',
                year= session['User'],
                message='Your contact page.',
                MODEL=match_data,
                form=data,
                error=log.error
            )
    else:
            return render_template(
                'contact.html',
                title='Contact',
                year= session['User'],
                message='Your contact page.',
                MODEL=match_data,
                form=data,
                error=log.error
            )
@app.route('/delete/',methods=['POST', 'GET'])
def delete():
    """Renders the contact page."""
    log=Strategy_data()
    if session.get('User')==None:
       abort(404)
    else:
        log.logic(session['User'])
    match_data=log.match_model(0,0)    
    data=['id']
    if request.method=='POST':
            log.DELETE_N(request.form['id'])
            return render_template(
                'del.html',
                title='Contact',
                year= session['User'],
                message='Your contact page.',
                MODEL=match_data,
                form=data,
                error=log.error
            )
    else:
            return render_template(
                'del.html',
                title='Contact',
                year= session['User'],
                message='Your contact page.',
                MODEL=match_data,
                form=data,
                error=log.error
            )
@app.route('/about/',methods=['POST', 'GET'])
def about():
    log=Strategy_data()
    inf=['start']
    data=None
    if session.get('User')==None:
        abort(404)
    else:
        log.logic(session['User'])
    """Renders the about page."""

    if request.method=='POST':
        try:
            inf=log.information_E()[0][request.form['start']][0]
            data=( log.MATCH_rel(session['User'],log.information_E()[0][request.form['start']][1]),
            log.MATCH_rel(request.form['start'],None),Strategy_data.id_get_query( log.MATCH_rel(request.form['start'],None)))
        except:
            data=log.create_E(request.form)
        finally:             
            return render_template(
                'about.html',
                title=session['User'],
                year=datetime.now().year,
                message='Your application description page.',
                labls_name='start',  
                inmr=data,          
                form=inf
            )
    else:
        return render_template(
            'about.html',
            title=session['User'],
            year=datetime.now().year,
            message='Your application description page.',
            labls_name='start',
            form=inf,
            inmr=log.information_E()
        )

@app.route('/match/',methods=['POST', 'GET'])
def match():
    log=Strategy_data()
    if session.get('User')==None:
        abort(404)
    else:
        log.logic(session['User'])

    if request.method=='POST': 
          data_MODEL=log.MATCH_rel_id(request.form['id'])
          data_M=log.data.departament(request.form['id'])
          return render_template(
                'match.html',
                title=session['User'],
                year=datetime.now().year,
                message='Your application description page.',
                form=['id'],
                MODEL=data_MODEL,
                M=data_M
        )
    else:
        return render_template(
                'match.html',
                title=session['User'],
                year=datetime.now().year,
                message='Your application description page.',
                form=['id'],
                MODEL=log.match_model(0,0),
                M=None
        )