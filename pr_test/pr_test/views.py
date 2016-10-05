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


class appbild:
    log=None
    session=None
    def test(self,session,request):
        self.log=Strategy_data()
        self.session=session
        flag=True
        if(request.form.get('start')!=None):
            flag=False
            session['User']=request.form['start']
        if session.get('User')==None:
            abort(404)
        else:
            self.log.logic(session['User'])
        return flag
    def add_session(self,session):
        self.session=session
        self.log=Strategy_data()
        if session.get('User')==None:
            abort(404)
        else:
            self.log.logic(session['User'])
    def start(self,session):
        session.clear()
        self.log=Strategy_data()
        inf=(['start'],'Имя введите')
        resp=make_response(render_template(
                'index.html',
                title='Home Page',
                year=datetime.now().year,
                data = None,
                labls_name=inf[1],
                form=inf[0],
                labls=self.log.label()
            )
        )
        return resp
    def add_Node(self,request):
            db_inf= self.log.create(request.form)
            resp=make_response( render_template(
                    'index.html',
                    title=self.session['User'],
                    year=datetime.now().year,
                    data = db_inf,
                    form= self.log.information()[0],
                    labls_name= self.log.information()[1],
                    labls=self.log.label()
                )
            )
            return resp
    def choice_Node(self):
        resp=make_response( render_template(
                    'index.html',
                    title=self.session['User'],
                    year=datetime.now().year,
                    data = None,
                    form= self.log.information()[0],
                    labls_name= self.log.information()[1],
                    labls=self.log.label()
                )
        )
        return resp
    def choice_rel(self):
        return render_template(
            'Add_relationship.html',
            title=self.session['User'],
            year=datetime.now().year,
            message='Your application description page.',
            labls_name='start',
            form=['start'],
            inmr=self.log.information_E(),
            error=self.log.error
        )
    def add_rel(self,request):
        inf=['start']
        data=['sss']
        try:
            inf=self.log.information_E()[0][request.form['start']][0]
            data=self.log.MATCH_rel(self.session,request)
        except:
            data=self.log.create_E(request.form)
        finally:             
            return render_template(
                'Add_relationship.html',
                title=self.session['User'],
                year=datetime.now().year,
                message='Your application description page.',
                labls_name='start',  
                inmr=data,          
                form=inf,
                error=self.log.error

            )
    def choice_update_node(self):
            return render_template(
                'update_node.html',
                title='choice_update_node',
                year= self.session['User'],
                message='Your contact page.',
                MODEL=self.log.match_model(0,0),
                form=['id','name','data'],
                error=self.log.error
            )
    def use_update_node(self,request):
            self.log.update_N(request.form['id'],request.form['name'],request.form['data']  )
            return render_template(
                'update_node.html',
                title='use_update_node',
                year= self.session['User'],
                message='Your contact page.',
                MODEL=self.log.match_model(0,0)  ,
                form=['id','name','data'],
                error=self.log.error
            )
    def choice_update_rel(self):
            return render_template(
                'update_rel.html',
                title='Contact',
                year= self.session['User'],
                message='Your contact page.',
                MODEL=self.log.match_model(0,0),
                form=['id'],
                error=self.log.error
            )
    def use_update_rel(self,request):
        data_MODEL=None
        try:
            id=request.form['id'];name=request.form['name'];data=request.form['data']
            self.log.update_E(id,name,data)
            data_MODEL=self.log.MATCH_relationship(id)
        except:
            data_MODEL=self.log.MATCH_rel_id(request.form['id'])
        finally:
            return render_template(
                    'update_rel.html',
                    title=self.session['User'],
                    year=datetime.now().year,
                    message='Your application description page.',
                    form=['id','name','data'],
                    MODEL=data_MODEL,
                    error=self.log.error
                    )
    def choice_delete_node(self):
            return render_template(
                'del.html',
                title='Contact',
                year= self.session['User'],
                message='Your contact page.',
                MODEL=self.log.match_model(0,0),
                form=['id'],
                error=self.log.error
            )
    def use_delete_node(self,request):
            self.log.DELETE_N(request.form['id'])
            match_data=self.log.match_model(0,0)    
            return render_template(
                'del.html',
                title='Contact',
                year= self.session['User'],
                message='Your contact page.',
                MODEL=self.log.match_model(0,0)    ,
                form=['id'],
                error=self.log.error
            )
    def choice_delete_rel(self):
            return render_template(
                'del_rel.html',
                title='Contact',
                year= self.session['User'],
                message='Your contact page.',
                MODEL=self.log.match_model(0,0),
                form=['id'],
                error=self.log.error
            )
    def use_delete_rel(self,request):
        self.log.DELETE_E(request.form['id'])
        data_MODEL=self.log.MATCH_rel_id(request.form['id'])
        return render_template(
                'del_rel.html',
                title='Contact',
                year= self.session['User'],
                message='Your contact page.',
                MODEL=data_MODEL,
                form=['id'],
                error=self.log.error
            )
    def choice_match(self):
        return render_template(
                'match.html',
                title=self.session['User'],
                year=datetime.now().year,
                message='Your application description page.',
                form=['id'],
                MODEL=self.log.match_model(0,0),
                M=None
        )
    def use_match(self,request):
          data_MODEL=self.log.MATCH_rel_id(request.form['id'])
          data_M=self.log.data.departament(request.form['id'])
          return render_template(
                'match.html',
                title=self.session['User'],
                year=datetime.now().year,
                message='Your application description page.',
                form=['id'],
                MODEL=data_MODEL,
                M=data_M
        )
        
@app.route('/')
def start():        
        return appbild().start(session)

@app.route('/home/',methods=['POST', 'GET'])
def home():
    appb=appbild()
    test=appb.test(session,request)
    if request.method=='POST' and test:
            return appb.add_Node(request)
    else:
            return appb.choice_Node()

@app.route('/update_node/',methods=['POST', 'GET'])
def update_node():
    appb=appbild()
    appb.add_session(session)    
    if request.method=='POST':
            return appb.use_update_node(request)
    else:
            return appb.choice_update_node()
@app.route('/delete/',methods=['POST', 'GET'])
def delete():
    """Renders the contact page."""
    appb=appbild()
    appb.add_session(session)    
    if request.method=='POST':
        return appb.use_delete_node(request)
    else:
        return appb.choice_delete_node()
@app.route('/Add_relationship/',methods=['POST', 'GET'])
def Add_relationship():
    appb=appbild()
    appb.add_session(session)
    if request.method=='POST':         
            return appb.add_rel(request)
    else:
            return appb.choice_rel()

@app.route('/match/',methods=['POST', 'GET'])
def match():
    appb=appbild()
    appb.add_session(session)
    if request.method=='POST': 
        return appb.use_match(request)
    else:
        return appb.choice_match()
@app.route('/update_rel/',methods=['POST', 'GET'])
def update_rel():
    appb=appbild()
    appb.add_session(session)
    if request.method=='POST': 
        return appb.use_update_rel(request)
    else:
        return appb.choice_update_rel()

@app.route('/del_rel/',methods=['POST', 'GET'])
def del_rel():
    appb=appbild()
    appb.add_session(session)
    if request.method=='POST': 
        return appb.use_delete_rel(request)
    else:
        return appb.choice_delete_rel()