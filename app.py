from flask import Flask,render_template,request,redirect,flash,g,session,send_from_directory
from fileinput import filename 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import urllib.request
import os,requests,json
load_dotenv()
app = Flask(__name__)
app.secret_key = '1a2b3c4d5e6d7g8h9i10'
UPLOAD_FOLDER='static'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']=16*1024*1024

ALLOWED_EXTENSIONS=set(['png','jpg','jpeg','gif','txt'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS




# Create a new client and connect to the server
client = MongoClient("mongodb+srv://periyasamyj51:poomani@2005Bd@cluster0.rc3fnqk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Create a new client and connect to the server
#client = MongoClient(os.getenv("uri"), server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
#try:
   # client.admin.command('ping')
   # print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
   # print(e)

db_name="course_application"
database=client[db_name]
collection_name="register_details"
registerdetails=database[collection_name]
ddata=registerdetails.find()



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')
@app.route('/home')
def home():
    return redirect('/')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/courses')
def courses():
    return render_template('courses.html')
@app.route('/teachers')
def teachers():
    return render_template('teachers.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/update')
def update():
    return render_template('update.html')
@app.route('/playlist')
def playlist():
    return render_template('playlist.html')
@app.route('/teacher_profile')
def teacher_playlist():
    return render_template('teacher_profile.html')
@app.route('/watch-video')
def watch_video():
    return render_template('watch-video.html')




@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/register/submit',methods=['GET','POST'])
        
def submit():
    name=request.form.get("name")
    email=request.form.get("email")
    n_pass=request.form.get("pass")
    c_pass=request.form.get("c_pass")
    file=request.files['inputfile']
    filename=secure_filename(file.filename)
   # filename=secure_filename(file.filename)
    if file.filename=='':
        session['file']='pic-1.jpg'
    elif file and allowed_file(file.filename):
      file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
      session['file']=filename
      pass
    else:
        flash('Invalid Upload file format use png,gif,jpg')
        return redirect('/register')
    profile=session['file']
    if registerdetails.find_one({'emailId': email}):
        user=True
    else:
        user=False
    data={
            "name":name,
            "emailId":email,
            "profile":profile,
            "password":c_pass
    }
    if user==True:
         flash("Email is alredy used", "danger")
         return redirect('/register')
    elif n_pass !=c_pass:
          flash("New Password and Conform Password not Match", "danger")
          return redirect('/register')
    else:
     registerdetails.insert_one(data)      
     return redirect('/login')
    
@app.route('/login', methods=['GET', 'POST'])
def login_submit():
    if request.method == 'POST':
        lemail = request.form.get("lemail")
        lpassword = request.form.get("lpass")
        user = registerdetails.find_one({'emailId': lemail, 'password': lpassword})
        if user:
            session['password']=lpassword
            username = user['name']
            session['uname']=username
            session['email']=user['emailId']
            filename=session['file']
            return render_template('home/home1.html',username=username,filename=filename)
        else:
            flash('Username and password do not match!', "danger")
            return redirect('/login')

    return render_template('login.html')




@app.route('/update1',methods=['GET','POST'])
def profile1():
    if request.method=='POST':
        up_name=request.form.get('name')
        up_email=request.form.get('email')
        up_oldpass=request.form.get('old_pass')
        up_newpasss=request.form.get('new_pass')
        up_cpass=request.form.get('c_pass')
        password=session['password']
        email=session['email']
        #for data in ddata:
           # if data['emailId']==email and data['password']==password:
             #id=data['_id'] 
           # else:
              #  pass

        if up_oldpass !=password:
            flash(' Old password does not match!', "danger")
            return render_template('home/update1.html',username=session['uname'])
        else:
            if up_newpasss !=up_cpass:
                flash(" New Password and Conform not Match", "danger")
                return render_template('home/update1.html',username=session['uname'])
            else:
                for data in ddata:
                    if data['emailId']==email and data['password']==password:
                        id=data['_id']
                    else:
                        pass
                myquery={"_id":id}
                newvalue={"$set":{"name":up_name,"emailId":up_email,"password":up_cpass}}
                registerdetails.update_one(myquery,newvalue)
                session['uname']=up_name
                session['email']=up_email
                return redirect('/profile1')
    return render_template('home/update1.html',username=session['uname'])
@app.route('/home1')
def home1():
    return render_template('home/home1.html',username=session['uname'])
@app.route('/about1')
def about1():
    return render_template('home/about1.html',username=session['uname'])
@app.route('/courses1')
def courses1():
    return render_template('home/courses1.html',username=session['uname'])
@app.route('/teachers1')
def teachers1():
    return render_template('home/teachers1.html',username=session['uname'])
@app.route('/contact1')
def contact1():
    return render_template('home/contact1.html',username=session['uname'])
@app.route('/profile1')
def update1():
    return render_template('home/profile1.html',username=session['uname'],email=session['email'])
@app.route('/playlist1')
def playlist1():
    return render_template('home/playlist1.html',username=session['uname'])
@app.route('/playlistjs')
def playlistjs():
    return render_template('home/playlistjs.html',username=session['uname'])
@app.route('/playstcs')
def playstcs():
    return render_template('home/playstcs.html',username=session['uname'])
@app.route('/playlistr')
def playlistr():
    return render_template('home/playlistr.html',username=session['uname'])
@app.route('/playlistp')
def playlistp():
    return render_template('home/playlistp.html',username=session['uname'])
@app.route('/playlistb')
def playlistb():
    return render_template('home/playlistb.html',username=session['uname'])
@app.route('/teacher_profile1')
def teacher_playlist1():
    return render_template('home/teacher_profile1.html',username=session['uname'])
@app.route('/akalprofil')
def akalprofil():
    return render_template('home/akalprofil.html',username=session['uname'])
@app.route('/darsani')
def darsani():
    return render_template('home/darsani.html',username=session['uname'])
@app.route('/priya')
def priya():
    return render_template('home/priya.html',username=session['uname'])
@app.route('/suwetha')
def suwetha():
    return render_template('home/suwetha.html',username=session['uname'])
@app.route('/vijay')
def vijay():
    return render_template('home/vijay.html',username=session['uname'])
@app.route('/watch-video1')
def watch_video1():
    return render_template('home/watch-video1.html',username=session['uname'])


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)
