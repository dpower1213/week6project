from app import db, login
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name_first = db.Column(db.String(150))
    name_last = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    itemss = db.relationship('Inv', secondary='user_cart', backref='users',lazy ='dynamic')
    
    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.name_first = data['name_first']
        self.name_last = data['name_last']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    # saves user to database
    def save(self):
        db.session.add(self)
        db.session.commit()
            
    def get_id(self):
        return self.user_id
        
class Inv(db.Model):
    __tablename__ = 'inv'
    item_id = db.Column(db.Integer, primary_key=True)
    upc = db.Column(db.String(50))
    item_name = db.Column(db.String(50))
    item_desc = db.Column(db.String(250))
    item_price = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default = dt.utcnow)
            
    def from_dict(self, data):
        self.upc = data['upc']
        self.item_name = data['item_name']
        self.item_desc = data['item_desc']
        self.item_price = data['item_price']
    
    def __repr__(self):
        return f'<Post: {self.item_id} | {self.item_name}>'
        
    def save(self):
        db.session.add(self) # add the item to the db session
        db.session.commit() #save everything in the session to the database
        
    def exists(item_name):
        return Inv.query.filter_by(item_name = item_name).first()
            
    def delete(item_id):
        db.session.remove(item_id) # remove the item from the db session
        db.session.commit() #save everything in the session to the database
    
    def get_item_id(self):
        return self.item_id
        
class UserCart(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, db.ForeignKey(Inv.item_id, ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    
    def save(self):
        db.session.add(self) # add the item to the db session
        db.session.commit() #save everything in the session to the database
    
    def delete(self):
        db.session.delete(self) # remove the item from the db session
        db.session.commit() #save everything in the session to the database
        
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))