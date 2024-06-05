from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from sqlalchemy.schema import UniqueConstraint

unique_name_per_supplier = UniqueConstraint('name', 'supplierId', name='unique_name_per_supplier')
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()