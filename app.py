from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345@127.0.0.1:3306/Shopping'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '8f42a73054b1749f8f58848be5e6502c'


from controllers import *
from exstensions import *
from models import *

admin = Admin(app,name='Eshopper Admin', template_mode='bootstrap3')

admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Subcategories, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Contact, db.session))
admin.add_view(ModelView(Review, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Subscribe,db.session))
admin.add_view(ModelView(Product_detail,db.session))


if __name__ == '__main__':
    app.init_app(db)
    app.init_db(migrate)
    app.init_db(port=5000, debug=True)


