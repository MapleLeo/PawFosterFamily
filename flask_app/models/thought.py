from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Thought:
    db = 'thoughts'
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_firstname = data['first_name']

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO thoughts (content, user_id) VALUES (%(content)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM thoughts LEFT JOIN users on thoughts.user_id = users.id;'
        results = connectToMySQL(cls.db).query_db(query)
        all_thoughts = []
        for row in results:
            all_thoughts.append(cls(row))
        return all_thoughts

    @classmethod
    def like_count_dict(cls):
        query = 'SELECT thought_id, count(*) as count FROM users_likes_thoughts group by thought_id;'
        results = connectToMySQL(cls.db).query_db(query)
        like_count_dict = {}
        for row in results:
            like_count_dict[row['thought_id']] = row['count']
        return like_count_dict

    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM thoughts WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def destroy(cls,data):
        query = 'DELETE FROM thoughts WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def thoughts_for_user(cls,data):
        query = 'SELECT * FROM thoughts WHERE user_id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def like(cls,data):
        query = 'INSERT INTO users_likes_thoughts (thought_id, user_id) VALUES (%(thought_id)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def unlike(cls,data):
        query = 'DELETE FROM users_likes_thoughts WHERE user_id = %(user_id)s AND thought_id = %(thought_id)s;'
        return connectToMySQL(cls.db).query_db(query, data)
        
    @staticmethod
    def validate_thought(thought):
        is_valid = True
        if len(thought['content']) == 0:
            is_valid = False
            flash("Thought is required","thought")
        if len(thought['content']) < 5:
            is_valid = False
            flash("Thought must be at least 5 characters","thought") 
        return is_valid