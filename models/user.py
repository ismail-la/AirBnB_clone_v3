#!/usr/bin/python3
"""
defines a class called User that inherits from two other classes:
BaseModel and Base
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


# comment
class User(BaseModel, Base):
    """user representation"""
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

        @property
        def places(self):
            """"""
            from models.place import Place
            place_list = []
            all_places = models.storage.all(Place)
            for place in all_places.values():
                if place.user_id == self.id:
                    place_list.append(place)
            return place_list

        @property
        def reviews(self):
            """"""
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.user_id == self.id:
                    review_list.append(review)
            return review_list

    def __init__(self, *args, **kwargs):
        """user initializes """
        super().__init__(*args, **kwargs)

    def __setattr__(self, key, value):
        """"""
        if key == 'password':
            value = md5(value.encode()).hexdigest()
        super().__setattr__(key, value)
