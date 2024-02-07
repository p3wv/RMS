from flask import render_template
from . import outside


@outside.route('/outside')
def outside_index():
    return render_template('menu.html')