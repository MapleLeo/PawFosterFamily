from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.shelter import Shelter
from flask_app.models.pet import Pet
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/shelter')
def index():
    return render_template('shelter_index.html')

@app.route('/shelter/register',methods=['POST'])
def register():
    if not Shelter.validate_register(request.form):
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
    session['shelter_id'] = id
    return redirect('/shelter/dashboard')

@app.route('/shelter/login',methods=['POST'])
def login():
    shelter = Shelter.get_by_email(request.form)

    if not shelter:
        flash("Invalid Email","login")
        return redirect('/foster')
    if not bcrypt.check_password_hash(shelter.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/shelter')
    session['shelter_id'] = shelter.id
    return redirect('/shelter/dashboard')

@app.route('/shelter/dashboard')
def dashboard():
    if 'shelter_id' not in session:
        return redirect('/shelter/logout')
    data = {
        'id': session['shelter_id']
    }
    return render_template('shelter_dashboard.html',shelter=Shelter.get_by_id(data), thoughts=Thought.get_all(),like_count_dict=Thought.like_count_dict())

@app.route('/shelters/<int:id>')
def shelter_thoughts(id):
    if 'shelter_id' not in session:
        return redirect('/shelter/logout')
    data = {
        'id':id
    }
    return render_template('show_thoughts.html',shelter=Shelter.get_by_id(data),thoughts=Thought.thoughts_for_user(data))


@app.route('/shelter/logout')
def logout():
    session.clear()
    return redirect('/shelter')    