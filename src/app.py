from flask import Flask
from flask.blueprints import Blueprint
from flask_cors import CORS

import config
import routes
from keras.models import load_model

server  = Flask(__name__)
print('Flask starting')
print('Loading model')
model = load_model(config.MODEL_STORAGE_PATH)
model._make_predict_function()
print('Model loaded')

# model = load_model(config.MODEL_STORAGE_PATH)

if config.ENABLE_CORS:
    cors    = CORS(server, resources={r"/api/*": {"origins": "*"}})

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=config.API_URL_PREFIX)

if __name__ == "__main__":
    #print("server details",server.url_map)
    server.run(host=config.HOST, port=config.PORT, debug=True)
    
print('Flask started')
