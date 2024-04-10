from flask import Blueprint
bp = Blueprint("location", __name__)
from location import routes, sb_interface, mg_interface