LOAD CSV WITH HEADERS FROM "file:///employees.csv" AS row
create (n:employee{name:row.LastName,addres:row.Address,position:row.Title,data:row.HireDate,EmployeeID:row.EmployeeID});

LOAD CSV WITH HEADERS FROM "file:///grup.csv" AS row
create (n:Group{name:row.name,grupID:row.grupID});


LOAD CSV WITH HEADERS FROM "file:///undepartment.csv" AS row
create (n:undepartment {name:row.name,data:row.data,undepartmentID:row.undepartmentID});


LOAD CSV WITH HEADERS FROM "file:///department.csv" AS row
create (n:department {name:row.name,data:row.data,departmentID:row.departmentID});


CREATE INDEX ON :employee(EmployeeID);
CREATE INDEX ON :Group(grupID);
CREATE INDEX ON :undepartment(undepartmentID);
CREATE INDEX ON :department(departmentID);



USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///employees.csv" AS row
MATCH (un:undepartment {undepartmentID: row.undepartment})
MATCH (emp:employee {EmployeeID: row.EmployeeID})
MERGE (emp)-[:life]->(un);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///grup.csv" AS row
MATCH (un:undepartment {undepartmentID: row.undepartment})
MATCH (emp:employee {EmployeeID: row.curator}) 
MATCH (Gr:Group {grupID: row.grupID})
MERGE (emp)-[:curator]->(Gr)
MERGE (Gr)-[:GR]->(un);


USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///undepartment.csv" AS row
MATCH (und:undepartment {undepartmentID: row.undepartmentID})
MATCH (d:department {departmentID: row.department})
MERGE (und)-[:un]->(d);



drop INDEX ON :employee(EmployeeID);
drop INDEX ON :Group(grupID);
drop INDEX ON :undepartment(undepartmentID);
drop INDEX ON :department(departmentID);

MATCH (n:employee) SET n.EmployeeID = NULL;
MATCH (n:Group) SET n.grupID = NULL;
MATCH (n:undepartment) SET n.undepartmentID = NULL;
MATCH (n:department) SET n.departmentID = NULL;
