from flask import Flask , render_template,request,session 
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail 
import pymysql
pymysql.install_as_MySQLdb()
from datetime import datetime
import json

with open('config.json' , 'r')as c: # To connect the json file in read mode
    params = json.load(c)["params"]

local_Server = True
app = Flask(__name__)        # initialize flask
app.secret_key = 'super-secret-key'          #secret key for secure connection



app.config.update(   #Connect to mail server
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)

mail = Mail(app)  #initialize mail
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/webuild'
db = SQLAlchemy(app) #for databse







class contactmails(db.Model): # information store into database
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    phone_num = db.Column(db.String(20),nullable=False)
    sub = db.Column(db.String(120),nullable=False)
    msg = db.Column(db.String(120),nullable=False)
    date = db.Column(db.String(12), nullable = True)

class posts(db.Model): # information store into database
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    slug = db.Column(db.String(120),nullable=False)
    contant= db.Column(db.String(20),nullable=False)
    date = db.Column(db.String(12), nullable = True)

class jobapplications(db.Model): # information store into database
    sno = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(120),nullable=False)
    dob = db.Column(db.String(120),nullable=False)
    phone_num = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    add1 = db.Column(db.String(120),nullable=False)
    add2 = db.Column(db.String(12), nullable =False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    zip_code = db.Column(db.String(120),nullable=False)
    reffer = db.Column(db.String(120),nullable=False)
    date = db.Column(db.String(120),nullable=True)

class employeedetails(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    position = db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(120),nullable=False)
    age = db.Column(db.String(20),nullable=False)
    st_date = db.Column(db.String(120),nullable=False)
    salary = db.Column(db.String(120),nullable=False)
    date = db.Column(db.String(12), nullable =True)

@app.route("/")
def index():
    return render_template('index.html', params=params)

@app.route("/about")
def about():
    return render_template('about.html',params=params)

@app.route("/dashboard",  methods = {'GET', 'POST'})
def dashboard():
    if "user" in session and session['user']==params['admin_user']:
        return render_template("dashboard.html", params=params,)

    if request.method=="POST":
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        if username==params['admin_user'] and userpass==params['admin_password']:
            # set the session variable
            session['user']=username
            return render_template("dashboard.html", params=params, posts=posts)
        else:
            return("PLEASE ENTER VALID USER_NAME AND PASSWORD OTHERWISE YOU CAN'T ACCESS THE ADMIN PAGE ")
    else:
        return render_template("login.html", params=params)



@app.route("/services")
def services():
    return render_template('services.html',params=params)

@app.route("/projects")
def projects():
    return render_template('projects.html',params=params)


@app.route("/blog")
def blog():
    return render_template('blog.html',params=params)


@app.route("/admin")
def admin():
    return render_template('login.html',params=params)



@app.route("/contact", methods = {'GET', 'POST'})
def contact():
    if(request.method == 'POST'): #collect data from contact form
       name =request.form.get('name')
       email =request.form.get('email')
       phone =request.form.get('phone')
       subject=request.form.get('subject')
       message =request.form.get('message')
       entry = contactmails(name = name,
                            email = email,
                            phone_num = phone,
                            sub = subject,
                            msg = message,
                            date=datetime.now())
       db.session.add(entry) 
       db.session.commit()
       mail.send_message ('New quary from - ' + name, #Sending message to the email
                        sender = email,
                        recipients = [params['gmail-user']],
                        body = subject +"\n"+ message + "\n" + email + "\n" + phone,
                        )

    return render_template('contact.html', params=params)

@app.route("/career",methods={'GET','POST'})
def career():
    
   if(request.method == 'POST'): #collect data from contact form
      firstname =request.form.get('firstname')
      lastname=request.form.get('lastname')
      dateofbirth=request.form.get('dateofbirth')
      phone=request.form.get('phone')
      email=request.form.get('email')
      address1 =request.form.get('address1')
      address2=request.form.get('address2')
      city =request.form.get('city')
      state=request.form.get('state')
      zipcode=request.form.get('zipcode')
      reffer=request.form.get('reffer')
      entry = jobapplications(first_name = firstname,
                           last_name = lastname,
                           dob= dateofbirth,
                           phone_num = phone,
                            email = email,
                            add1 = address1,
                            add2 = address2,
                            city = city,
                            state = state,
                            zip_code = zipcode,
                            reffer = reffer,
                            date=datetime.now())
                            
      db.session.add(entry)
      db.session.commit()
      mail.send_message ('WeBuild_Job Application From '+"-"+ firstname+" "+lastname,
                        sender = email,
                        recipients = [params['gmail-user']],
                        body = "Name- "+firstname+" "+lastname+"\n" + "Date-Of-Birth"+dateofbirth+"\n"+ "Phone_number -" +phone+ "\n" +"Email-"+email+"\n"+ "Address -"+address1+","+address2+","+ city+","+state+","+ zipcode+"\n"+"Refferal from -" + reffer,
                        )
   return render_template('career.html', params=params)


@app.route("/add-employee", methods={'GET', 'POST'})
def addemployee():
    if(request.method == 'POST'): #collect data from contact form
       empname =request.form.get('empname')
       position =request.form.get('position')
       address =request.form.get('address')
       age=request.form.get('age')
       startdate =request.form.get('startdate')
       salary = request.form.get('salary')
       entry = employeedetails(name = empname,
                             position = position,
                            address = address,
                            age = age,
                            st_date =startdate,
                            salary = salary,
                            date=datetime.now())

    db.session.add(entry)
    db.session.commit()
    return render_template('add_employee.html',params=params)


@app.route("/blog-details")
def blogdetails_route():
    return render_template('blog-details.html', params=params)

@app.route("/service-details")
def servicedetails():
    return render_template('service-details.html',params=params)

@app.route("/project-details")
def projectsdetails():
    return render_template('project-details.html',params=params)

@app.route("/employee-details")
def employeedetails():
    return render_template('employee_details.html',params=params)

@app.route("/commercial")
def commercial():
    return render_template('commercial.html',params=params)

@app.route("/architecture")
def architecture():
    return render_template('architecture.html',params=params)

@app.route("/builders")
def builders():
    return render_template('builders.html',params=params)

@app.route('/project-status')
def projectstatus():
    data = {'Task' : 'Hours per Day', 'Total Budget' : 44, 'Risk' : 4, 'Progress' : 6, 'Pending' : 5, 'Working' : 15}
    return render_template('project_status.html', params=params, data=data)


if __name__== "__main__":
    app.run(debug=True)