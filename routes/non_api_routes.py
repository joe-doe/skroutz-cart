from flask import render_template


def register_non_api_routes(app, model):

    @app.route('/index')
    def index():
        return render_template('index.html', items=model.get_all_items())

    @app.route('/new_item')
    def new_item():
        return render_template('new_item.html')

    @app.route('/ping')
    def ping():
        return render_template('ping.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/about')
    def about():
        return render_template('about.html')
