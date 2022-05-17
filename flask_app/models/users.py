from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data): 
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @staticmethod
    def validate_user(data):
        is_valid = True
        
        # confirm that the first name length is between 3 and 30 characters
        if len(data["first_name"]) < 3 or len(data["first_name"]) > 30:
            is_valid = False
            flash("first name must be at least 3 characters, and at most 30 character")

        # confirm that the last name length is between 3 and 30 characters
        if len(data["last_name"]) < 3 or len(data["last_name"]) > 30:
            is_valid = False
            flash("last name must be at least 3 characters, and at most 30 character")

        # confirm that the email meets the email criteria
        if not EMAIL_REGEX.match(data["email"]):
            is_valid = False
            flash("Please provide a valid user email address")

        # email must be unique
        # if len(User.get_user_by_email({'username' : data['username']})) != 0: would be needed if data is not already a dictionary
        if len(User.get_user_by_email(data)) != 0:
            is_valid = False
            flash("Email already tied to an exisitng account")

        # password must be at least 8 characters
        if len(data["password"]) < 8:
            is_valid = False
            flash("Password must be at least 8 character")

        # password and confirm must match exactly
        if data["password"] != data["confirm_password"]: 
            is_valid = False
            flash("Passwords do not match one another")
        return is_valid

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        results = connectToMySQL('login_and_registration').query_db(query, data)
        return results

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('login_and_registration').query_db(query, data)
        
        users = []
        for item in results:
            users.append(User(item))
        return users

