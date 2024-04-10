from flask import Blueprint
bp = Blueprint("food", __name__)
from food import routes, sb_interface, mg_interface