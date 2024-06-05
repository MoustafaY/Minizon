from backend.extensions import db
from sqlalchemy.orm.exc import NoResultFound
import uuid

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return db.session.query(self.model).all()

    def get_by_id(self, id):
        output = db.session.get(self.model, id)
        if output is None: 
            raise NoResultFound
        return output

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def update(self, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        db.session.commit()
        return instance

    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()
    
    def reset(self):
        self.model.query.delete()
        db.session.commit()
    
    def save(self):
        db.session.commit()

class BaseToken:
    def saveToken(token):
        db.session.add(token)
        db.session.commit()