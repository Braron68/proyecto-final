from flask import Flask, render_template, request, redirect, url_for, session
from user import users

app = Flask(__name__)
app.secret_key = 'clave de acceso'


registro_horas = []

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['contraseña']
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Usuario o contraseña incorrectos")
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', user=session['username'])

@app.route('/submit', methods=['POST'])
def submit():
    if 'username' not in session:
        return redirect(url_for('index'))

    entrada = request.form['entrada']
    salida = request.form['salida']
    fecha = request.form['fecha']
    comentario = request.form['comentario']

    registro_horas.append({
        'usuario': session['username'],
        'fecha': fecha,
        'entrada': entrada,
        'salida': salida,
        'comentario': comentario
    })

    return render_template('success.html', user=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
