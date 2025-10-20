import os
from flask_admin import Admin
from models import db, User, Characters, FavoriteCharacters, Planets, FavoritePlanets, Starships, FavoriteStarships
from flask_admin.contrib.sqla import ModelView

class UserModelView(ModelView):
    column_auto_select_realted = True # Esto carga las relaciones
    column_list = ['id','name','email','password','is_active','favorite_characters_list','favorite_planets_list','favorite_starships_list']

class CharatersModelView(ModelView):
    column_auto_selected_realted = True # Esto carga las relaciones
    column_list = ['id','name','height','weight','favorite_character_by'] 

class FavoriteCharactersModelView(ModelView):
    column_auto_selected_realted = True # Esto carga las relaciones
    column_list = ['id','user_id','character_id']

class PlanetsModelView(ModelView):
    column_auto_selected_realted = True # Esto carga las relaciones
    column_list = ['id','name','population','size','favorite_planet_by']

class FavoritePlanetsModelView(ModelView):
    column_auto_selected_realted = True # Esto carga las relaciones
    column_list = ['id','user_id','planet_id']

class StarshipsModelView(ModelView):
    column_auto_selected_realted = True # Esto carga las relaciones
    column_list = ['id','name','speed','size','favorite_starship_by']

class FavoriteStarshipsModelView(ModelView):
    column_auto_selected_realted = True # Esto carga las relaciones
    column_list = ['id','user_id','starship_id']


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharatersModelView(Characters, db.session))
    admin.add_view(FavoriteCharactersModelView(FavoriteCharacters, db.session))
    admin.add_view(PlanetsModelView(Planets, db.session))
    admin.add_view(FavoritePlanetsModelView(FavoritePlanets, db.session))
    admin.add_view(StarshipsModelView(Starships, db.session))
    admin.add_view(FavoriteStarshipsModelView(FavoriteStarships, db.session))
    

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session)) Esto es en la version antigua ahora no funciona las relaciones con ella
    # admin.add_view(XModelView(YourModelName,db.session)) Cambia la x por el nombre que le quieras dar a la clase