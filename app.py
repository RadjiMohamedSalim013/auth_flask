from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  LoginManager, UserMixin, login_user,  logout_user, login_required, current_user




app = Flask(__name__)
app.secret_key = "2313acf58ce71e4fd0079fcad4e9234324084cc50498365ec1e57b67759de231"


#configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



#création de la table User

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
@login_required
def home():
        return render_template('home.html', username=current_user.username)

#connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérifier l'utilisateur dans la base de données
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return 'Nom d\'utilisateur ou mot de passe incorrect'

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
        
        # Hacher le mot de passe avant de le sauvegarder
        hashed_password = generate_password_hash(password)

        # Ajouter le nouvel utilisateur à la base de données
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)