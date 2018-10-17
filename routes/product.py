from flask import Blueprint, session, request, render_template, flash, redirect
from wtforms import Form, StringField, validators
from db import db_session
from models import Product
from routes.auth import auth_required


bp = Blueprint('product', __name__, url_prefix='/product')

@bp.route('/list', methods=['POST', 'GET'])
@auth_required
def list():
    products = db_session.query(Product)
    return render_template('product/list.html', products=products)


class AddProductForm(Form):
    name = StringField('name', [validators.DataRequired(), validators.Length(min=2, max=20)])
    vendor = StringField('vendor', [validators.DataRequired(), validators.Length(min=2, max=20)])


@bp.route('/add', methods=['POST', 'GET'])
@auth_required
def add():
    form = AddProductForm(request.form)
    if request.method == 'POST' and form.validate():
        db_session.add(Product(form.name.data, form.vendor.data))
        db_session.commit()
        flash('Product successfully added.', 'success')

    return render_template('product/add.html', form=form)
