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
from models import db, User, Users, Characters, Planets, FavoriteCharacters, FavoritePlanets
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/users', methods=['GET'])
def get_users():
    all_users = db.session.execute(select(Users)).scalars().all()
    all_users = list(map(lambda x: x.serialize(), all_users))

    return jsonify(all_users), 200

@app.route('/users/favorites', methods=['GET'])
def get_users_favorites():
    favorite_planets = db.session.execute(select(FavoritePlanets)).scalars().all()
    favorite_planets = list(map(lambda x: x.serialize(), favorite_planets))
    favorite_characters = db.session.execute(select(FavoriteCharacters)).scalars().all()
    favorite_characters = list(map(lambda x: x.serialize(), favorite_characters))
    

    return jsonify(favorite_characters, favorite_planets)

@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters = db.session.execute(select(Characters)).scalars().all()
    all_characters= list(map(lambda x: x.serialize(), all_characters))

    return jsonify(all_characters), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    error_response = {
        "error": "This character doesn't exist",
    }
    try:
        character = db.session.get(Characters, character_id)
        return jsonify(character.serialize()), 200
    except AttributeError:
        return jsonify(error_response), 400

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = db.session.execute(select(Planets)).scalars().all()
    all_planets= list(map(lambda x: x.serialize(), all_planets))

    return jsonify(all_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    error_response = {
        "error": "This planet doesn't exist",
    }

    try:
        planet = db.session.get(Planets, planet_id)
        return jsonify(planet.serialize()), 200
    except AttributeError:
        return jsonify(error_response), 400
    

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    
    planet = FavoritePlanets(id_user=1, id_planets=planet_id, active=True)
    try:
        db.session.add(planet)
        db.session.commit()
    
        return "Planet ADDED to favorites", 201

    except IntegrityError:
        db.session.rollback()
        return "Error. This planet is already in your favorites", 400


@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    
    character = FavoriteCharacters(id_user=1, id_characters=character_id, active=True)
    try:
        db.session.add(character)
        db.session.commit()

        return "Character ADDED to favorites", 201

    except IntegrityError:
        db.session.rollback()
        return "Error. This character is already in your favorites", 400
    

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def del_favorite_character(character_id):
    
    favorites = db.session.get(FavoriteCharacters, character_id)
    try:
        db.session.delete(favorites)
        db.session.commit()

        return "Character DELETED from favorites", 201

    except UnmappedInstanceError:
        db.session.rollback()
        return "Error. This character is already DELETED", 401


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def del_favorite_planet(planet_id):
    
    favorites = db.session.get(FavoritePlanets, planet_id)
    try:
        db.session.delete(favorites)
        db.session.commit()

        return "Planet DELETED from favorites", 201

    except UnmappedInstanceError:
        db.session.rollback()
        return "Error. This planet is already DELETED", 401

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
