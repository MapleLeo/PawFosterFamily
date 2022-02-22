from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.foster import Foster

class Application:
    db = 'pawfosterfamily'
    def __init__(self,data):
        self.id = data['id']
        self.status = data['status']
        self.show = data['show']
        self.foster_id = data['foster_id']
        self.pet_id = data['pet_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO applications (status, foster_id, pet_id) VALUES (%(status)s, %(foster_id)s, %(pet_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_foster(cls, foster_id):
        query = 'SELECT * FROM applications LEFT JOIN pets on applications.pet_id = pets.id where applications.foster_id = %(foster_id)s AND `show` = 1;'
        results = connectToMySQL(cls.db).query_db(query, {'foster_id': foster_id})
        applications = []
        for row in results:
            applications.append({
                'id': row['id'],
                'pet_name': row['name'],
                'status': row['status'],
            })
        return applications
    
    @classmethod
    def get_by_shelter_with_pet_and_foster(cls, shelter_id):
        query = 'SELECT applications.id as applications_id, pets.name, fosters.* FROM applications '\
            'LEFT JOIN pets on applications.pet_id = pets.id '\
            'LEFT JOIN fosters on applications.foster_id = fosters.id '\
            'where pets.shelter_id = %(shelter_id)s AND '\
            'applications.status = "PENDING"'
        # SELECT * FROM applications LEFT JOIN pets on applications.pet_id = pets.id LEFT JOIN fosters on applications.foster_id = fosters.id where pets.shelter_id = 2;'
        results = connectToMySQL(cls.db).query_db(query, {'shelter_id': shelter_id})
        applications = []
        for row in results:
            applications.append({
                'application_id': row['applications_id'],
                'pet_name': row['name'],
                'foster': Foster(row),
            })
        print(applications)
        return applications
    
    
    @classmethod
    def mark_read(cls, id):
        query = 'update applications set `show` = 0 where id=%(id)s;'
        return connectToMySQL(cls.db).query_db(query, {'id': id})
    
    @classmethod
    def set_status(cls, id, status):
        query = 'update applications set `status` = %(status)s where id=%(id)s;'
        return connectToMySQL(cls.db).query_db(query, {'id': id, 'status': status})