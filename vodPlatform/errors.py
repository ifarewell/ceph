from flask import render_template

from vodPlatform import app


@app.errorhandler(401)
def unauthorized_access(e):
    return render_template('errors/401.html'), 401


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
