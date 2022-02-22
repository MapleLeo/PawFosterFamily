from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Foster:
    db = "pawfosterfamily"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO fosters (first_name, last_name, email, city, state, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(city)s, %(state)s, %(password)s);'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM fosters;'
        results = connectToMySQL(cls.db).query_db(query)
        fosters = []
        for row in results:
            fosters.append(cls(row))
        return fosters

    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM fosters WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = 'SELECT * FROM fosters WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(foster):
        is_valid = True
        query = 'SELECT * FROM fosters WHERE email = %(email)s;'
        results = connectToMySQL(Foster.db).query_db(query,foster)
        if len(results) >= 1:
            flash("Email already taken.","foster_register")
            is_valid = False
        if not EMAIL_REGEX.match(foster['email']):
            flash("Invalid Email!!!","foster_register")
            is_valid = False
        if len(foster['first_name']) < 2:
            flash("First name must be at least 2 characters","foster_register")
            is_valid = False
        if len(foster['last_name']) < 2:
            flash("Last name must be at least 2 characters","foster_register")
            is_valid = False
        if len(foster['city']) < 1:
            flash("City is required","foster_register")
            is_valid = False    
        if len(foster['password']) < 8:
            flash("Password must be at least 8 characters","foster_register")
            is_valid = False
        if foster['password'] != foster['confirm']:
            flash("Passwords don't match","foster_register")
        return is_valid