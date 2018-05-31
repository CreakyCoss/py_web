from flask import Blueprint

backstage = Blueprint('backstage', __name__)

from . import views