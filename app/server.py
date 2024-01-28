
from flask import Flask, render_template, session
from flask.ctx import RequestContext
from flask import redirect, request, url_for
import jsonify


app = Flask(__name__)
app.secret_key = 'Carti'


@app.route('/', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        print("Login is called")
        # Perform login verification logic heres

        data = request.get_json()
        print(data)
        username = data['user_id']
        password = data['password']
        
        print(username,password)
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


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    print(request.method)
    print(request.url)
    if session.get('logged_in'):
        return render_template('features/page.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/todo', methods=['GET','POST'])
def todo():
    todo_item = request.form.get('todo_item')
    return render_template('features/todo.html')


if __name__ == '__main__':
    app.run(debug=True)


