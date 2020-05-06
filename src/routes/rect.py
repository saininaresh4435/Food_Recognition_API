from flask import Blueprint
from flask_restful import Api

from resources import RectResource

RECT_BLUEPRINT = Blueprint("rect", __name__)
#print("rout details",RECT_BLUEPRINT)
Api(RECT_BLUEPRINT).add_resource(
    RectResource, "/rect/recipe"
)
