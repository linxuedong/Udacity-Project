from flask import Flask, render_template

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from .models import Base

from .models import Category, Item

app = Flask(__name__)
app.config.from_pyfile('config.py')

engine = create_engine('postgresql://vagrant@localhost/catalog')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


@app.route('/')
def index():
    # 展示 categories
    categories = session.query(Category).all()

    # 展示 items
    items = session.query(Item).order_by(Item.created_at.desc()).all()

    return render_template('index.html', categories=categories, items=items)


@app.route('/catalog/<category_name>/items')
def item_list(category_name):
    # categories
    categories = session.query(Category).all()
    current_category = session.query(Category).filter(
        Category.name == category_name).one()

    # 某个 categories 的 items
    items = session.query(Item).filter(
        Item.category == current_category).order_by(Item.created_at.desc()).all()

    return render_template('index.html', categories=categories, items=items)


@app.route('/catalog/<category_name>/<item_name>')
def item_detail(category_name, item_name):
    # item name

    # item descripe

    return '{} items: {}'.format(category_name, item_name)


@app.route('/catalog/<category_name>/edit')
def edit(category_name):
    return 'edit item'
