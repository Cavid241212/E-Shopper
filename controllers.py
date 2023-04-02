from app import app
from flask import render_template,request,redirect,url_for,flash
from forms import ContactForm, RegisterForm, LoginForm, SubscribeForm,ReviewForm,SearchForm
from models import Contact,User,Product,Subscribe,Category,Subcategories,Review,Product_detail
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user,login_user,logout_user,login_required




@app.route("/detail/<int:id>/", methods = ['GET','POST'])
def detail(id):
    products = Product.query.filter_by(id = id).first()
    all_images = Product_detail.query.filter_by(product_id=id).all()
    favorits = Category.query.filter_by(id=id).first().products
    reviews = Review.query.filter_by(product_id=id).all()
    categories = Category.query.all()
    form = ReviewForm()
    subscribe_form = SubscribeForm()
    search_form = SearchForm()
    if request.method == 'POST':
        form = ReviewForm(request.form)
        if form.validate_on_submit():
            print("valid")
            if current_user.is_authenticated:
                review = Review(
                    message = form.message.data,
                    product_id = id,
                    user_id = current_user.id,
                    
                )
                review.save()
                return redirect(f'/detail/{id}/')
            else:
                flash('Yorum yazmak için giriş yapmalısınız.', 'info')
                return redirect(url_for('login'))
            
    return render_template("detail.html",item = products, favorits = favorits,form = form, reviews = reviews,subscribe_form = subscribe_form,search_form=search_form,categories=categories,all_images=all_images)


@app.route("/favorites")
def favorites():
    return render_template("favorites.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/shop')


@app.route("/login", methods = ['GET','POST'])

def login():
    form = LoginForm()
    subscribe_form = SubscribeForm()
    search_form = SearchForm()
    categories = Category.query.all()
    error = None
    if request.method == 'POST':
        form = LoginForm(request.form)
        user = User.query.filter_by(email = form.email.data).first()
        if request.form['email'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid email or password'
        else:
            flash('You were successfully logged in')
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('/shop')
    return render_template("login.html", form = form,subscribe_form=subscribe_form,search_form=search_form,categories=categories,error=error)

@app.route("/register", methods = ['GET','POST'])
def register():
    form = RegisterForm()
    subscribe_form = SubscribeForm()
    search_form = SearchForm()
    categories = Category.query.all()
    if request.method == 'POST':
        form = RegisterForm(request.form)
        print(request.form)
        if form.validate_on_submit():
            print("valid")
            user = User(
                name = form.name.data,
                email = form.email.data,
                password = generate_password_hash(form.password.data)
            )
            user.save()
            flash('Thanks for registering')
            return redirect("/register")
    return render_template("register.html", form = form,subscribe_form=subscribe_form,search_form=search_form,categories=categories)

@app.route("/shop")
def shop():
    categories = Category.query.all()
    products = Product.query.all()
    subscribe_form = SubscribeForm()
    search_form = SearchForm()
    return render_template('shop.html', categories=categories,products = products,subscribe_form=subscribe_form,search_form=search_form)

@app.route("/categories/<string:name>/")
def categories(name):
    subscribe_form = SubscribeForm()
    categories = Category.query.all()
    products = Category.query.filter_by(title=name).first().products
    search_form = SearchForm()
    return render_template('shop.html', categories=categories, products = products,subscribe_form=subscribe_form,search_form=search_form)

@app.route("/categories/<string:category_name>/<string:subcategory_name>")
def subcategories(category_name, subcategory_name):
    subscribe_form = SubscribeForm()
    categories = Category.query.all()
    subcategory = Subcategories.query.filter_by(title=subcategory_name).first()
    search_form = SearchForm()
    print(subcategory)
    products = subcategory.products
    print(products)
    return render_template('shop.html', categories=categories, subcategory=subcategory, products=products,subscribe_form=subscribe_form,search_form=search_form)

@app.route("/")
def base_category():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template('base.html', categories=categories, products = products)
    
@app.route("/contact",methods = ['GET','POST'])
def contact():
    form = ContactForm()
    subscribe_form = SubscribeForm()
    search_form = SearchForm()
    categories = Category.query.all()
    if request.method == 'POST':
        print(form.name.data)
        print(form.email.data)
        print(form.subject.data)
        form = ContactForm(request.form)
        print(request.form)
        if form.validate_on_submit():
            print("valid")
            contacts = Contact(
                name = form.name.data,
                email = form.email.data,
                subject = form.subject.data,
                message = form.message.data
            )
            contacts.save()
            flash("Message sent successfully!")
            return redirect('/contact')
        else:
            flash('Please correct the errors below.', 'danger')
    
    return render_template("contact.html",form = form,subscribe_form=subscribe_form,search_form=search_form,categories=categories)

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    subscribe_form = SubscribeForm()
    search_form = SearchForm()
    print(request.url)
    if request.method == 'POST':
      subscribe_form=SubscribeForm(request.form)
      if subscribe_form.validate_on_submit():
        subscribes = Subscribe(
            name=subscribe_form.name.data,
            email=subscribe_form.email.data
        )
        subscribes.save()
        flash('You have subscribed successfully!', 'success')
       
        a=request.form["path"].split("/")[-1]
        if len(request.form["path"].split("/"))>4:
          a="/" +request.form["path"].split("/")[3] + "/" + request.form["path"].split("/")[4] 
         
          return redirect(a)
        return redirect(url_for(f'{a}'))
      else:
        flash('Please correct the errors below.', 'danger')
    return render_template('base.html', subscribe_form=subscribe_form,search_form=search_form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    subscribe_form = SubscribeForm()
    categories = Category.query.all()
    productss = Product.query.all()
    if request.method == 'POST':
        search_form = SearchForm(request.form)
        if search_form.validate_on_submit():
            search_term = search_form.search.data
            productss = Product.query.filter(Product.title.like('%' + search_term + '%')).all()
            return render_template('shop-search.html', productss=productss, search_form=search_form,subscribe_form=subscribe_form,categories=categories,search_term=search_term)
    return render_template('base.html', search_form=search_form,subscribe_form=subscribe_form)
