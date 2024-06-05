from backend.baseRepository import BaseRepository, BaseToken
from backend.extensions import db
from backend.models import Customer, Supplier, Product, ShoppingCart, Transcript, TranscriptProduct, Shipment, ShipmentProduct, ShoppingCartProduct, Inventory, BlockListToken
from sqlalchemy.orm.exc import NoResultFound
import uuid

class CustomerRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)

    def pay_balance(self, customerId, payment):
        payment = float(payment)
        customer = self.get_by_id(customerId)
        if customer.balance < payment:
            raise ValueError
        if payment < 0:
            raise ValueError
        customer.balance = customer.balance - payment
        self.save()
        return customer
    
    def get_for_user(self, id):
        return db.session.query(self.model).filter_by(id=id).one_or_none()

    
    def get_by_email(self, email, password):
        customer = db.session.query(self.model).filter_by(email=email, password=password).one_or_none()
        if customer is None:
            raise NoResultFound
        return customer
    
    def get_balance(self, id):
        customer = self.get_by_id(id)
        return customer.balance


class SupplierRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)
    
    def get_by_email(self, email, password):
        supplier = db.session.query(self.model).filter_by(email=email, password=password).one_or_none()
        if supplier is None:
            raise NoResultFound
        return supplier
    
    def get_for_user(self, id):
        return db.session.query(self.model).filter_by(id=id).one_or_none()

class ProductRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)

    def get_by_name(self, supplierId, name):
        product = db.session.query(self.model).filter_by(supplierId=supplierId, name=name).one_or_none()
        if product is None:
            raise NoResultFound
        return product
    
    def get_all_by_supplier(self, id):
        return db.session.query(self.model).filter_by(supplierId=id).all()

class ShoppingCartRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)
    
    def get_by_customer(self, id):
        shoppingCart = db.session.query(self.model).filter_by(customerId=id).one_or_none()
        if shoppingCart is None:
            raise NoResultFound
        return shoppingCart
    
    def get_product_by_id(self, productId, shoppingCartId):
        return db.session.query(ShoppingCartProduct).filter_by(shoppingCartId=shoppingCartId, inventoryId=uuid.UUID(productId)).one_or_none()

    def add_to_cart(self, customerId, inProduct):
        shoppingCart = self.get_by_customer(customerId)
        product = self.get_product_by_id(inProduct["id"], shoppingCart.id)
        if product is None:
            newProduct = ShoppingCartProduct(name=inProduct["name"], quantity=inProduct["quantity"], price=inProduct["price"], shoppingCartId=shoppingCart.id, inventoryId=uuid.UUID(inProduct["id"]))
            shoppingCart.shoppingCartProducts.append(newProduct)
        else:
            product.quantity = product.quantity + inProduct["quantity"]
        newSum = self.calculateSum(shoppingCart.shoppingCartProducts)
        shoppingCart.totalSum = newSum
        self.save()
    
    def update_cart(self, customerId, inProduct):
        shoppingCart = self.get_by_customer(customerId)
        product = self.get_product_by_id(inProduct['id'], shoppingCart.id)
        if product is None:
            raise NoResultFound
        product.quantity = inProduct["quantity"]
        newSum = self.calculateSum(shoppingCart.shoppingCartProducts)
        shoppingCart.totalSum = newSum
        self.save()
    
    def remove_from_cart(self, customerId, productId):
        shoppingCart = self.get_by_customer(customerId)
        product = self.get_product_by_id(productId, shoppingCart.id)
        if product is None:
            raise NoResultFound
        shoppingCart.shoppingCartProducts.remove(product)
        newSum = self.calculateSum(shoppingCart.shoppingCartProducts)
        shoppingCart.totalSum = newSum
        self.save()
    
    def clear_cart(self, customerId):
        shoppingCart = self.get_by_customer(customerId)
        shoppingCart.shoppingCartProducts = []
        shoppingCart.totalSum = 0.0
        self.save()

    
    def calculateSum(self, products):
        sum = 0
        for product in products:
            sum+= (float(product.price)*int(product.quantity))
        return sum


class TranscriptRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)

    def get_by_customer(self, id):
        transcript = db.session.query(self.model).filter_by(customerId=id).all()
        return transcript
    
    def add_to_transcript(self, transcript, products):
        for product in products:
            transcriptProduct = TranscriptProduct(name=product.name, quantity=product.quantity, price=product.price, transcriptId=transcript.id, inventoryId=product.inventoryId)
            transcript.transcriptProducts.append(transcriptProduct)
        transcript.totalSum = self.calculateSum(transcript.transcriptProducts)
        self.save()

    def calculateSum(self, products):
        sum = 0
        for product in products:
            sum+= (product.price*product.quantity)
        return sum

class ShipmentRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)

    def add_to_shipment(self, shipment, products):
        for product in products:
            shipmentProduct = ShipmentProduct(name=product["name"], quantity=product["quantity"], productId=product["id"], shipmentId=shipment.id)
            shipment.shipmentProducts.append(shipmentProduct)
        self.save()
    
    def get_all_by_supplier(self, id):
        return db.session.query(self.model).filter_by(supplierId=id).all()

class InventoryRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)

    def create(self, **kwargs):
        product = db.session.query(self.model).filter_by(supplierId=kwargs.get('supplierId'), productId=kwargs.get('productId')).one_or_none()
        if product is None:
            product = self.model(**kwargs)
        else:
            product.quantity = product.quantity + kwargs.get('quantity')
        db.session.add(product)
        db.session.commit()
        return product


class TokenRepository:
    def getToken(self, jti):
        return BlockListToken.query.filter_by(token=jti).one_or_none()
    
    def addToken(self, jti):
        token = BlockListToken(token=jti)
        BaseToken.saveToken(token)

customerRepository = CustomerRepository(Customer)
supplierRepository = SupplierRepository(Supplier)
productRepository = ProductRepository(Product)
shoppingCartRepository = ShoppingCartRepository(ShoppingCart)
transcriptRepository = TranscriptRepository(Transcript)
shipmentRepository = ShipmentRepository(Shipment)
inventoryRepository = InventoryRepository(Inventory)
