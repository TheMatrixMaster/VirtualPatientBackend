import functools
from flask import (
    Blueprint,
    g,
    session,
    redirect,
    url_for,
    flash,
    abort,
    request,
    render_template,
)

bp = Blueprint('view', __name__)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


