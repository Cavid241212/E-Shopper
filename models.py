from exstensions import db
from exstensions import login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from datetime import datetime

from app import app

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), nullable = False)
    subcategories_id = db.relationship('Subcategories', backref='Category')
    products =  db.relationship('Product', backref = 'Category')

    
    def __init__(self,title):
        self.title = title
       
    def __repr__(self):
        return self.title
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Subcategories(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    products = db.relationship('Product', backref='Subcategories')


    def __init__(self,title):
        self.title = title
       
    def __repr__(self):
        return self.title
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), nullable = False)
    price = db.Column(db.Numeric(10,2), nullable = False)
    old_price = db.Column(db.Numeric(10,2), nullable = True)
    image_url = db.Column(db.String(200),nullable = False)
    description = db.Column(db.String(150), nullable = False)
    subcategories_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    reviews = db.relationship('Review', backref='Product')
    images_url = db.relationship('Product_detail', backref='Product')
    
   
    def __init__(self,title,price,description,old_price,image_url,category_id,subcategories_id):
        self.title = title
        self.price = price
        self.old_price = old_price
        self.description = description
        self.image_url = image_url
        self.category_id = category_id
        self.subcategories_id = subcategories_id
        
    def __repr__(self):
        return self.title
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Product_detail(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    images_url = db.Column(db.String(200),nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __init__(self,images_url,product_id):
        self.images_url = images_url
        self.product_id = product_id

    def __repr__(self):
        return self.images_url
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    subject = db.Column(db.String(150), nullable = False)
    message = db.Column(db.Text)
    
   
    def __init__(self,name,email,subject,message):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message
        
    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
   
    def __init__(self,message,product_id,user_id):
        self.message = message
        self.product_id = product_id
        self.user_id = user_id

    def __repr__(self):
        return self.title
    
    def save(self):
        db.session.add(self)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250),unique = True, nullable = False)
    email = db.Column(db.String(255),unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    review = db.relationship('Review', backref='User')
    
   
    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = password
    
    def check_password(self, new_password):
        return check_password_hash(self.password, new_password)
        
    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Subscribe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200),nullable = False)


    def __init__(self,name,email):
        self.name = name
        self.email = email
        
    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()




