from flask import render_template


def register_non_api_routes(app, model):

    @app.route('/index')
    def index():
        return render_template('index.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/about')
    def about():
        return render_template('about.html')
