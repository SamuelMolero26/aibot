
from flask import Flask, render_template, session
from flask.ctx import RequestContext
from flask import redirect, request, url_for
import jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('login_register.html')



@app.route('/login', methods=['POST'])
def login():
    print("Login is called")
    if request.method == 'POST':
        # Perform login verification logic here
        username = request.form.get('user_id')
        password = request.form.get('password')
        
        # Check if username and password are valid
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            session['username'] = username
            print("This is called")
            
            return redirect(url_for('dashboard'))
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    else:
        return render_template('login_register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['POST'])
def dashboard():
    print(request.method)
    print(request.url)
    if session.get('logged_in'):
        return render_template('page.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


