from flask import Blueprint, render_template
# from fisher_book import FisherBook
# from helper import is_isbn_or_key

web = Blueprint('web', __name__)


@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


from fisher.view import auth
from fisher.view import book
from fisher.view import drift
from fisher.view import gift
from fisher.view import login
from fisher.view import main
from fisher.view import wish

