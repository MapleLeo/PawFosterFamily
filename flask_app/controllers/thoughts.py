from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.thought import Thought
from flask_app.models.user import User

@app.route('/create/thought',methods=['POST'])
def add_thought():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Thought.validate_thought(request.form):
        return redirect('/dashboard')
    data = {
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    id=Thought.save(data)
    return redirect('/dashboard')

@app.route('/destroy/thought/<int:id>')
def destroy_thought(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    Thought.destroy(data)
    return redirect('/dashboard')

@app.route('/likes/<int:id>',methods=['POST'])
def likes(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id'],
        'thought_id': id
    }
    Thought.like(data)
    return redirect('/dashboard')

@app.route('/unlikes/<int:id>',methods=['POST'])
def unlikes(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id'],
        'thought_id': id
    }
    Thought.unlike(data)
    return redirect('/dashboard')
        
