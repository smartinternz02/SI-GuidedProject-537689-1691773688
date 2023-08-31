from flask import Flask, render_template, request,session

app = Flask(__name__)


app.secret_key = 'a'
def showall():
    sql = "SELECT * from USER"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ", dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The Contact is : ", dictionary["CONTACT"])
        print("The Address is : ", dictionary["ADDRESS"])
        print("The Role is : ", dictionary["ROLE"])
        print("The Branch is : ", dictionary["BRANCH"])
        print("The Password is : ", dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)


def getdetails(email, password):
    sql = "select * from SB_TABLE where email='{}' and password='{}'".format(email, password)
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ", dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The Contact is : ", dictionary["CONTACT"])
        print("The Address is : ", dictionary["ADDRESS"])
        print("The Role is : ", dictionary["ROLE"])
        print("The Branch is : ", dictionary["BRANCH"])
        print("The Password is : ", dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)


def insertdb(conn, name, email, contact, address, role, branch, password):
    sql = "INSERT into SB_TABLE VALUES('{}','{}','{}','{}','{}','{}','{}')".format(name, email, contact, address, role,
                                                                                   branch, password)
    stmt = ibm_db.exec_immediate(conn, sql)
    print("Number of affected rows: ", ibm_db.num_rows(stmt))


import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=zgx14281;PWD=Jkqqzq4gvZUgbk7z",'', '')
print(conn)
print("connection successful...")

@app.route('/')
def index2():
    return render_template("index2.html")

@app.route('/register1', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        address = request.form['address']
        role = request.form['role']
        if role == "0":
            role = "Faculty"
        else:
            role = "Student"
        branch = request.form['branch']
        password = request.form['pwd']

        # inp=[name,email,contact,address,role,branch,password]
        insertdb(conn, name, email, contact, address, role, branch, password)
        return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['pwd']
        sql = "select * from USER where email='{}' and password='{}'".format(email, password)
        stmt = ibm_db.exec_immediate(conn, sql)
        userdetails = ibm_db.fetch_both(stmt)
        print(userdetails)
        if userdetails:
            session['register'] = userdetails["EMAIL"]
            return render_template('userprofile.html', name=userdetails["NAME"], email=userdetails["EMAIL"],contact=userdetails["CONTACT"], address=userdetails["ADDRESS"], role=userdetails["ROLE"], branch=userdetails["BRANCH"])
        else:
            msg = "Incorrect Email id or Password"
            return render_template("login.html", msg=msg)
    return render_template('login.html')



@app.route('/upload')
def submit():
    return render_template('upload.html')



@app.route('/uploader', methods = ['POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return render_template("uploader.html", name = f.filename)


@app.route('/admin_profile')
def admin():
    return render_template("admin_profile.html")

@app.route('/student_profile')
def sprofile():
    return render_template("student_profile.html")

@app.route('/faculty_profile')
def fprofile():
    return render_template("faculty_profile.html")

@app.route('/marks')
def marks():
    return render_template("marks.html")

@app.route('/assignment')
def assignment():
    return render_template("assignment.html")

@app.route("/logout")
def logout():

    return render_template("logout.html")

@app.route("/index2")
def home():
    return render_template("index2.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/register')
def index():
    return render_template('register.html')



if __name__ == "__main__":
    app.run(debug = True,port = 5000,host ='0.0.0.0')