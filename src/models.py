from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Users(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    subscription: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    last_payment: Mapped[str] = mapped_column(nullable=False)

    favoritecharacters: Mapped[List["FavoriteCharacters"]] = relationship(back_populates="users")
    favoriteplanets: Mapped[List["FavoritePlanets"]] = relationship(back_populates="users")



    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "subscription": self.subscription,
            "last_payment": self.last_payment
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    hair_color: Mapped[str] = mapped_column(nullable=False)
    eyes_color: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    favoritecharacters: Mapped[List["FavoriteCharacters"]] = relationship(back_populates="characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eyes_color": self.eyes_color,
            "description": self.description
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[str] = mapped_column(nullable=False)
    terrain: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    
    favoriteplanets: Mapped[List["FavoritePlanets"]] = relationship(back_populates="planets")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "description": self.description
            # do not serialize the password, its a security breach
        }
    



class FavoriteCharacters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    id_characters: Mapped[int] = mapped_column(ForeignKey("characters.id"), nullable=False, unique=True)
    active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    users: Mapped["Users"] = relationship(back_populates="favoritecharacters")

    characters: Mapped["Characters"] = relationship(back_populates="favoritecharacters")

    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "id_characters": self.id_characters
            # do not serialize the password, its a security breach
        }
    

class FavoritePlanets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    id_planets: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=False, unique=True)
    active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    users: Mapped["Users"] = relationship(back_populates="favoriteplanets")

    planets: Mapped["Planets"] = relationship(back_populates="favoriteplanets")


    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "id_planets": self.id_planets
            # do not serialize the password, its a security breach
        }