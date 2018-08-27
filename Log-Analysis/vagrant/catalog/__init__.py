from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask import session as login_session

import jwt
import datetime
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from .models import Category, Item

from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)
app.config.from_pyfile('config.py')

engine = create_engine('postgresql://vagrant@localhost/catalog')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

CLIENT_ID = json.loads(
    open('catalog/client_secret.json', 'r').read())['web']['client_id']


@app.route('/login')
def login():
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
    permission = {'can_add': True, 'can_edit': True,
                  'can_delete:': True, 'exp': exp}
    state = jwt.encode(permission, 'secret', algorithm='HS256').decode('utf-8')
    login_session['state'] = state
    return render_template('login.html', STATE=state, exp=exp)


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
    item = session.query(Item).filter(Item.title == item_name).one()
    return render_template('item_detail.html', item=item)


@app.route('/catalog/<item_name>/edit', methods=['GET', 'POST'])
def edit(item_name):
    categories = session.query(Category).all()
    item_query = session.query(Item).filter(Item.title == item_name)
    item = item_query.one()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category_id = str(request.form['category'])

        new_item = {
            'title': title,
            'description': description,
            'category_id': category_id
        }

        item_query.update(new_item)
        session.commit()

        flash('You were successfully edited.')

        return redirect(url_for('item_detail', category_name=item.category.name,
                                item_name=title))
    return render_template('edit.html', categories=categories, item=item)


@app.route('/catalog/<item_name>/delete', methods=['GET', 'POST'])
def delete(item_name):
    item_query = session.query(Item).filter(Item.title == item_name)
    item = item_query.one()
    if request.method == 'POST':
        item_query.delete()
        session.commit()
        flash('You were successfully deleted.')

        return redirect(url_for('index'))

    return render_template('delete_item.html', item=item)
