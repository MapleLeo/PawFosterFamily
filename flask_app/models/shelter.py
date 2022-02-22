from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Shelter:
    db = "pawfosterfamily"
    def __init__(self,data):
        self.id = data['id']
        self.shelter_name = data['shelter_name']
        self.email = data['email']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO shelters (shelter_name, email, city, state, password) VALUES (%(shelter_name)s, %(email)s, %(city)s, %(state)s, %(password)s);'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM shelters;'
        results = connectToMySQL(cls.db).query_db(query)
        shelters = []
        for row in results:
            shelters.append(cls(row))
        return shelters

    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM shelters WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = 'SELECT * FROM shelters WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(shelter):
        is_valid = True
        query = 'SELECT * FROM shelters WHERE email = %(email)s;'
        results = connectToMySQL(Shelter.db).query_db(query,shelter)
        if len(results) >= 1:
            flash("Email already taken.","shelter_register")
            is_valid = False
        if not EMAIL_REGEX.match(shelter['email']):
            flash("Invalid Email!!!","shelter_register")
            is_valid = False
        if len(shelter['shelter_name']) < 2:
            flash("Shelter name must be at least 2 characters","shelter_register")
            is_valid = False
        if len(shelter['city']) < 1:
            flash("City is required","shelter_register")
            is_valid = False    
        if len(shelter['password']) < 8:
            flash("Password must be at least 8 characters","shelter_register")
            is_valid = False
        if shelter['password'] != shelter['confirm']:
            flash("Passwords don't match","shelter_register")
        return is_valid