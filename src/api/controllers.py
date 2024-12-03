from flask import request, jsonify, abort
from flask_restful import Resource, fields, marshal_with, reqparse
from .extensions import db
from .models import Product
from flask import jsonify
from werkzeug.exceptions import HTTPException

# Definición de los campos de respuesta para marshalling
product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Float,
    'stock': fields.Integer
}

# Configurar los argumentos requeridos en las peticiones
product_args = reqparse.RequestParser()
product_args.add_argument('name', type=str, required=True, help="Name is required")
product_args.add_argument('price', type=float, required=True, help="Price is required")
product_args.add_argument('stock', type=int, required=True, help="Stock is required")




class ProductDetail(Resource):
    @marshal_with(product_fields)
    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        if not product:
            abort(404, description="Product not found")
        return product, 200
   

    @marshal_with(product_fields)
    def patch(self, id):
        args = product_args.parse_args()
        product = Product.query.filter_by(id=id).first()
        if not product:
            abort(40, description="Product not found")
        
        # Actualizar los campos si existen
        if args['name']:
            product.name = args['name']
        if args['price']:
            product.price = args['price']
        if args['stock']:
            product.stock = args['stock']
        
        db.session.commit()
        return product, 200
    


    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        if not product:
            abort(404, description="Product not found")
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully'}, 200


class ProductList(Resource):
    @marshal_with(product_fields)
    def get(self):
        products = Product.query.all()
        return products, 200

    @marshal_with(product_fields)
    def post(self):
        args = product_args.parse_args()

        # Validar campos
        if not args['name'] or args['name'].isspace():
            abort(400, description="Name cannot be empty or contain only spaces")
        if args['price'] <= 0:
            abort(400, description="Price must be greater than zero")
        if args['stock'] < 0:
            abort(400, description="Stock cannot be negative")

        # Crear un nuevo producto
        product = Product(name=args['name'], price=args['price'], stock=args['stock'])
        db.session.add(product)
        db.session.commit()
        return product, 201

