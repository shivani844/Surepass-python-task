from random import randrange
from flask_mongoengine import MongoEngine
from flask import Flask, jsonify, request
from flask_restx import Api ,Resource
from flask_jwt_extended import (JWTManager,jwt_required,create_access_token,
get_jwt_identity
)

app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'anything_secret'
jwt = JWTManager(app)

app.config["MONGODB_SETTINGS"] = {
    "db" : "test",
    }

db = MongoEngine(app)
class BackendError(Exception):
    pass

@app.route('/token',methods=["GET"])
def token(): 
    key = request.json.get('key') 
    user = request.json.get('user')
    if key == app.config['JWT_SECRET_KEY']:
        access_token = create_access_token(identity = user)
        return jsonify(access_token = access_token)
    else:
        return {"Wrong secret key": "Please enter the right key."}

@api.route('/<pan_number>')
class hello(Resource):
  @jwt_required
  def get(self,pan_number):
    num = randrange(10)

    if num in (8,9):
        try:
            raise BackendError
        except:
            return "Backend Error Occured."
    
    db.disconnect()
    db.connect(host = 'mongodb+srv://sudhanshoosarage:sudhanshoosarage@testcluster.yvkdz.mongodb.net/test?retryWrites=true&w=majority')
    class Users(db.Document):
        pan = db.StringField()
        name = db.StringField()
        dob = db.DateTimeField()
        father_name = db.StringField()
        client_id = db.IntField()
    flag = 0
    for x in Users.objects:
        if x.pan == pan_number:
            user = x
            flag = 1
            break
    if flag == 0:
        return {
            "message":"Pan number is not valid."
        }


            
    if user.pan == pan_number:
        return {
            'pan': user.pan,
            'name': user.name,
            'dob':str(user.dob),
            'father_name': user.father_name,
            'client_id':str(user.client_id)
        }
        
@api.route('/getFromId/<id1>')
class id(Resource):
    @jwt_required
    def get(self,id1):
        db.disconnect()
        db.connect(host = 'mongodb+srv://sudhanshoosarage:sudhanshoosarage@testcluster.yvkdz.mongodb.net/test?retryWrites=true&w=majority')
        class Users(db.Document):
            pan = db.StringField()
            name = db.StringField()
            dob = db.DateTimeField()
            father_name = db.StringField()
            client_id = db.IntField()

        flag = 0
        for x in Users.objects:
            if x.client_id == int(id1):
                flag = 1       
                return {
                    'pan': x.pan,
                    'name': x.name,
                    'dob':str(x.dob),
                    'father_name': x.father_name,
                    'client_id':str(x.client_id)
                }
                break
        if flag == 0:
            return {
                "message": "Entered id is wrong."
            }
        


if __name__ == '__main__':
    app.run(debug = True)