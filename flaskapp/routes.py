import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskapp.db import get_db


bp = Blueprint('routes', __name__)

@bp.route('/')
def hello():
    return 'hello world'
