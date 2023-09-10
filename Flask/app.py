from flask import Flask, render_template, request,session

app = Flask(__name__)
app.secret_key ='a'
def showall():
    sql= "SELECT * from JJ_TABLE"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The Contact is : ",  dictionary["CONTACT"])
        print("The Adress is : ",  dictionary["ADDRESS"])
        print("The Role is : ",  dictionary["ROLL"])
        print("The Branch is : ",  dictionary["BRANCH"])
        print("The Password is : ",  dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)
        
def getdetails(email,password):
    sql= "select * from JJ_TABLE where email='{}' and password='{}'".format(email,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The Contact is : ", dictionary["CONTACT"])
        print("The Address is : ", dictionary["ADDRESS"])
        print("The Role is : ", dictionary["ROLL"])
        print("The Branch is : ", dictionary["BRANCH"])
        print("The Password is : ", dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)
        
def create_user(conn,name,email,contact,address,role,branch,password):
    sql= "INSERT into JJ_TABLE VALUES('{}','{}','{}','{}','{}','{}','{}',NEXT VALUE FOR USER_SEQ)".format(name,email,contact,address,role,branch,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))
    
def insert_feedback(conn, email, name, registration_no, feedback_comments):
    sql= "INSERT into USER_FEEDBACK VALUES(NEXT VALUE FOR FEEDBACK_COMMENTS_SEQ,'{}','{}','{}','{}')".format(name, email, registration_no, feedback_comments)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))

def submit_assignment(conn,assignment_id,student_id,submission_dt,file_content):
    sql= "INSERT into ASSIGNMENT_SUBMISSION(SUBMISSION_ID, ASSIGNMENT_ID, STUDENT_ID, SUBMISSION_DT, SOLUTION) VALUES(NEXT VALUE FOR ASSIGNMENT_SUBMISSION_SEQ,'{}','{}','{}','{}')".format(assignment_id, student_id, submission_dt, file_content)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))

def get_comments():
    sql= "select * from USER_FEEDBACK"
    stmt = ibm_db.exec_immediate(conn, sql)
    comments = ibm_db.fetch_both(stmt)
    while comments != False:
        print("The Name is : ",  comments["ID"])
        print("The E-mail is : ", comments["NAME"])
        print("The Contact is : ", comments["EMAIL"])
        print("The Address is : ", comments["REGISTRATION_NO"])
        print("The Role is : ", comments["FEEDBACK_COMMENTS"])
        comments = ibm_db.fetch_both(stmt)
    return comments

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qzw20690;PWD=4QXenxs5r1fHLIN7",'','')
print(conn)
print("connection successful...")

@app.route('/')
def index():
    #return render_template('registration.html')
    return render_template('index.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/feedback', methods=['POST','GET'])
def feedback():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        registration_no = request.form['registrationNumber']
        feedback_comments = request.form['feedback']
        
        insert_feedback(conn, email, name, registration_no, feedback_comments)
        msg = "Feedback submitted successfully."
        return render_template('contactus.html', msg=msg)   
        
@app.route('/fill_registration_form')
def fill_registration_form():
    return render_template('adminregister.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        contact = request.form['mobile']
        address = request.form['address']
        role = request.form['role']
        if role =="0":
            role = "Faculty"
        elif role == "1":
            role = "Student"
        else:
            role = "New Admin"
        branch = request.form['branch']
        password = request.form['pwd']
        
        create_user(conn,name,email,contact,address,role,branch,password)
        return render_template('login.html')
        

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['pwd']
        sql= "select * from JJ_TABLE where email='{}' and password='{}'".format(email,password)
        stmt = ibm_db.exec_immediate(conn, sql)
        userdetails = ibm_db.fetch_both(stmt)
        while(userdetails):
            role = ibm_db.result(stmt, "ROLL").strip()
            session['register'] =userdetails["EMAIL"]
            session['student_id'] =userdetails["ID"]
            if ((role == "Student")==True):
                loginPage = 'studentprofile.html'
            elif ((role == "Faculty")==True):
                loginPage = 'facultyprofile.html'
            elif ((role == "New Admin")==True):
                loginPage = 'adminprofile.html'
            else:
                msg = "Incorrect Email id or Password"
                return render_template("login.html", msg=msg)
            return render_template(loginPage,name=userdetails["NAME"],email= userdetails["EMAIL"],contact= userdetails["CONTACT"],address=userdetails["ADDRESS"],role=userdetails["ROLL"],branch=userdetails["BRANCH"])
    return render_template('login.html')

@app.route('/comments', methods=['GET'])
def comments():
    pageToRender = 'comments.html'
    all_comments = []
    row_cnt = 0
    sql= "select * from USER_FEEDBACK"
    stmt = ibm_db.exec_immediate(conn, sql)
    comments = ibm_db.fetch_assoc(stmt)
    msg="Failed to load"
    while comments != False:
        msg="Loaded successfully"
        all_comments.insert(row_cnt, comments)
        row_cnt=row_cnt+1
        comments = ibm_db.fetch_assoc(stmt)
    return render_template(pageToRender, comments=all_comments, msg=msg)

@app.route('/studentassignment', methods=['GET', 'POST'])
def studentassignment():
    pageToRender = 'studentassignment.html'
    all_assignments = []
    row_cnt = 0
    student_id=3 #session["student_id"]
    sql= "SELECT A.ASSIGNMENT_ID, A.ASSIGNMENT_NM, A.ASSIGNMENT_DT, B.SUBMISSION_DT, B.MARKS_OBTAINED FROM ENROLLMENT E INNER JOIN ASSIGNMENT A ON A.FACULTY_ID=E.FACULTY_ID AND A.COURSE_ID=E.COURSE_ID INNER JOIN JJ_TABLE S ON S.ID=E.STUDENT_ID LEFT OUTER JOIN ASSIGNMENT_SUBMISSION B ON A.ASSIGNMENT_ID=B.ASSIGNMENT_ID WHERE S.ID={}".format(student_id)
    stmt = ibm_db.exec_immediate(conn, sql)
    assignments = ibm_db.fetch_assoc(stmt)
    msg="Failed to load"
    while assignments != False:
        msg="Loaded successfully"
        all_assignments.insert(row_cnt, assignments)
        row_cnt=row_cnt+1
        assignments = ibm_db.fetch_assoc(stmt)
    return render_template(pageToRender, assignments=all_assignments, msg=msg)

@app.route('/studentsubmit', methods=['GET', 'POST'])
def studentsubmit():
    pageToRender = 'studentsubmit.html'
    assignment_id = 1#request.form['assignment_id']
    student_id = 3 #request.form['student_id']
    submission_dt = '03-SEP-23'
    file_content = request.form['myfile']
    submit_assignment(conn,assignment_id,student_id,submission_dt,file_content)
    return render_template(pageToRender)
    

@app.route('/facultystulist', methods=['GET'])
def facultystulist():
    pageToRender = 'facultystulist.html'
    student_list = []
    row_cnt = 0
    faculty_id=1 #session["student_id"]
    sql= "SELECT S.NAME, C.COURSE_NM FROM ENROLLMENT E INNER JOIN JJ_TABLE S ON E.STUDENT_ID = S.ID INNER JOIN COURSES C ON E.COURSE_ID = C.COURSE_ID INNER JOIN FACULTY F ON E.FACULTY_ID = F.FACULTY_ID AND F.FACULTY_ID = C.FACULTY_ID AND F.FACULTY_ID={};".format(faculty_id)
    stmt = ibm_db.exec_immediate(conn, sql)
    students = ibm_db.fetch_assoc(stmt)
    msg="Failed to load"
    while students != False:
        msg="Loaded successfully"
        student_list.insert(row_cnt, students)
        row_cnt=row_cnt+1
        students = ibm_db.fetch_assoc(stmt)
    return render_template(pageToRender, student_list=student_list, msg=msg)

@app.route('/facultymarks', methods=['GET'])
def facultymarks():
    pageToRender = 'facultymarks.html'
    student_marks_list = []
    row_cnt = 0
    faculty_id=1 #session["student_id"]
    student_id=3 #session["student_id"]
    sql= "SELECT A.ASSIGNMENT_ID, A.ASSIGNMENT_NM, S.NAME, A.ASSIGNMENT_DT, B.SOLUTION, B.SUBMISSION_DT, B.MARKS_OBTAINED FROM ENROLLMENT E INNER JOIN ASSIGNMENT A ON A.FACULTY_ID=E.FACULTY_ID AND A.COURSE_ID=E.COURSE_ID INNER JOIN JJ_TABLE S ON S.ID=E.STUDENT_ID INNER JOIN COURSES C ON E.COURSE_ID = C.COURSE_ID INNER JOIN FACULTY F ON E.FACULTY_ID = F.FACULTY_ID AND F.FACULTY_ID = C.FACULTY_ID LEFT OUTER JOIN ASSIGNMENT_SUBMISSION B ON A.ASSIGNMENT_ID=B.ASSIGNMENT_ID WHERE F.FACULTY_ID={} AND S.ID={};".format(faculty_id, student_id)
    stmt = ibm_db.exec_immediate(conn, sql)
    student_marks = ibm_db.fetch_assoc(stmt)
    msg="Failed to load"
    while student_marks != False:
        msg="Loaded successfully"
        student_marks_list.insert(row_cnt, student_marks)
        row_cnt=row_cnt+1
        student_marks = ibm_db.fetch_assoc(stmt)
    return render_template(pageToRender, student_marks_list=student_marks_list, msg=msg)
    
if __name__ =='__main__':
    app.run( debug = True)
