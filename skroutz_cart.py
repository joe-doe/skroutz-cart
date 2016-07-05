import json
import os
from flask import Flask
from flask_cors import CORS
from flask_restplus import Api

from initializers import (
    initialize_db,
    initialize_model,
    initialize_routes,
    initialize_schedule_jobs
)


# open configuration file and read the values
with open('config.json') as config_file:
    config = json.load(config_file)

# override values if custom config exists
try:
    with open('my_config.json') as ext_config_file:
        ext_config = json.load(ext_config_file)
        config.update(ext_config)
except IOError:
    print "No external configuration found. Using default"
    pass

# get sensible credentials from environment variables
try:
    config['uri'] = str(os.environ['mongodb_uri'])
except KeyError:
    pass


app = Flask(__name__,
            static_folder='web/static',
            template_folder='web/templates')
CORS(app)

api = Api(app)
db = initialize_db(config)
model = initialize_model(config, db)

initialize_routes(app, api, model)
# initialize_schedule_jobs(config, model)

# main
if __name__ == '__main__':
        # model.store()
        # model.process()
        app.run(debug=False)

