import pytest
from src.main import create_app
from src.api.extensions import db

from typing import Any
from flask.testing import FlaskClient
import pytest

@pytest.fixture
def client(app: Any) -> FlaskClient:
    """Cliente de prueba para hacer solicitudes HTTP."""
    return app.test_client()

def test_create_product(client: FlaskClient):
    response = client.post('/products', json={
        'name': 'Test Product',
        'price': 20.0,
        'stock': 10
    })
    assert response.status_code == 201
    assert response.json['name'] == 'Test Product'



@pytest.fixture
def app():
    """Crea una instancia de la aplicación configurada para pruebas."""
    app = create_app()
    app.config['TESTING'] = True  # Habilita el modo de pruebas
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria para pruebas
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Crea las tablas necesarias
        yield app  # Provee la aplicación para pruebas
        db.drop_all()  # Limpia la base de datos después de las pruebas


@pytest.fixture
def client(app):
    """Proporciona un cliente de pruebas para hacer peticiones HTTP."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Proporciona un runner para ejecutar comandos CLI."""
    return app.test_cli_runner()
