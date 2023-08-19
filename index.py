from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
import json
from flask_login import LoginManager
login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = 'super-secret-key'
login_manager.init_app(app)

local_server=True

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/project"
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/project"
db = SQLAlchemy(app)

class Createacc1(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    mono = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(12))

    def __init__(self, name, email, mono,password):
        self.name = name
        self.email = email
        self.mono=mono
        self.password = password

class main1(db.Model):

    srno = db.Column(db.Integer, primary_key=True)
    sno =  db.Column(db.String(80), nullable=False)
    Comment=db.Column(db.String(80), nullable=False)
    textarea = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    secret = db.Column(db.String(12), nullable=False)
    syntex = db.Column(db.String(12),nullable=False)
    # PriPub=db.Column(db.String(12),nullable=False)

    def __init__(self, textarea, title, secret,syntex,sno,Comment):
        # self.srno=srno
        self.sno=sno
        self.Comment=Comment
        self.textarea = textarea
        self.title = title
        self.secret = secret
        self.syntex=syntex


@login_manager.user_loader
def load_user(sno):
    return Createacc1.get(sno)

@app.route("/", methods=['GET', 'POST'])
def login():
    login1 = Createacc1.query.filter_by().first()
    if ('user' in session and session['user'] == login1.email):
        return render_template("main.html")
    if (request.method=='POST'):
       useremail=request.form.get('uemail')
       userpassword=request.form.get('upassword')
       login = Createacc1.query.filter_by(email=useremail, password=userpassword).first()
       if login is not None:
           session['user'] = useremail
           session['sno']=login.sno
           session['name']=login.name
           print(session['name'])
           return render_template('main.html')
       else:
           return render_template("login.html")
    return render_template("login.html")

@app.route("/signup",methods=['GET','POST'])
def createacc():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        mono=request.form.get('mono')
        password=request.form.get('password')
        if len(mono) != 10:
            return "Plese Enter 10 Digit Number....."
        else:
         login1=Createacc1.query.filter_by(email=email).first()
         if login1 is not None:
            return "Enter Other Email This Email Is Alredy use Someone......."
         else:
          entry=Createacc1(name=name,email=email,mono=mono,password=password)

          db.session.add(entry)
          db.session.commit()
         return render_template("login.html")



    return render_template("signup.html")


@app.route("/main",methods=['GET','POST'])
def main():
    if (request.method == 'POST'):
        textarea = request.form.get('textarea')
        title = request.form.get('title')
        secret = request.form.get('secret')
        syntex = request.form.get('syntex')
        # PriPub=  request.form.get('PriPub')
        search = request.form.get('search')
        login1=main1.query.filter_by(secret=secret).first()
        if login1 is  not None:
            return "Plaese Use Anther Secret Key This Key Is Allredy USe Someone...."
        else:
         login = main1.query.filter_by(secret=search).first()
         if login is not None:
            # return redirect("/show")
            session['srno'] = login.srno
            session['textarea'] = login.textarea
            session['title'] = login.title
            session['syntex'] = login.syntex
            session['secret'] = login.secret
            session['Comment']=login.Comment


            return redirect("/search")
         else:
             session['textarea'] = "This secret key doesn't exist"
             session['title'] = ""
             session['syntex'] = ""
             session['secret'] = ""
             session['Comment'] = ""
             return redirect("/search")
         {}

         entry = main1(textarea=textarea, title=title, secret=secret, syntex=syntex, sno=session['sno'],Comment="")
         db.session.add(entry)
         db.session.commit()
         return render_template("main.html",createacc=createacc,login1=login1)

    return render_template("main.html",createacc=createacc)


@app.route("/edit/<string:srno>",methods=['get','post'])
def edit(srno):
    # if ('user' in session and session['user'] == Createacc1.email):
    login = Createacc1.query.filter_by().first()
    if login is not None:
        if (request.method == 'POST'):
            box_textarea =request.form.get('textarea')
            box_title =request.form.get('title')
            box_secret =request.form.get('secret')
            box_syntex =request.form.get('syntex')
            if srno == '0':
              Main1 = main1(textarea = box_textarea, title = box_title, secret = box_secret, syntex = box_syntex)
              db.session.add(Main1)
              db.session.commit()
            else:
              Main1 = main1.query.filter_by(srno=srno).first()
              Main1.textarea = box_textarea
              Main1.title = box_title
              Main1.secret = box_secret
              Main1.syntex = box_syntex
            db.session.commit()
            return redirect('/show')

    Main1 = main1.query.filter_by(srno=srno).first()
    return render_template('edit.html',Main1=Main1)



@app.route("/delete1/<string:srno>",methods=['get','post'])
def delete(srno):
    login = Createacc1.query.filter_by().first()
    if login is not None:
        Main1=main1.query.filter_by(srno=srno).first()
        db.session.delete(Main1)
        db.session.commit()
    return redirect('/show')

@app.route("/delete2/<string:srno>",methods=['get','post'])
def delete2(srno):
    login = Createacc1.query.filter_by().first()
    if login is not None:
        Main1=main1.query.filter_by(srno=srno).first()
        if Main1:
         Main1.Comment = ""

         db.session.commit()
    return redirect('/show')



@app.route("/resetemail",methods=['get','post'])
def Resetemail():
    if (request.method == 'POST'):
        oemail = request.form.get('email')
        npassword = request.form.get('password')
        nemail = request.form.get('nemail')
        login = Createacc1.query.filter_by(email=oemail, password=npassword).first()
        if login:
            login.email = nemail
            db.session.commit()
            return render_template("login.html")
    return render_template("resetemail.html")

@app.route("/resetpassword",methods=['get','post'])
def reset():
    if (request.method == 'POST'):
        nemail = request.form.get('email')
        npassword = request.form.get('password')
        newpassword = request.form.get('cpnpas')
        login= Createacc1.query.filter_by(email=nemail,password=npassword).first()
        if login:
            login.password=newpassword
            # entry = Createacc1(name=login.name, email=login.email, mono=login.mono, password=login.password)
            # db.session.add(entry)
            db.session.commit()
            return render_template("login.html")


    return render_template("resetpassword.html")

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')

@app.route("/show/")
def show():
    posts = main1.query.filter_by(sno=session['sno']).all()



    return render_template("show.html",posts=posts,login=login)

@app.route("/search",methods=['get','post'])
def search():
    if (request.method == 'POST'):
        Comment = request.form.get('Comment')

        login1=main1.query.filter_by(textarea=session['textarea'], title=session['title'], secret=session['secret'], syntex=session['syntex'], srno=session['srno']).first()
        if login1 is not None:
           login1.Comment= session['Comment']+ "\n"+ session['name'] +" ==> " + Comment
           db.session.commit()
           return render_template("search.html")

    # login=main1(textarea=session['textarea'],title=session['title'],syntex=session['syntex'],secret=session['secret'],sno=session['sno'],Comment=session['Comment'])
    return render_template("search.html")

app.run(debug=True)