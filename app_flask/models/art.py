from app_flask import app
from app_flask.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from app_flask.models.user import User
import re 


class Art:
    db = "artdb"
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.type = data["type"]
        self.creation = data["creation"]
        self.user_id = data['user_id']
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM arts;"
        results = connectToMySQL(cls.db).query_db(query)
        arts = []
        for row in results:
            art = cls(row)
            arts.append(art)
            
        return arts


    @classmethod
    def get_users_arts(cls, data):
        query = "SELECT * FROM arts WHERE arts.user_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        arts=[]
        for row in results:
            art = cls(row)
            arts.append(art)
        return arts


    @classmethod
    def create_valid_arts(cls, data):
        
        query = "INSERT INTO arts (title, description, type, creation, user_id) VALUES (%(title)s, %(description)s, %(type)s, %(creation)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
        

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM arts JOIN users ON arts.user_id=users.id WHERE arts.id=%(id)s"
        
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        row = results[0]
        arts = cls(row)
        user_data ={
                    "id": row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "image": row["image"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"]
                }
        user = User(user_data)
        arts.user = user
        return arts

    @classmethod
    def delete_arts_by_id(cls, arts_id):

        data = {"id": arts_id}
        query = "DELETE from arts WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query,data)

        return arts_id


    @classmethod
    def update_arts(cls, data, art_id, user_id):
        
        arts = cls.get_one(art_id)
        if arts.user_id != user_id["id"]:
            flash("The one who creates it can only update it")
            return False
        if not cls.is_valid(data):
            return False
        
        
        query = "UPDATE arts SET title = %(title)s, description = %(description)s, type = %(type)s, creation = %(creation)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
        
        
        

    @staticmethod
    def is_valid(paintings):
        valid = True
        if len(paintings['title']) < 2:
            flash("Enter 2 or more characters")
            valid = False
        if len(paintings['description']) < 10:
            flash("Please enter more than 10 characters, add more details")
            valid = False
        if len(paintings['type']) < 0:
            flash("Enter a valid type")
            valid = False
        return valid