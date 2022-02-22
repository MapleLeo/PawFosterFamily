from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.shelter import Shelter
from flask_app.models.pet import Pet
from flask_app.models.application import Application
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/shelter')
def shelter_index():
    return render_template('shelter_index.html')

@app.route('/shelter/register',methods=['POST'])
def shelter_register():
    if not Shelter.validate_register(request.form):
        return redirect('/shelter')
    data = {
        'shelter_name': request.form['shelter_name'],
        'email': request.form['email'],
        'city': request.form['city'],
        'state': request.form['state'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = Shelter.save(data)
    session['shelter_id'] = id
    return redirect('/shelter/dashboard')

@app.route('/shelter/login',methods=['POST'])
def shelter_login():
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
def shelter_dashboard():
    if 'shelter_id' not in session:
        return redirect('/shelter/logout')
    data = {
        'id': session['shelter_id']
    }
    pet_data = {
        'shelter_id': session['shelter_id']
    }
    pets = Pet.get_by_shelter(pet_data)
    applications = Application.get_by_shelter_with_pet_and_foster(session['shelter_id'])
    return render_template('shelter_dashboard.html',shelter=Shelter.get_by_id(data),pets=pets, applications=applications)

@app.route('/shelters/<int:id>')
def shelter_thoughts(id):
    if 'shelter_id' not in session:
        return redirect('/shelter/logout')
    data = {
        'id':id
    }
    return render_template('show_thoughts.html',shelter=Shelter.get_by_id(data),thoughts=Thought.thoughts_for_user(data))


@app.route('/logout')
def shelter_logout():
    session.clear()
    return redirect('/')    