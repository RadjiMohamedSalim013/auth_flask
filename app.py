from flask import Flask, render_template, request, redirect, url_for



app = Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html')



#connexion
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        if username == 'admin' and password == 'admin':
            return redirect(url_for('home'))
        else:
            return "Nom d'utilisateur ou mot de passe incorrect"

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)