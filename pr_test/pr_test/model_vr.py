from neo4j.v1 import GraphDatabase, basic_auth ,CypherError
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
class MODEL_data:
    __metaclass__ = Singleton
    __save=[]   
    error=[]
    def __init__(self):
        self.__driver=GraphDatabase.driver('bolt://localhost:7687', auth=basic_auth("neo4j", "qwe3809696"),encrypted=False)
    def _add_CREATE(self,query):
       self.__save.append(query)
    def save(self):
       # funcT=(lambda RUN: lambda y: (list(RUN(y))))
        def func(F):
            data=[]
            for i in self.__save:
                 data.append(list(F(i))) 
            return data
        #func= (lambda funcT:lambda run: map(funcT(run),self.__save))(lambda RUN: lambda y: (list(RUN(y))))
        T=self._save(func)
        self.__save.clear()
        return T;
       # self.__save((lambda x: map( result=tx.run(i); result = list(result);Test.append(result)))
        
    def _save(self,func):
        Test=None
        session = self.__driver.session()
        tx= session.begin_transaction()
        try:
                Test=func(tx.run)
                tx.commit()
        except CypherError as a:
                self.error.append(a.message)
                tx.rollback()
                session.close()
                Test= None
        finally:
                 session.close()
                 return Test                      
    def query(self,query):
        session = self.__driver.session()
        data=None
        try:
            data=list(session.run(query))
            session.close()
            return data
        except CypherError as a:
            self.error.append(a.message)
            session.close()
            return None

    def _match(self,leble:str,i:int,j:int):
        if(i==0 and j==0):
            return self.query('MATCH (n:'+leble+') return n')
        else:
            return self.query('MATCH (n:'+leble+')-[*'+str(i)+'..'+str(j)+']-(m) return m')
     
    def res(self):
        self._add_CREATE('MATCH (n) DETACH DELETE n')
        self.save()
        #session = self.__driver.session()
        #session.run('create CONSTRAINT ON (n:department) ASSERT n.name IS UNIQUE')
        #session.run('create CONSTRAINT ON (n:undepartment) ASSERT n.name IS UNIQUE')
        #session.close()
    def update_N(self,id,name,data):
       self._add_CREATE('MATCH (n) WHERE id(n)='+str(id)+' SET n.'+name+'=\''+data+'\'')
       self.save()
    def update_E(self,id,name,data):
       self._add_CREATE('MATCH ()-[n]-() WHERE id(n)='+str(id)+' SET n.'+name+'=\''+data+'\'')
       self.save()
    def DELETE_N(self,id):
       self._add_CREATE('MATCH (n) WHERE id(n)='+str(id)+' DETACH DELETE n')
       self.save()
    def DELETE_E(self,id):
       self._add_CREATE('MATCH ()-[n]-() WHERE id(n)='+str(id)+'  DELETE n')
       self.save()
    def MATCH_rel_id(self,id):
        return self.query('MATCH (a)-[r]-(n) WHERE id(a)='+str(id)+' return r,n')
    def MATCH_node_id(self,id):
               self._add_CREATE('MATCH (n) WHERE id(n)='+str(id)+'  return n')
    def MATCH_rel(self,lable,rel):
        return self.query('MATCH (a:'+lable+')-[r:'+rel+']-(n) return r,n')     
    def MATCH_relationship(self,id):
        return self.query('MATCH ()-[r]-() WHERE id(r)='+str(id)+' return r')        
    def labels_name(self):
        return ['department','undepartment','Group','employee','subject','lecture_hall','student']
    @staticmethod
    def id_get_Create(a):
        id=[]
        if a is None:
            return None
        else:
            for i in a:
                id.append(i[0][i[0].keys()[0]].id)
            return id
    @staticmethod    
    def id_get_query(a):
        id=[]
        if a is None:
            return None
        else:
            for i in a:
                id.append(i[i.keys()[0]].id)
            return id
class department(MODEL_data):
        __metaclass__ = Singleton
        def Create_arr(self,inf):
                self._add_CREATE('MERGE  (a:department{name:\''+inf['name']+'\',data:\''+inf['data']+'\'}) return a')
                return self.save()
       
        def Create(self,name,data):
              list(map(lambda x,y:self._add_CREATE('CREATE (a:department{name:\''+x+'\',data:\''+y+'\'}) return a'),name,data))
              return self.save()
        def MATCH(self,i,j,test=False):
            return self._match('department',i,j)
        def MATCH_A(self,name):
            return self.query('MATCH (n:department{name:\''+name+'\'}) return n')
        def departament(self,id):
            return self.query('match (n:department) where  id(n)='+str(id)+' return m')
        def information(self):
            return( ['name','data'],'department')
        def information_E(self):
            return ({},'department')
class undepartment(MODEL_data):
        __metaclass__ = Singleton
        def Create_arr(self,inf):
                self._add_CREATE('MERGE  (a:undepartment{name:\''+inf['name']+'\',data:\''+inf['data']+'\'}) return a')
                return self.save()
        def Create(self,name,data):
              list(map(lambda x,y:self._add_CREATE('CREATE (a:undepartment{name:\''+x+'\',data:\''+y+'\'}) return a'),name,data))
              return self.save()
        def Create_department(self,undepartmentid,departmentid):
              self._add_CREATE('MATCH (a:department),(b:undepartment) WHERE id(a)='+str(departmentid)+' AND id(b)='+str(undepartmentid)+' and not EXISTS((b)-[:un]-())   WITH a,b  CREATE (b)-[r:un]->(a) return r')    
              return self.save()
        def Crate_E(self,data):
            if(data.get('undepartment')!=None and  data.get('department')!=None):return self.Create_place(data.get('undepartment'), data.get('department'))  
        def MATCH(self,i,j,test=False):
            return self._match('undepartment',i,j)

        def MATCH_A(self,name):
            return self.query('MATCH (n:undepartment{name:\''+name+'\'}) return n')
        def departament(self,id):
            return self.query('match (n:undepartment)-[r:un]->(m:department) where  id(n)='+str(id)+' return DISTINCT m,r')
        def information(self):
            return( ['name','data'],'undepartment')            
        def information_E(self):
            return ({'department':(['department','undepartment'],'un')},'undepartment')
class employee(MODEL_data):
        __metaclass__ = Singleton
        def Create_arr(self,inf):
                self._add_CREATE('CREATE (a:employee{name:\''+inf['name']+'\',position:\''
                +inf['position']+'\',addres:\''+inf['addres']+'\',data:\''+inf['data']+'\'}) return a')
                return self.save()
        def Create(self,name,position,addres,data):      
            list(map(lambda x,y,z,w:self._add_CREATE('CREATE (a:employee{name:\''+x+'\',position:\''+y+'\',addres:\''+z+'\',data:\''+w+'\'}) return a'), name,position,addres,data))
            return self.save()
        def Create_place(self,labl,idD,id):
          self._add_CREATE('MATCH (a:'+labl+'),(b:employee) WHERE id(b)='+str(id)+' and id(a)='+str(idD)+' and not EXISTS((b)-[:life]-()) WITH a,b  CREATE (b)-[r:life]->(a)  return r')
          return self.save()
        def Create_Group(self,idG,idE):
            self._add_CREATE('MATCH (a:Group),(b:employee) WHERE  id(b)='+str(idE)+' and id(a)='+str(idG)+' not EXISTS((b)-[:curator]-()) and  EXISTS((a)-[:GR]-(:undepartment)-[:life]-(b)) WITH a,b  CREATE (b)-[r:curator]->(a)  return r' )
            return self.save()
        def Create_subject(self,idS,id):
            self._add_CREATE('MATCH (a:subject),(b:employee) WHERE id(b)='+str(id)+' and id(a)='+str(idS)+' WITH a,b  CREATE (b)-[r:employee_subject]->(a) return r')
            return self.save()
        def Crate_E(self,data):
            if(data.get('undepartment')!=None and  data.get('employee')!=None):return self.Create_place('undepartment',data.get('undepartment'), data.get('employee'))
            if(data.get('department')!=None and  data.get('employee')!=None):return self.Create_place('department',data.get('department'), data.get('employee'))    
            if(data.get('employee')!=None and data.get('Group')!=None):return self.Create_Group(data.get('Group'),data.get('employee'))  
            if(data.get('subject')!=None and data.get('employee')!=None):return self.Create_Group(data.get('subject'),data.get('employee'))  
        def MATCH(self,i,j,test=False):
            if(test):
                return self.query('MATCH (a:Group),(b:employee) WHERE not EXISTS((a)-[:curator]-()) and  EXISTS((a)-[:GR]-(:undepartment)-[:life]-(b)) return a,b')
            else:
                return self._match('employee',i,j)
         
        def departament(self,id):
            return self.query('match (n:employee)-[r:life|un*]->(m:department) where  id(n)='+str(id)+' return DISTINCT m,r')
        def information(self):
            return (['name','position','addres','data'],'employee')
        def information_E(self):
            return ({'undepartment':(['employee','undepartment'],'life'),'department':(['employee','department'],'life'),'Group':(['employee','Group'],'curator'),'subject':(['employee','subject'],'employee_subject')},'employee')    
class Group(MODEL_data):
        __metaclass__ = Singleton
        def Create_arr(self,inf):
                self._add_CREATE('CREATE (a:Group{name:\''+inf['name']+'\'}) return a')
                return self.save()
        def Create(self,name):      
            list(map(lambda x:self._add_CREATE('CREATE (a:Group{name:\''+x+'\'}) return a'),name))
            return self.save()
        def Create_un(self,id,idU):
           self._add_CREATE('MATCH (a:undepartment),(b:Group) WHERE id(b)='+str(id)+' and id(a)='+str(idU)+' and not EXISTS((b)-[:GR]-())   WITH a,b  CREATE (b)-[r:GR]->(a) return r')
           return self.save()
        def Crate_E(self,data):
            if(data.get('undepartment')!=None and data.get('Group')!=None): return self.Create_un(data.get('Group'),data.get('undepartment'))  
        def MATCH(self,i,j,test=False):
            return self._match('Group',i,j) 
        def information(self):
            return (['name'],'Group')
        def departament(self,id):
            return self.query('match (n:Group)-[r:GR|un*]->(m:department) where  id(n)='+str(id)+' return DISTINCT m,r')
        def information_E(self):
            return ({'undepartment':(['Group','undepartment'],'GR')},'Group')  
class subject(MODEL_data):
        __metaclass__ = Singleton
        def Create_arr(self,inf):
            self._add_CREATE('CREATE (a:subject{name:\''+inf['name']+'\',data:\''+inf['data']+'\'}) return a')
            return self.save()
        def Create(self,name,data):
            list(map(lambda x,y: self._add_CREATE('CREATE (a:subject{name:\''+x+'\',data:\''+y+'\'}) return a'),name,data))
            return self.save()
        def Create_time(self,idS,idL,time):
           self._add_CREATE('MATCH (a:subject),(b:lecture_hall) WHERE id(a)='+str(idS)+' AND id(b)='+str(idL)+'  WITH a,b  CREATE (a)-[r:time_lecture{time:\''+time+'\'}]->(b) return r')
           return self.save()
        def Create_un(self,idD,id):
          self._add_CREATE('MATCH (a:undepartment),(b:subject) WHERE id(b)='+str(id)+' and id(a)='+str(idD)+' and not EXISTS((b)-[:subject_undepartment]-()) WITH a,b  CREATE (b)-[r:subject_undepartment]->(a) return r ')
          return self.save()   
        def Crate_E(self,data):
            if(data.get('subject')!=None and data.get('undepartment')!=None): return self.Create_un(data.get('undepartment'),data.get('subject'))  
            if(data.get('subject')!=None and data.get('lecture_hall')!=None and data.get('time')!=None ): return self.Create_time(data.get('subject'),data.get('lecture_hall'),data.get('time'))   
        def MATCH(self,i,j,test=False):
            return self._match('subject',i,j) 

        def departament(self,id):
            return self.query('match (n:subject)-[r:subject_s|Group_SD|GR|un*]-(m:department) where  id(n)='+str(id)+' return DISTINCT m,r')
        def information(self):
            return (['name','data'],'subject')
        def information_E(self):
            return ({'undepartment':(['subject','undepartment'],'subject_undepartment'),'lecture_hall':(['subject','lecture_hall','time'],'time_lecture')},'subject')    
class lecture_hall(MODEL_data):
    __metaclass__ = Singleton
    def Create_arr(self,inf):
         self._add_CREATE('CREATE (a:lecture_hall{number:\''+inf['name']+'\'}) return a')
         return self.save()    
    def Create(self,N):
        list(map(lambda x: self._add_CREATE('CREATE (a:lecture_hall{number:'+str(x)+'}) return a'),N))
        return self.save()
    def Create_un(self,id,idU):
           self._add_CREATE('MATCH (a:lecture_hall),(b:undepartment) WHERE id(a)='+str(id)+' and id(b)='+str(idU)+' and not EXISTS((a)-[:lecture_hall_undepartment]-()) WITH a,b  CREATE (a)-[r:lecture_hall_undepartment]->(b) return r')
           return self.save()
    def Crate_E(self,data):
        if(data.get('lecture_hall')!=None and data.get('undepartment')!=None): return self.Create_un(data.get('lecture_hall'),data.get('undepartment'))
 
    def MATCH(self,i,j,test=False):
        return self._match('lecture_hall',i,j)
    def departament(self,id):
        return self.query('match (n:lecture_hall)-[r:time_lecture|subject_s|Group_SD|GR|un*]-(m:department) where  id(n)='+str(id)+' return DISTINCT m,r')
    def information(self):
            return (['name'],'lecture_hall')
    def information_E(self):
            return ({'undepartment':(['lecture_hall','undepartment'],'lecture_hall_undepartment')},'lecture_hall')
class student(MODEL_data):
    __metaclass__ = Singleton
    def Create_arr(self,inf):
         self._add_CREATE('CREATE (a:student{name:\''+inf['name']+'\',address:\''+inf['address']+'\',data:\''+inf['data']+'\'}) return a')
         return self.save()
    def Create(self,name,address,data):
        list(map(lambda x,y,z:self._add_CREATE('CREATE (a:student{name:\''+x+'\',address:\''+y+'\',data:\''+y+'\'}) return a'),name,address,data))
        return self.save()
    def Create_work(self,ids,idl,text):
              self._add_CREATE('MATCH (a:student),(b:employee) WHERE id(a)='+str(ids)+' AND id(b)='+str(idl)+' and not EXISTS((a)-[:DWorKW]-()) and EXISTS((a)--()-[:GR]-(:undepartment)-[:life]-(b))  WITH a,b  CREATE (a)-[r:DWorKW{text:\''+text+'\'}]->(b) return r')    
              return self.save()
    def Create_Group(self,ids,idG):
              self._add_CREATE('MATCH (a:student),(b:Group) WHERE id(a)='+str(ids)+' AND id(b)='+str(idG)+'   WITH a,b  CREATE (a)-[r:Group_SD]->(b) return r')    
              return self.save()
    def Create_subject(self,id,idS,evaluation):
              self._add_CREATE('MATCH (a:student),(b:subject) WHERE id(a)='+str(id)+' AND id(b)='+str(idS)+'  WITH a,b  CREATE (a)-[r:subject_s{evaluation:\''+evaluation+'\'}]->(b) return r')    
              return self.save()
    def Crate_E(self,data):
        if(data.get('Group')!=None and data.get('student')!=None): return self.Create_Group(data.get('student'),data.get('Group'))
        if(data.get('subject')!=None and data.get('student')!=None and data.get('evaluation')!=None): return self.Create_subject(data.get('student'),data.get('subject'),data.get('evaluation'))
        if(data.get('student')!=None and data.get('employee')!=None and data.get('text')!=None): return self.Create_work(data.get('student'),data.get('employee'),data.get('text'))

 
    def MATCH_lable(self,id,lable):
        return self.query('MATCH (a:student)-[r:'+lable+']-(n) WHERE id(a)='+str(id)+' return r,n')
    def MATCH(self,i,j,test=False):
            if(test):
                return self.query('MATCH (a:student),(b:employee) WHERE not EXISTS((a)-[:DWorKW]-()) and  EXISTS((a)--()-[:GR]-(:undepartment)-[:life]-(b)) return a,b')
            else:
                return self._match('student',i,j)
    def departament(self,id):
        return self.query('match (n:student)-[r:Group_SD|GR|un*]->(m:department) where  id(n)='+str(id)+' return DISTINCT m,r')
    def information(self):
            return (['name','address','data'],'student')
    def information_E(self):
            return ({'Group':(['Group','student'],'Group_SD'),'employee':(['employee','student','text'],'DWorKW'),'subject':(['subject','student','evaluation'],'subject_s')},'student')
class Strategy_data(MODEL_data):
    data=None
    information=None
    def logic(self,data):
        if('department'==data):self.data=department();self.data.error.clear()
        if('undepartment'==data): self.data=undepartment();self.data.error.clear()
        if('Group'==data):self.data=Group();self.data.error.clear()
        if('employee'==data):self.data=employee();self.data.error.clear()
        if('subject'==data): self.data=subject();self.data.error.clear()
        if('lecture_hall'==data):self.data=lecture_hall();self.data.error.clear()
        if('student'==data):self.data=student();self.data.error.clear()
    def label(self):
        return self.labels_name()
    def create(self,inf):
        return self.data.Create_arr(inf)

    def create_E(self,inf):
        self.data.Crate_E(inf)
     
    
    def match_model(self,i,j,test=False):
        return self.data.MATCH(i,j,test)
    def information(self):
        return self.data.information()
    def information_E(self):
        return self.data.information_E()
    def MATCH_rel(self, lable,rel):
        if(rel==None):
            return self._match(lable,0,0)
        else:
            return self.query('MATCH (n:'+lable+') WHERE  not EXISTS((n)-[:'+rel+']-())  return n')
    def dep(self,id):
         return self.query('MATCH (n)-[*]-(m:department) WHERE id(n)='+str(id)+' WITH n ')
#def test():
#    a=MODEL_data()
#    #b=[('department','name'),('department','data'),('undepartment','name'),('undepartment','data')
#    #,('employee','name'),('employee','position'),('employee','addres'),('employee','data')
#    #,('Group','name'),('subject','name'),('subject','data'),('lecture_hall','data')
#    #,('student','name'),('student','address'),('student','data')
#    #]
#    a.res(b)
def start2():
    st=MODEL_data()
    st.res()
    dep=department()
    undep=undepartment()
    a=dep.Create(['AFF','MMF'],['INF','INF'])
    b=undep.Create(['AF','MM'],['INF','INF'])
    undep.Create_department(MODEL_data.id_get_Create(b)[0],MODEL_data.id_get_Create(a)[0])
    undep.Create_department(MODEL_data.id_get_Create(b)[1],MODEL_data.id_get_Create(a)[0])
    emp=employee()
    a1=emp.Create(['RUS','EN','OI','QW'],['L','A','D','C'],['Sa','sb','sc','aw'],['A','a','A','a','A'])
    for i in MODEL_data.id_get_Create(a1):
        emp.Create_place('undepartment',MODEL_data.id_get_Create(b)[0],i)
    Gr=Group()
    b1=Gr.Create(['48A','347L'])
    Gr.Create_un(MODEL_data.id_get_Create(b1)[0],MODEL_data.id_get_Create(b)[0]);Gr.Create_un(MODEL_data.id_get_Create(b1)[1],MODEL_data.id_get_Create(b)[1])
    sub=subject()
    lec=lecture_hall()
    d1=lec.Create([484,125,365])
    c1=sub.Create(['GO','ll'],['neo','ll'])
    emp.Create_subject(MODEL_data.id_get_Create(c1)[0],MODEL_data.id_get_Create(a1)[0]);emp.Create_subject(MODEL_data.id_get_Create(c1)[1],MODEL_data.id_get_Create(a1)[1]);
    sub.Create_un(MODEL_data.id_get_Create(b)[0],MODEL_data.id_get_Create(c1)[0]);    sub.Create_un(MODEL_data.id_get_Create(b)[0],MODEL_data.id_get_Create(c1)[1])
    sub.Create_time(MODEL_data.id_get_Create(c1)[0],MODEL_data.id_get_Create(d1)[0],'12:00,07/03/2017');    sub.Create_time(MODEL_data.id_get_Create(c1)[1],MODEL_data.id_get_Create(d1)[0],'14:00,07/03/2017');
    sub.Create_time(MODEL_data.id_get_Create(c1)[0],MODEL_data.id_get_Create(d1)[1],'10:00,07/03/2017');
    stud=student()
    s1=stud.Create(['1','2','3'],['no','no','no'],['D','D','D'])
    for i in MODEL_data.id_get_Create(s1):
        stud.Create_work(i,MODEL_data.id_get_Create(a1)[0],'tem'+str(i))
    for i in MODEL_data.id_get_Create(s1):
        stud.Create_Group(i,MODEL_data.id_get_Create(b1)[i%2])
    for i in MODEL_data.id_get_Create(s1):
        stud.Create_subject(i,MODEL_data.id_get_Create(c1)[i%2],'NA')

#driver = GraphData,base.driver('bolt://localhost:7687', auth=basic_auth("neo4j", "3809696"),encrypted=False)
#res = driver.session()
#data=res.run("PROFILE MATCH (p:Person { name:\"Tom Hanks\" }) RETURN p")
#for i in data:
#        print(i)