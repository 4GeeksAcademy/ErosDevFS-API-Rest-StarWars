import os
from flask_admin import Admin
from models import db, User, Users, Characters, Planets, FavoriteCharacters, FavoritePlanets
from flask_admin.contrib.sqla import ModelView

class FavoritesCharactersAdmin(ModelView):
    column_list = ('id', 'id_user', 'id_characters', 'active')
    form_columns = ('id_user', 'id_characters', 'active')
    
class FavoritePlanetsAdmin(ModelView):
    column_list = ('id', 'id_user', 'id_planets', 'active')
    form_columns = ('id_user', 'id_planets', 'active')

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')


    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Characters, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(FavoritesCharactersAdmin(FavoriteCharacters, db.session))
    admin.add_view(FavoritePlanetsAdmin(FavoritePlanets, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))