from flask import Flask, jsonify
from flask_restful import Api
from src.api.extensions import db
from src.api.controllers import ProductList, ProductDetail
from werkzeug.exceptions import HTTPException


def create_app():
    app = Flask(__name__)
    app.config.from_object('src.instance.config.Config')


    # Ruta básica de inicio
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Product API!"}), 200

    # Inicializar extensiones
    db.init_app(app)

    # Crear instancia de Flask-RESTful API
    api = Api(app)

    # Registrar los endpoints
    api.add_resource(ProductList, '/products')
    api.add_resource(ProductDetail, '/products/<int:id>')

    

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Maneja errores HTTP y devuelve un JSON estándar"""
        return jsonify({
            "error": e.name,
            "message": e.description
        }), e.code


    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


def test_app_initialization():
    from src.main import app
    assert app is not None
