from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api, reqparse, abort
import mysql.connector
from flask_jwt import JWT , jwt_required  
from functools import wraps
from PIL import Image
from captcha.image import ImageCaptcha
import numpy as np
import matplotlib.pyplot as plt
import random
import os
import time

from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp


app = Flask(__name__)
api = Api(app)
# app.secret_key = 'jose'
app.config['SECRET_KEY'] = 'hardsecretkey'




mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="flaskcodeloop"
)

mycursor = mydb.cursor()





class Captcha():
    def captch(): 
        number = ['0','1','2','3','4','5','6','7','8','9']
        MAX_CAPTCHA = 6
        WIDTH=100
        HEIGHT=30

        image = ImageCaptcha(width=WIDTH, height=HEIGHT, font_sizes=[30])

        captcha_text = []
        for i in range(MAX_CAPTCHA):
            c = random.choice(number)
            captcha_text.append(c)

        captcha_text = ''.join(captcha_text)
        captcha = image.generate(captcha_text)
        captcha_image = Image.open(captcha)
        captcha_image = np.array(captcha_image)
        # image.write(captcha_text, str(i)+'_'+captcha_text + '.png') 
        ts=time.time()
        mycursor.execute("""INSERT INTO `captch`(`user`,`code`) VALUES ('%s','%s') """%(ts ,captcha_text))
        mydb.commit()
        
        plt.imshow(captcha_image)
        plt.show()

        

ti = time.time()
mycursor.execute("""SELECT * FROM `captch` WHERE `code`= '%s' """%(codecap))
codeend = mycursor.fetchall() 

class User(object):
    def __init__(self, _id , username, password):
        self.id = _id
        self.username = username
        self.password = password

    # def __str__(self):
    #     return "User(id='%s')" % self.id


users = [
    User(1,'ali', 'FDGXF5454'),
    User(2,'reza', 'zxcv'),
    User(3,'mohsen', '354dsfs')
]

# mycursor.execute("""select id, username, password
# from user_info 
# where id = id""")
# users = mycursor.fetchall()



userid_mapping = {u.id:u for u in users}
username_mapping = {u.username:u for u in users}




def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)

jwt = JWT(app, authenticate, identity)


class Home(Resource):
    
    def get(self):
        Captcha.captch()

        return "hi"

    def post(self):
        
        json_data = request.get_json(force=True)
        codecap = json_data['captch'] 
        mycursor.execute("""SELECT * FROM `captch` WHERE `code`= '%s' """%(codecap))
        codeend = mycursor.fetchall()
        if len(codeend) == 0:
            return "goodbye"
        else:
            return "hello"
                
       
        


class HelloWorld(Resource):
    @jwt_required()

    def get(self):
        mycursor.execute("""select movie_name, Director, date  from movie """)
        movie = mycursor.fetchall()
        return jsonify(movie)

        

    def post(self):
        pass
        


api.add_resource(Home, '/')
api.add_resource(HelloWorld, '/movie')






  

if __name__ == "__main__":
	app.run(debug=True)
 


