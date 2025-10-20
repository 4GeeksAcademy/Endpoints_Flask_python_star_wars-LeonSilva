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
from models import db, User, Characters, Planets, FavoriteCharacters, FavoritePlanets, FavoriteStarships
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


@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    
    if user is None:
        return jsonify({
            "msn" : f"No se ah encontrado el usuario: {user_id}"
            }),404
    fav_characters = user.favorite_characters_list
    fav_planets = user.favorite_planets_list 
    fav_starships = user.favorite_starships_list

    fav_characters_serialized = []
    fav_planets_serialized = []
    Fav_starships_serialized = []

    for x in fav_characters:
        fav_characters_serialized.append(x.character.serialize())
    
    for x in fav_planets:
        fav_planets_serialized.append(x.planet.serialize())
    
    for x in fav_starships:
        Fav_starships_serialized.append(x.starship.serialize())

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "favorite_characters": fav_characters_serialized,
        "favorite_planets": fav_planets_serialized,
        "favorite_starships": Fav_starships_serialized
    }), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

'''
"favorite_characters": user.favorite_characters_list,
"favorite_planets": user.favorite_planets_list,
"favorite_starships": user.favorite_starships_list
'''
