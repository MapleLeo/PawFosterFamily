from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.foster import Foster
from flask_app.models.pet import Pet
from flask_app.models.application import Application
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/foster')
def foster_index():
    return render_template('foster_index.html')

@app.route('/foster/register',methods=['POST'])
def foster_register():
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
def foster_login():
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
def foster_dashboard():
    if 'foster_id' not in session:
        return redirect('/foster/logout')
    data = {
        'id': session['foster_id']
    }
    pets = Pet.get_all_available()
    return render_template('foster_dashboard.html',foster=Foster.get_by_id(data), pets=pets)

@app.route('/fosters/<int:id>')
def foster_thoughts(id):
    if 'foster_id' not in session:
        return redirect('/foster/logout')
    data = {
        'id':id
    }
    return render_template('show_thoughts.html',foster=Foster.get_by_id(data),thoughts=Thought.thoughts_for_user(data))

@app.route('/foster/account')
def foster_account():
    if 'foster_id' not in session:
        return redirect('/foster/logout')
    data = {
        'id': session['foster_id']
    }
    pets = Pet.get_by_foster(session['foster_id'])
    applications = Application.get_by_foster(session['foster_id'])
    return render_template('foster_account.html',foster=Foster.get_by_id(data), pets=pets, applications=applications)

@app.route('/logout')
def foster_logout():
    session.clear()
    return redirect('/')    

@app.route('/read_notification/<int:id>' ,methods=['POST'])
def read_notification(id):
    if 'foster_id' not in session:
        return redirect('/foster/logout')
    Application.mark_read(id)
    return redirect('/foster/account')