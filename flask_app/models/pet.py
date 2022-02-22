from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Pet:
    db = 'pawfosterfamily'
    def __init__(self,data):
        self.id = data['id']
        self.img = data['img']
        self.name = data['name']
        self.age = data['age']
        self.foster_time_needed = data['foster_time_needed']
        self.foster_grade = data['foster_grade']
        self.description = data['description']
        self.shelter_id = data['shelter_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO pets (name, age, foster_time_needed, foster_grade, description, shelter_id) VALUES (%(name)s, %(age)s, %(foster_time_needed)s, %(foster_grade)s, %(description)s, %(shelter_id)s);'
        # query = 'INSERT INTO pets (img, name, age, foster_time_needed, foster_grade, description, shelter_id) VALUES (%(img)s, %(name)s, %(age)s, %(foster_time_needed)s, %(foster_grade)s, %(description)s, %(shelter_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_shelter(cls, data):
        query = 'SELECT * FROM pets WHERE shelter_id = %(shelter_id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        all_pets = []
        for row in results:
            all_pets.append(cls(row))
        return all_pets

    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM pets WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_all_available(cls):
        query = 'SELECT * FROM pets WHERE (SELECT count(*) from applications where applications.pet_id = pets.id AND applications.status = "APPROVED") = 0;'
        results = connectToMySQL(cls.db).query_db(query)
        all_pets = []
        for row in results:
            all_pets.append(cls(row))
        return all_pets

    @classmethod
    def destroy(cls,data):
        query = 'DELETE FROM pets WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def pets_for_user(cls,data):
        query = 'SELECT * FROM pets WHERE user_id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_by_foster(cls, foster_id):
        query = 'SELECT * FROM pets JOIN applications on applications.pet_id = pets.id where applications.status = "APPROVED" and applications.foster_id = %(foster_id)s;'
        results = connectToMySQL(cls.db).query_db(query, { 'foster_id': foster_id })
        all_pets = []
        for row in results:
            all_pets.append(cls(row))
        return all_pets

    @staticmethod
    def validate_pet(pet):
        is_valid = True
        if len(pet['name']) == 0:
            is_valid = False
            flash("Name is required","pet")
        if len(pet['foster_time_needed']) < 0:
            is_valid = False
            flash("Foster time needed is required","pet") 
        return is_valid