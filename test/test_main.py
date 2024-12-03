import pytest
from src.main import create_app
from src.api.extensions import db
from src.api.models import Product
from typing import Any  # Importar Any para las anotaciones de tipo
from flask.testing import FlaskClient  # Si usas FlaskClient para tests



def test_create_product(client: FlaskClient):
    response = client.post('/products', json={
        'name': 'Test Product',
        'price': 20.0,
        'stock': 10
    })
    assert response.status_code == 201
    assert response.json['name'] == 'Test Product'

def test_create_product(client: Any):
   response = client.post('/products', json={'name': 'Test', 'price': 10.0, 'stock': 5})
   assert response.status_code == 201  # Ensure it's created
   product_id = response.json ['id']  # Capture the returned ID

def test_create_product_invalid_data(client: FlaskClient):
    response = client.post('/products', json={'name': '', 'price': -5, 'stock': 10})
    assert response.status_code == 400
    assert 'error' in response.get_json() 
    assert response.get_json()['error'] == 'Invalid data'


#Lectura 
def test_get_all_products(client: Any):
    response = client.get('/products')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_product_by_id(client: Any):
    # Crear un producto para probar
    create_response = client.post('/products', json={
        'name': 'Producto de Prueba',
        'price': 20.0,
        'stock': 15
    })
    assert create_response.status_code == 201
    product_id = create_response.get_json().get('id')  # Obtener el ID del producto creado

    # Obtener el producto por su ID
    get_response = client.get(f'/products/{product_id}')
    assert get_response.status_code == 200
    product = get_response.get_json()
    
    # Validar los datos del producto obtenido
    assert product['id'] == product_id
    assert product['name'] == 'Producto de Prueba'
    assert product['price'] == 20.0
    assert product['stock'] == 15

    response = client.get(f'/products/{product_id}')
    assert response.status_code == 200
    product = response.get_json()
    assert product['id'] == product_id
    assert product['name'] == 'Producto de Prueba'
    assert product['price'] == 20.0
    assert product['stock'] == 15




def test_update_product(client: Any):
    # Crear un producto para probar
    create_response = client.post('/products', json={
        'name': 'Producto Prueba',
        'price': 10.0,
        'stock': 10
    })
    assert create_response.status_code == 201
    product_id = create_response.get_json().get('id')  # Obtén el ID del producto creado

    # Actualizar el producto
    update_response = client.patch(f'/products/{product_id}', json={
        'price': 15.0,
        'name': 'Producto Actualizado',
        'stock': 5
    })
    assert update_response.status_code == 200
    updated_product = update_response.get_json()
    assert updated_product['price'] == 15.0
    assert updated_product['name'] == 'Producto Actualizado'
    assert updated_product['stock'] == 5

def test_get_product_not_found(client: FlaskClient):
    response = client.get('/products/999')
    assert response.status_code == 404
    assert response.get_json().get('message') == 'Product not found'

#Actualizar 
def test_delete_product(client: Any):
    # Crear un producto para probar
    client.post('/products', json={'name': 'Test', 'price': 10.0, 'stock': 5})
    response = client.delete('/products/1')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Product deleted successfully'


def test_update_nonexistent_product(client):
    response = client.patch('/products/999', json={'price': 20.0})
    assert response.status_code == 400
    assert response.get_json().get('message') == 'Product not found'




def test_delete_product_not_found(client):
    response = client.delete('/products/999')  # Producto inexistente
    assert response.status_code == 404

def test_config_loading(app):
    assert app.config['DEBUG'] is False  # O cualquier configuración que tengas

def test_404_error(client):
    response = client.get('/nonexistent')  # Ruta no existente
    assert response.status_code == 404


def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Product API!"}

def test_product_repr(): 
    product = Product(name="Test Product", price=15.0, stock=20)
    assert repr(product) == "<Product(name='Test Product', price=15.0, stock=20)>"

