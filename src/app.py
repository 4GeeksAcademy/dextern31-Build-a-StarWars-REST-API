"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Characters, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


#[GET] /people Get a list of all the people in the database
@app.route("/people", methods=['GET'])
def getPeople():
    people = Characters.query.all()
    allPeople = list(map(lambda x: x.serialize(), people))

    return jsonify(allPeople), 200

#[GET] /people/<int:people_id> Get a one single people information
@app.route("/people/<int:people_id>", methods=['GET'])
def getSinglePerson(people_id):
    getPerson = Characters.query.get(people_id)
    if getPerson == None:
        response_body = {
            "msg": "Character does not exist"
        } 
        return jsonify(response_body), 400
    
    person = getPerson.serialize()

    return jsonify(person), 200

#[GET] /planets Get a list of all the planets in the database
@app.route("/planets", methods=['GET'])
def getPlanets():
    planet = Planets.query.all()
    allPlanets = list(map(lambda x: x.serialize(), planet))

    return jsonify(allPlanets), 200

#[GET] /planets/<int:planet_id> Get one single planet information
@app.route("/planets/<int:planet_id>", methods=['GET'])
def getSinglePlanets(planet_id):
    getPlanet = Planets.query.get(planet_id)
    if getPlanet == None:
        response_body = {
            "msg": "Planet does not exist"
        }
        return jsonify(response_body), 400
    
    planet = getPlanet.serialize()

    return jsonify(planet), 200

#[GET] /users Get a list of all the blog post users
@app.route("/users", methods=['GET'])
def getUsers():
    users = User.query.all()
    allUsers = list(map(lambda x: x.serialize(), users))

    return jsonify(allUsers), 200

#[GET] /users/favorites Get all the favorites that belong to the current user.
@app.route("/users/favorites", methods=['GET'])
def getFavorites():
    userFavorites = Favorites.query.filter_by(user_id = 1)
    favorites = list(map(lambda x: x.serialize(), userFavorites))

    return jsonify(favorites), 200

#[POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id.
@app.route("/favorite/planet/<int:planet_id>", methods=['POST'])
def addFavoritePlanet(planet_id):    

    planet  = Planets.query.get(planet_id)
    if planet == None:
        response_body = {
            "msg": "Planet does not exist"
        }
        return jsonify(response_body), 400

    favorite = Favorites.query.filter_by(user_id=1, planet_id = planet_id).first()
    if favorite != None:
        response_body = {
            "msg": "Planet is already a favorite"
        }
        return jsonify(response_body), 400
    favoritePlanet = Favorites(user_id=1, planet_id=planet_id)
    db.session.add(favoritePlanet)
    db.session.commit()

    response_body = {
        "msg": "Favorite successfully added "
    }

    return jsonify(response_body), 200

#[POST] /favorite/people/<int:people_id> Add new favorite people to the current user with the people id = people_id.
@app.route("/favorite/people/<int:people_id>", methods=['POST'])
def addFavoritePerson(people_id):
    people = Characters.query.get(people_id)
    if people == None:
        response_body = {
            "msg": "Character does not exist"
        }
        return jsonify(response_body), 400
    
    favorite = Favorites.query.filter_by(user_id=1, character_id = people_id).first()
    if favorite != None:
        response_body = {
            "msg": "Character is already a favorite"
        }
        return jsonify(response_body), 400

    favoritePerson = Favorites(user_id=1, character_id=people_id)
    db.session.add(favoritePerson)
    db.session.commit()

    response_body = {
        "msg": "Favorite successfully added "
    }

    return jsonify(response_body), 200

#[DELETE] /favorite/planet/<int:planet_id> Delete favorite planet with the id = planet_id.
@app.route("/favorite/planet/<int:planet_id>", methods=['DELETE'])
def delFavoritePlanet(planet_id):
    planet  = Planets.query.get(planet_id)
    if planet == None:
        response_body = {
            "msg": "Planet does not exist"
        }
        return jsonify(response_body), 400
    
    favorite = Favorites.query.filter_by(user_id = 1, planet_id = planet_id).first()
    if favorite == None:
        response_body = {
            "msg": "Planet is not a favorite"
        }
        return jsonify(response_body), 400

    db.session.delete(favorite)
    db.session.commit()

    response_body = {
        "msg": "Favorite successfully deleted "
    }

    return jsonify(response_body), 200

#[DELETE] /favorite/people/<int:people_id> Delete favorite people with the id = people_id.
@app.route("/favorite/people/<int:people_id>", methods=['DELETE'])
def delFavoritePerson(people_id):
    people = Characters.query.get(people_id)
    if people == None:
        response_body = {
            "msg": "Character does not exist"
        }
        return jsonify(response_body), 400
    
    favorite = Favorites.query.filter_by(user_id = 1, character_id = people_id).first()
    if favorite == None:
        response_body = {
            "msg": "Character is not a favorite"
        }
        return jsonify(response_body), 400
    
    db.session.delete(favorite)
    db.session.commit()

    response_body = {
        "msg": "Favorite successfully deleted "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
