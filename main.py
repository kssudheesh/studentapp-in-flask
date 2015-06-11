import os
import sqlite3
from flask import Flask,request,g,redirect,url_for,render_template,flash,session

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
   DATABASE=os.path.join(app.root_path,'marklist.db'),
   DEBUG=True,
   SECRET_KEY='sudheesh',  
))
app.config.from_envvar('FLASKR_SETTINGS',silent=True)

def connect_db():
  rv=sqlite3.connect(app.config['DATABASE'])
  rv.row_factory=sqlite3.Row
  return rv

def init_db():
  with app.app_context():
     db=get_db()
     with app.open_resource('schema.sql',mode='r')as f:
       db.cursor().executescript(f.read())
       db.commit()

def get_db():
  if not hasattr(g,'sqlite_db'):
     g.sqlite_db=connect_db()
  return g.sqlite_db

@app.route('/',methods=['GET','POST'])
def home():
  return render_template('home.html')

@app.route('/add',methods=['GET','POST'])
def add():
  if request.method=='POST':
    if request.form['create']=="create":
      db=get_db()
      db.execute('insert into marklist(name,mark) values(?,?)',[request.form['name'],request.form['mark']])
      db.commit()
      flash(' Details added..')
  return render_template('add.html')

@app.route('/view',methods=['GET','POST'])
def view():
     db = get_db()
     cur = db.execute('select name,mark from marklist')
     entries = cur.fetchall()
     return render_template('view.html', entries=entries)

@app.teardown_appcontext
def close_db(error):
  if hasattr(g,'sqlite_db'):
     g.sqlite_db.close()

if __name__=='__main__':
 app.run(debug=True)
