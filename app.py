from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = "2313acf58ce71e4fd0079fcad4e9234324084cc50498365ec1e57b67759de231"


#configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#création de la table User

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    if  "username" in session:
        return render_template('home.html', username=session["username"])
    return redirect(url_for('login'))


#connexion
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        user = User.query.filter(User.username == username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')


#inscription
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existed = User.query.filter(User.username == username).first()
        if existed :
            return "Cet utilisateur existe déjà"
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')




@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)