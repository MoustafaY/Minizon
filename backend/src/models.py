from backend.extensions import db, unique_name_per_supplier
import uuid

class Customer(db.Model):
    id = db.Column(db.UUID(as_uuid=True), unique=True, primary_key=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    shoppingCart = db.relationship('ShoppingCart', backref='customer', cascade='all, delete-orphan', uselist=False)
    transcriptHistory = db.relationship('Transcript', backref='customer')

    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)
        if not self.shoppingCart:
            self.shoppingCart = ShoppingCart(customerId=self.id)


class ShoppingCart(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    totalSum = db.Column(db.Float, nullable=False, default=0.0)
    customerId = db.Column(db.UUID(as_uuid=True), db.ForeignKey('customer.id'), nullable=False)
    shoppingCartProducts = db.relationship('ShoppingCartProduct', backref='shopping_cart', cascade='all, delete-orphan')

class ShoppingCartProduct(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    shoppingCartId = db.Column(db.UUID(as_uuid=True), db.ForeignKey('shopping_cart.id'), nullable=False)
    inventoryId = db.Column(db.UUID(as_uuid=True), db.ForeignKey('inventory.id'), nullable=False)


class Transcript(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    totalSum = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.DateTime, nullable=False)
    customerId = db.Column(db.UUID(as_uuid=True), db.ForeignKey('customer.id'), nullable=True)
    transcriptProducts = db.relationship('TranscriptProduct', backref='transcript', cascade='all, delete-orphan')

class TranscriptProduct(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    transcriptId = db.Column(db.UUID(as_uuid=True), db.ForeignKey('transcript.id'), nullable=False)
    inventoryId = db.Column(db.UUID(as_uuid=True), db.ForeignKey('inventory.id'), nullable=True)
    products = db.relationship('Inventory', backref='transcript_products')

class Supplier(db.Model):
    id = db.Column(db.UUID(as_uuid=True), unique=True, primary_key=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    products = db.relationship('Product', backref='supplier', cascade="all, delete-orphan")
    shipmentHistory = db.relationship('Shipment', backref='supplier', cascade="all, delete-orphan")

class Shipment(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    date = db.Column(db.DateTime, nullable=False)
    supplierId = db.Column(db.UUID(as_uuid=True), db.ForeignKey('supplier.id'), nullable=True)
    shipmentProducts = db.relationship('ShipmentProduct', backref='shipment', cascade='all, delete-orphan')

class ShipmentProduct(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    shipmentId = db.Column(db.UUID(as_uuid=True), db.ForeignKey('shipment.id'), nullable=True)
    productId = db.Column(db.UUID(as_uuid=True), db.ForeignKey('product.id'), nullable=True)
    product = db.relationship('Product', backref='shipment_product')

class Inventory(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    productId = db.Column(db.UUID(as_uuid=True), db.ForeignKey('product.id', ondelete='CASCADE'), nullable=True)
    supplierId = db.Column(db.UUID(as_uuid=True), db.ForeignKey('supplier.id'), nullable=False)

class Product(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    supplierId = db.Column(db.UUID(as_uuid=True), db.ForeignKey('supplier.id'), nullable=True)
    inventory = db.relationship('Inventory', backref='product', cascade='all, delete-orphan')

    __table_args__ = (
        unique_name_per_supplier,
    )

class BlockListToken(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    token = db.Column(db.String(255), nullable=False)