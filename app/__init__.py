from flask import Flask
from flasgger import Swagger
from .api import (health, metrics, product, user)


app = Flask(__name__)
swagger = Swagger(app)

# Routes
app.register_blueprint(health.api)
app.register_blueprint(metrics.api)
app.register_blueprint(product.api)
app.register_blueprint(user.api)
