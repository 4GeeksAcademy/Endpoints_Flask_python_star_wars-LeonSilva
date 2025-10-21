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
from models import db, User, Characters, Planets, Starships, FavoriteCharacters, FavoritePlanets, FavoriteStarships
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


@app.route('/users',methods=['GET'])
def get_all_users():
    
    users = User.query.all()

    if users is None:
        return jsonify({
            "msn": "No se han encontrado usuarios"
        }), 404
    
    users_data = []

    for x in users:
        users_data.append(x.serialize()) 
    
    return jsonify({"users_data": users_data}), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    
    user = User.query.get(user_id)
    
    if user is None:
        return jsonify({
            "msn" : f"No se ah encontrado el usuario: {user_id}"
            }), 404
    
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

@app.route('/characters',methods = ['GET'])
def get_all_characters():
    
    characters = Characters.query.all()
    
    if characters is None:
        return jsonify({"msn":"No hay ningun personaje registrado"}), 404

    characters_list = []

    for x in characters:
        characters_list.append(x.serialize())

    return jsonify({
        "characters_data": characters_list
    }), 200

@app.route('/character/<int:character_id>',methods = ['GET'])
def get_character(character_id):
    
    character = Characters.query.get(character_id)
    
    if character is None:
        return jsonify({"msn":"No hay ningun personaje registrado"}), 404

    character = character.serialize()

    return jsonify({
        "characters_data": character
    }), 200

@app.route('/planets',methods = ['GET'])
def get_all_planets():
    
    planets = Planets.query.all()
    
    if planets is None:
        return jsonify({"msn":"No hay ningun personaje registrado"}), 404

    planets_list = []

    for x in planets:
        planets_list.append(x.serialize())

    return jsonify({
        "planets_data": planets_list
    }), 200


@app.route('/planet/<int:planet_id>',methods = ['GET'])
def get_planet(planet_id):
    
    planet = Planets.query.get(planet_id)
    
    if planet is None:
        return jsonify({"msn":"No hay ningun personaje registrado"}), 404
    
    planet = planet.serialize()
    
    return jsonify({
        "planet_data": planet
    }), 200

@app.route('/starships',methods = ['GET'])
def get_all_starships():
    
    starships = Starships.query.all()
    
    if starships is None:
        return jsonify({"msn":"No hay ninguna nave registrada"}), 404

    starships_list = []

    for x in starships:
        starships_list.append(x.serialize())

    return jsonify({
        "starships_data": starships_list
    }), 200

@app.route('/starship/<int:starship_id>',methods = ['GET'])
def get_starship(starship_id):
    
    starship = Starships.query.get(starship_id)
    
    if starship is None:
        return jsonify({"msn":"No hay ningun personaje registrado"}), 404
    
    starship = starship.serialize()
    
    return jsonify({
        "starship_data": starship
    }), 200

@app.route('/characters',methods=['POST'])
def post_character():
    
    body = request.get_json(silent=True)
    new_character = Characters()
    
    if body is None:
        return jsonify({"msn":"no se encontró un body JSON"}), 400
    
    if "name" not in body:
        return jsonify({"msn":"nombre requerido"}), 400
    new_character.name = body["name"]
    if "weight" in body:
        new_character.weight = int(body["weight"])
    if "height" in body:
        new_character.height = int(body["height"])
    
    db.session.add(new_character)
    db.session.commit()
    
    return jsonify({"personaje_creado": new_character.serialize()}), 200

@app.route('/planets',methods=['POST'])
def post_planet():
    
    body = request.get_json(silent=True)
    new_planet = Planets()
    
    if body is None:
        return jsonify({"msn":"no se encontró un body JSON"}), 400
    
    if "name" not in body:
        return jsonify({"msn":"nombre requerido"}), 400
    new_planet.name = body["name"]
    if "population" in body:
        new_planet.weight = int(body["weight"])
    if "size" in body:
        new_planet.height = int(body["height"])
    
    db.session.add(new_planet)
    db.session.commit()
    
    return jsonify({"planeta_creado": new_planet.serialize()}), 200

@app.route('/starships',methods=['POST'])
def post_starship():
    
    body = request.get_json(silent=True)
    new_starship = Starships()
    
    if body is None:
        return jsonify({"msn":"no se encontró un body JSON"}), 400
    
    if "name" not in body:
        return jsonify({"msn":"nombre requerido"}), 400
    new_starship.name = body["name"]
    if "speed" in body:
        new_starship.weight = int(body["weight"])
    if "size" in body:
        new_starship.height = int(body["height"])
    
    db.session.add(new_starship)
    db.session.commit()
    
    return jsonify({"nave_creada": new_starship.serialize()}), 200

@app.route('/user/<int:user_id>/favorite/character/<int:character_id>',methods=['POST'])
def add_favorite_character(user_id,character_id):
    
    user = User.query.get(user_id)
    character = Characters.query.get(character_id)

    if not user or not character:
        return jsonify({"msn":"no se encontró el user o character (o ambos)"}), 400

    is_fav_existing = FavoriteCharacters.query.filter_by(user_id = user.id, character_id = character.id).first()

    if is_fav_existing:
        return jsonify({"msn": "El usuario ya tiene este personaje en favoritos"}), 409

    new_favorite  = FavoriteCharacters(user_id = user.id, character_id = character.id  )
    db.session.add(new_favorite)
    db.session.commit()

    fav_user_serialized = []

    user_fav = user.favorite_characters_list

    for x in user_fav:
        fav_user_serialized.append(x.character.serialize())

    return jsonify({
        "user_fav_list": fav_user_serialized 
    }), 200

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>',methods=['POST'])
def add_favorite_planet(user_id,planet_id):
    
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if not user or not planet:
        return jsonify({"msn":"no se encontró el user o planet (o ambos)"}), 400

    is_fav_existing = FavoritePlanets.query.filter_by(user_id = user.id, planet_id = planet.id).first()

    if is_fav_existing:
        return jsonify({"msn": "El usuario ya tiene este personaje en favoritos"}), 409

    new_favorite  = FavoritePlanets(user_id = user.id, planet_id = planet.id  )
    db.session.add(new_favorite)
    db.session.commit()

    fav_user_serialized = []

    user_fav = user.favorite_planets_list

    for x in user_fav:
        fav_user_serialized.append(x.planet.serialize())

    return jsonify({
        "user_fav_list": fav_user_serialized 
    }), 200

@app.route('/user/<int:user_id>/favorite/starship/<int:starship_id>',methods=['POST'])
def add_favorite_starship(user_id,starship_id):
    
    user = User.query.get(user_id)
    starship = Starships.query.get(starship_id)

    if not user or not starship:
        return jsonify({"msn":"no se encontró el user o starship (o ambos)"}), 400

    is_fav_existing = FavoriteStarships.query.filter_by(user_id = user.id, starship_id = starship.id).first()

    if is_fav_existing:
        return jsonify({"msn": "El usuario ya tiene este personaje en favoritos"}), 409

    new_favorite  = FavoriteStarships(user_id = user.id, starship_id = starship.id  )
    db.session.add(new_favorite)
    db.session.commit()

    fav_user_serialized = []

    user_fav = user.favorite_characters_list

    for x in user_fav:
        fav_user_serialized.append(x.character.serialize())

    return jsonify({
        "user_fav_list": fav_user_serialized 
    }), 200

@app.route('/user/<int:user_id>/favorite/character/<int:character_id>',methods=['DELETE'])
def delete_favorite_character(user_id,character_id):
    
    user = User.query.get(user_id)
    character = Characters.query.get(character_id)

    if not user or not character:
        return jsonify({"msn":"no se encontró el user o character (o ambos)"}), 400

    is_fav_existing = FavoriteCharacters.query.filter_by(user_id = user.id, character_id = character.id).first()

    if not is_fav_existing:
        return jsonify({"msn": "El usuario no tiene este personaje en favoritos"}), 409

    db.session.delete(is_fav_existing)
    db.session.commit()

    fav_user_serialized = []

    user_fav = user.favorite_characters_list

    for x in user_fav:
        fav_user_serialized.append(x.character.serialize())

    return jsonify({
        "user_fav_list": fav_user_serialized 
    }), 200

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>',methods=['DELETE'])
def delete_favorite_planet(user_id,planet_id):
    
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if not user or not planet:
        return jsonify({"msn":"no se encontró el user o planet (o ambos)"}), 400

    is_fav_existing = FavoritePlanets.query.filter_by(user_id = user.id, planet_id = planet.id).first()

    if not is_fav_existing:
        return jsonify({"msn": "El usuario no tiene este personaje en favoritos"}), 409

    db.session.delete(is_fav_existing)
    db.session.commit()

    fav_user_serialized = []

    user_fav = user.favorite_planets_list

    for x in user_fav:
        fav_user_serialized.append(x.planet.serialize())

    return jsonify({
        "user_fav_list": fav_user_serialized 
    }), 200

@app.route('/user/<int:user_id>/favorite/starship/<int:starship_id>',methods=['DELETE'])
def delete_favorite_starship(user_id,starship_id):
    
    user = User.query.get(user_id)
    starship = Starships.query.get(starship_id)

    if not user or not starship:
        return jsonify({"msn":"no se encontró el user o starship (o ambos)"}), 400

    is_fav_existing = FavoriteStarships.query.filter_by(user_id = user.id, starship_id = starship.id).first()

    if not is_fav_existing:
        return jsonify({"msn": "El usuario no tiene este personaje en favoritos"}), 409

    db.session.delete(is_fav_existing)
    db.session.commit()

    fav_user_serialized = []

    user_fav = user.favorite_starships_list

    for x in user_fav:
        fav_user_serialized.append(x.starship.serialize())

    return jsonify({
        "user_fav_list": fav_user_serialized 
    }), 200

@app.route('/user/<int:user_id>/favorite/character/<int:character_id>/new_character/<int:new_character_id>',methods=['PUT'])
def put_favorite_character(user_id, character_id, new_character_id):
    
    user = User.query.get(user_id)
    character = Characters.query.get(character_id)
    new_character = Characters.query.get(new_character_id)

    if not user or not character:
        return jsonify({"msn":"no se encontró el user o character (o ambos)"}), 400

    if not new_character:
        return jsonify({"msn":"no se encontró el nuevo character por el que quieres cambiar"}), 400

    is_fav_existing = FavoriteCharacters.query.filter_by(user_id = user.id, character_id = character.id).first()
    if not is_fav_existing:
        return jsonify({"msn": "El usuario no tiene este personaje en favoritos"}), 409
    
    is_new_fav_existing = FavoriteCharacters.query.filter_by(user_id = user.id, character_id = new_character.id).first()
    if is_new_fav_existing:
        return jsonify({"msn": "El usuario ya tiene este personaje en favoritos"}), 409
    else:
        is_fav_existing.character_id = new_character.id
    db.session.commit()

    fav_user_serialized = []

    user_fav = user.favorite_characters_list

    for x in user_fav:
        fav_user_serialized.append(x.character.serialize())

    return jsonify({
        "user_fav_list": fav_user_serialized 
    }), 200

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>/new_planet/<int:new_planet_id>',methods=['PUT'])
def put_favorite_planet(user_id, planet_id, new_planet_id):
    
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)
    new_planet = Planets.query.get(new_planet_id)

    if not user or not planet:
        return jsonify({"msn":"no se encontró el user o planet (o ambos)"}), 400

    if not new_planet:
        return jsonify({"msn":"no se encontró el nuevo planet por el que quieres cambiar"}), 400

    is_fav_existing = FavoritePlanets.query.filter_by(user_id = user.id, planet_id = planet.id).first()
    if not is_fav_existing:
        return jsonify({"msn": "El usuario no tiene este personaje en favoritos"}), 409
    
    is_new_fav_existing = FavoritePlanets.query.filter_by(user_id = user.id, planet_id = new_planet.id).first()
    if is_new_fav_existing:
        return jsonify({"msn": "El usuario ya tiene este personaje en favoritos"}), 409
    else:
        is_fav_existing.planet_id = new_planet.id
    db.session.commit()

    fav_user_serialized = []

    user_fav = user.favorite_planets_list

    for x in user_fav:
        fav_user_serialized.append(x.planet.serialize())

    return jsonify({
        "user_fav_list": fav_user_serialized 
    }), 200

@app.route('/user/<int:user_id>/favorite/starship/<int:starship_id>/new_starship/<int:new_starship_id>',methods=['PUT'])
def put_favorite_starship(user_id, starship_id, new_starship_id):
    
    user = User.query.get(user_id)
    starship = Starships.query.get(starship_id)
    new_starship = Starships.query.get(new_starship_id)

    if not user or not starship:
        return jsonify({"msn":"no se encontró el user o starship (o ambos)"}), 400

    if not new_starship:
        return jsonify({"msn":"no se encontró el nuevo starship por el que quieres cambiar"}), 400

    is_fav_existing = FavoriteStarships.query.filter_by(user_id = user.id, starship_id = starship.id).first()
    if not is_fav_existing:
        return jsonify({"msn": "El usuario no tiene este personaje en favoritos"}), 409
    
    is_new_fav_existing = FavoriteStarships.query.filter_by(user_id = user.id, starship_id = new_starship.id).first()
    if is_new_fav_existing:
        return jsonify({"msn": "El usuario ya tiene este personaje en favoritos"}), 409
    else:
        is_fav_existing.starship_id = new_starship.id
    db.session.commit()

    fav_user_serialized = []

    user_fav = user.favorite_starships_list

    for x in user_fav:
        fav_user_serialized.append(x.starship.serialize())

    return jsonify({
        "user_fav_list": fav_user_serialized 
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
