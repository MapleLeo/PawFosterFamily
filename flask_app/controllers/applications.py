from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.application import Application

@app.route('/application/<int:id>/approve', methods=['POST'])
def approve_application(id):
    Application.set_status(id, "APPROVED")
    return redirect('/shelter/dashboard')

@app.route('/application/<int:id>/reject', methods=['POST'])
def reject_application(id):
    Application.set_status(id, "REJECTED")
    return redirect('/shelter/dashboard')
