from .extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    

    def __repr__(self):
     return f"Product (name = {self.name}, price = {self.price}, stock = {self.stock})" 
    
    def test_product_str_method():
        product = Product(name="Test", price=10.0, stock=5)
        assert str(product) == "Test"
