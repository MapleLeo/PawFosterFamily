from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.pet import Pet
from flask_app.models.foster import Foster
from flask_app.models.shelter import Shelter
from flask_app.models.application import Application
import os
@app.route('/new/pet')
def new_pet():
    if'shelter_id' not in session:
        return redirect('/logout')

    data = {
        'id':session['shelter_id']
    }
    
    return render_template('new_pet.html', shelter=Shelter.get_by_id(data))

@app.route('/create/pet', methods=['POST'])
def add_pet():
    if 'shelter_id' not in session:
        return redirect('/logout')
    if not Pet.validate_pet(request.form):
        return redirect('/shelter/dashboard')
    if 'img' not in request.files:
        return redirect("/shelter/dashboard")
    file = request.files['img']
    file.save(os.path.join("flask_app/Static/", file.filename))
    data = {
        'img': file.filename,
        'name': request.form['name'],
        'age': request.form['age'],
        'foster_time_needed': request.form['foster_time_needed'],
        'foster_grade': request.form['foster_grade'],
        'description': request.form['description'],
        'shelter_id': session['shelter_id']
    }
    id=Pet.save(data)
    return redirect('/shelter/dashboard')

@app.route('/apply/pet/<int:id>', methods=['POST'])
def apply_pet(id):
    if 'foster_id' not in session:
        return redirect('/logout')
    data = {
        'pet_id': id,
        'foster_id': session['foster_id'],
        'status': 'PENDING',
    }
    Application.save(data)
    return redirect('/foster/dashboard')

@app.route('/destroy/pet/<int:id>')
def destroy_pet(id):
    if 'shelter_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    Pet.destroy(data)
    return redirect('/shelter_dashboard')

@app.route('/pet/<int:id>')
def show_pet(id):
    if 'foster_id' not in session:
        return redirect('/logout')
    return render_template('show_pet.html',foster=Foster.get_by_id({'id': session['foster_id']}), pet=Pet.get_one({'id': id}))

