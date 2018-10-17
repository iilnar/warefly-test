from flask import Blueprint, request, render_template, flash, g

from db import db_session
from models import Purchase, Product, Store, User
from routes.auth import auth_required

bp = Blueprint('purchase', __name__, url_prefix='/purchase')


@auth_required
@bp.route('/list', methods=['POST', 'GET'])
def list():
    purchases = db_session.query(Purchase, Product).filter(
        Purchase.buyer_id == g.user.id).join(Product)
    return render_template('purchase/list.html', records=purchases)


@auth_required
@bp.route('/filter', methods=['POST', 'GET'])
def filter_by_user_and_store():
    records = []
    if request.method == 'POST':
        user_id = request.form['user']
        store_id = request.form['store']

        records = db_session.query(Purchase, Product).filter(Purchase.buyer_id == user_id and
                                                             Purchase.store_id == store_id).join(Product)
    render_params = {
        'records': records,
        'users': db_session.query(User).order_by(User.id),
        'stores': db_session.query(Store).order_by(Store.id)
    }
    return render_template('purchase/filter.html', **render_params)


@auth_required
@bp.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        store_id = request.form['store']
        product_id = request.form['product']
        price = request.form['price']
        has_error = False

        if db_session.query(Store).filter(Store.id == store_id).count == 0:
            flash('No such store', 'error')
            has_error = True
        if db_session.query(Product).filter(Product.id == product_id).count == 0:
            flash('No such product', 'error')
            has_error = True
        if price is None:
            flash('Price is not set', 'error')
            has_error = True

        if not has_error:
            db_session.add(Purchase(g.user.id, store_id, product_id, price))
            db_session.commit()
            flash('Purchase successfully added', 'success')

    render_params = {
        'products': db_session.query(Product).order_by(Product.name),
        'stores': db_session.query(Store).order_by(Store.name)
    }
    return render_template('purchase/add.html', **render_params)
