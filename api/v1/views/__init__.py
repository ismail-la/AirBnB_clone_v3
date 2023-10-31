#!/usr/bin/python3
"""Python script that sets up a blueprint for a Flask application.
initializing app_views
"""

# Blueprints in Flask are used for modular structuring of applications.
from flask import Blueprint

# These modules are likely to contain route handlers for different parts
#  of your application.
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *

# Creates a new blueprint named app_views.
# The url_prefix='/api/v1' means that all routes registered with this
#  blueprint will have URLs prefixed with /api/v1.
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
