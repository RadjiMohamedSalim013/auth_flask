from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  LoginManager, UserMixin, login_user,  logout_user, login_required, current_user
from flask_migrate import Migrate
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__)
app.secret_key = "2313acf58ce71e4fd0079fcad4e9234324084cc50498365ec1e57b67759de231"


#configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

s = URLSafeTimedSerializer(app.secret_key)

migrate = Migrate(app, db)

from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'radjimohamed013@gmail.com'  # Remplace par ton email
app.config['MAIL_PASSWORD'] = 'pxlq nxwz brad xtoh'    # Remplace par ton mot de passe

mail = Mail(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



#création de la table User

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)






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
        email = request.form['email']

        existed = User.query.filter(User.username == username).first()
        if existed :
            return "Cet utilisateur existe déjà"
        
        # Hacher le mot de passe avant de le sauvegarder
        hashed_password = generate_password_hash(password)

        # Ajouter le nouvel utilisateur à la base de données
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


#envoi d'un email pour renitialiser le mot de passe
@app.route('/reset_password_request', methods=['POST', 'GET'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            send_reset_email(user)
            return "Un email de réinitialisation de mot de passe a été envoyé à votre adresse email."
        else:
            return "Aucun utilisateur avec cette adresse email."
    return render_template('reset_password_request.html')



def send_reset_email(user):
    try:
        token = s.dumps(user.email, salt='recover-password')
        reset_url = url_for('reset_password', token=token, _external=True)
        msg = Message('Réinitialisation de mot de passe',
                      sender='radjimohamed013@gmail.com',
                      recipients=[user.email])
        msg.body = f"Pour réinitialiser votre mot de passe, visitez le lien suivant : {reset_url}"
        mail.send(msg)
        print(f"Email envoyé à {user.email}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")


@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    try:
        email = s.loads(token, salt='recover-password', max_age=3600)
    except:
        return "Token expiré"
    
    if request.method == 'POST':
        new_password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)