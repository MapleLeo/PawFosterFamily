from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.foster import Foster
from flask_app.models.pet import Pet
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/foster')
def index():
    return render_template('foster_index.html')

@app.route('/foster/register',methods=['POST'])
def register():
    if not Foster.validate_register(request.form):
        return redirect('/foster')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'city': request.form['city'],
        'state': request.form['state'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = Foster.save(data)
    session['foster_id'] = id
    return redirect('/foster/dashboard')

@app.route('/foster/login',methods=['POST'])
def login():
    foster = Foster.get_by_email(request.form)

    if not foster:
        flash("Invalid Email","foster_login")
        return redirect('/foster')
    if not bcrypt.check_password_hash(foster.password, request.form['password']):
        flash("Invalid Password","foster_login")
        return redirect('/foster')
    session['foster_id'] = foster.id
    return redirect('/foster/dashboard')

@app.route('/foster/dashboard')
def dashboard():
    if 'foster_id' not in session:
        return redirect('/foster/logout')
    data = {
        'id': session['foster_id']
    }
    return render_template('foster_dashboard.html',foster=Foster.get_by_id(data), thoughts=Thought.get_all(),like_count_dict=Thought.like_count_dict())

@app.route('/fosters/<int:id>')
def foster_thoughts(id):
    if 'foster_id' not in session:
        return redirect('/foster/logout')
    data = {
        'id':id
    }
    return render_template('show_thoughts.html',foster=Foster.get_by_id(data),thoughts=Thought.thoughts_for_user(data))


@app.route('/foster/logout')
def logout():
    session.clear()
    return redirect('/foster')    