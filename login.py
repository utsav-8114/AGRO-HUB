from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
import requests
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'#for creating the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False #for turning modification tracking off
db=SQLAlchemy(app)#initializing the database
class User(db.Model):#Defines a database table called user
    id= db.Column(db.Integer,primary_key=True)#makes unique auto incrementing id's
    username=db.Column(db.String(100),unique=True,nullable=False)#making unique usernames
    password=db.Column(db.String(100),nullable=False)#making passwords(saving as plain text for now)
    def __repr__(self):#(used for debugging)
        return f"<User {self.username}>"

with app.app_context():
    db.create_all()
#making login route

@app.route("/login",methods=["POST"])
def cust_login(): 
    data=request.get_json()
    cust_username=data.get("username")
    cust_pass=data.get("password")
    user=User.query.filter_by(username=cust_username).first()
    if user and check_password_hash(user.password,cust_pass):
        return jsonify({"message":"login is successful!","username":user.username}),200
    else:
        return jsonify({"message":"Invalid credentials "}),401
#making register route

@app.route("/register",methods=["POST"])
def cust_register():
    data=request.get_json()
    cust_username=data.get("username")
    cust_pass= data.get("password")
    hashed_password = generate_password_hash(cust_pass)
    
    user=User(username=cust_username,password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify("User registered successfully")

#making users table route

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()  # Get all users from the database
    # Convert the users to a list of dictionaries
    users_list = [{"id": user.id, "username": user.username, "password": user.password} for user in users]
    return jsonify(users_list)  # Return the list of users as JSON




if __name__ == "__main__":
    app.run(debug=True)