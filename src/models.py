from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite_characters_list: Mapped[list['FavoriteCharacters']] = relationship(
        back_populates='user')
    favorite_planets_list: Mapped[list['FavoritePlanets']] = relationship(
        back_populates='user')
    favorite_starships_list: Mapped[list['FavoriteStarships']] = relationship(
        back_populates='user')

    def __repr__(self):
        return f'{self.name}'

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active
        }

class FavoriteCharacters(db.Model):
    __tablename__ = 'favorite_character'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(
        back_populates='favorite_characters_list')
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    character: Mapped['Characters'] = relationship(
        back_populates='favorite_character_by')

    def __repr__(self):
        return f'{self.character}'

class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='favorite_planets_list')
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    planet: Mapped['Planets'] = relationship(
        back_populates='favorite_planet_by')

    def __repr__(self):
        return f'{self.planet}'

class FavoriteStarships(db.Model):
    __tablename__ = 'favorite_starship'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(
        back_populates='favorite_starships_list')
    starship_id: Mapped[int] = mapped_column(ForeignKey('starships.id'))
    starship: Mapped['Starships'] = relationship(
        back_populates='favorite_starship_by')

    def __repr__(self):
        return f'{self.starship}'

class Characters(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[int] = mapped_column(Integer, nullable=True)
    favorite_character_by: Mapped[list['FavoriteCharacters']] = relationship(
        back_populates='character')

    def __repr__(self):
        return f'{self.name}'
    
    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "height": self.height,
            "weight": self.weight,
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=True)
    size: Mapped[int] = mapped_column(Integer, nullable=True)
    favorite_planet_by: Mapped[list['FavoritePlanets']
                               ] = relationship(back_populates='planet')
    
    def __repr__(self):
        return f'{self.name}'
    
    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "population": self.population,
            "size": self.size,
        }

class Starships(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    speed: Mapped[int] = mapped_column(Integer, nullable=True)
    size: Mapped[int] = mapped_column(Integer, nullable=True)
    favorite_starship_by: Mapped[list['FavoriteStarships']] = relationship(
        back_populates='starship')
    
    def __repr__(self):
        return f'{self.name}'
    
    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "speed": self.speed,
            "size": self.size,
        }