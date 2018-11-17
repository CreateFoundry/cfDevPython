#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 14:25:34 2018

@author: vinaymac
"""
import pymysql
from flask import Flask, render_template, json, request
from werkzeug import generate_password_hash, check_password_hash
 
app = Flask(__name__)
 
class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "cfdev"
        password = "P@ssw0rdDev"
        db = "createFoundryDev"
 
        self.connection = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cursorInstance = self.connection.cursor()
    
    def list_employees(self):
       self.cursorInstance.execute("SELECT firstname, lastname, email, mobile, landline, buildingname,streetname, doornumber,area,city,state,postcode FROM customer LIMIT 50")
       result = self.cursorInstance.fetchall()
       return result
   
    def checkUser(self,_email,_password):
        try:
            if _email and _password:
                sql="SELECT user_password FROM userdetails where user_username=%s"
                self.cursorInstance.execute(sql,_email);
                hashedData = self.cursorInstance.fetchall()
                checkUserDetails = check_password_hash(hashedData[0]['user_password'], _password)
                print(checkUserDetails)
                return checkUserDetails
            else:
                return json.dumps({'html':'<span>Enter the required fields</span>'})
        except Exception as e:
            return json.dumps({'error':str(e)})
   
    def callSPUser(self,_name,_email,_password):
        try:
             # validate the received values
             if _name and _email and _password:
                 # All Good, let's call MySQL
                 _hashed_password = generate_password_hash(_password,method='pbkdf2:sha256', salt_length=8)
                 print("Printing the hashed password"+_hashed_password)
                 self.cursorInstance.callproc('sp_createUser',(_name,_email,_hashed_password))
                 data = self.cursorInstance.fetchall()
                 self.connection.commit()
                 print('Returning the data')
                 return data
             else:
                print('Data missing')
                return json.dumps({'html':'<span>Enter the required fields</span>'})
        except Exception as e:
            print('ERROR')
            return json.dumps({'error':str(e)})
        finally:
            self.cursorInstance.close()
            self.connection.close();

# Block to render the landing page
@app.route('/home')
def mainHome():
    return render_template('index.html')
@app.route('/')
def home():
    return render_template('index.html')

# Block to render the user home page
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')


# Block for Sign Up - Render html page
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

# Block for Sign Up - Perform SignUp action with db persistence
@app.route('/signUpUser',methods=['POST'])
def signUp():
    print("Came in Signup method")
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    db = Database()
    details = db.callSPUser(_name,_email,_password);
    if 'Username Exists !!' in details[0]:
        raise InvalidUsage('Username already exists', status_code=410)    
    else:
        return json.dumps({'message':'User created successfully !'})

# Block for Sign In - Render html page
@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

# Block for Sign In - Perform SignIn action with password check
@app.route('/signIn',methods=['POST'])
def signIn():
     _email = request.form['inputEmail']
     _password = request.form['inputPassword']
     db = Database()
     details = db.checkUser(_email,_password);
     if details!=True:
         raise InvalidUsage('User does not exists', status_code=410) 
     else: 
        return json.dumps({'message':'User logged in successfully !'})
    
#    try:
#        _email = request.form['inputEmail']
#        _password = request.form['inputPassword']
#        db = Database()
#        details = db.checkUser(_email,_password);
#        if 'Username Exists !!' in details[0]:
#             raise InvalidUsage('User does not exists', status_code=410) 
#        else:
#            return json.dumps({'message':'User logged in successfully !'})
#     except Exception as e:
#        return json.dumps({'error':str(e)})
 
@app.route('/getAllCustomers')
def employees():
    def db_query():
        db = Database()
        emps = db.list_employees()
        return emps
    res = db_query()
    return render_template('customers.html', result=res, content_type='application/json')

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv



if __name__ == '__main__':
    app.run(debug = True)
#    db = Database()
#    details = db.callSPUser('abiram','ursabi@gmail.com','logmein123');
#    details = db.checkUser('ursabi@gmail.com','logmein123');
#    if details!=True:
#        raise InvalidUsage('User does not exists', status_code=410) 
#    else: 
#        print('User logged in')
   