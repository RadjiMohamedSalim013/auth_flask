from flask import Flask, render_template, request, redirect, url_for, session



app = Flask(__name__)
app.secret_key = "2313acf58ce71e4fd0079fcad4e9234324084cc50498365ec1e57b67759de231"



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


        if username == 'admin' and password == 'admin':
            session['username'] = username

            return redirect(url_for('home'))
        else:
            return "Nom d'utilisateur ou mot de passe incorrect"

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)