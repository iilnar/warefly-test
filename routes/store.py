from flask import Blueprint, session, request, render_template, flash, redirect
from wtforms import Form, StringField, DecimalField, validators
from db import db_session
from models import Store
from routes.auth import auth_required


bp = Blueprint('store', __name__, url_prefix='/store')
PAGE_SIZE = 2


@bp.route('/list', methods=['POST', 'GET'])
@bp.route('/list/<int:page>', methods=['POST', 'GET'])
@auth_required
def list(page=0):
    total_count = db_session.query(Store).count()
    if page == 0:
        stores = db_session.query(Store).order_by(Store.id)
    else:
        offset = (page-1)*PAGE_SIZE
        stores = db_session.query(Store).order_by(Store.id).offset(offset).limit(PAGE_SIZE)

    render_params = {
        'stores_list': stores,
        'stores_count': total_count,
        'page': page,
        'total_pages': (total_count + PAGE_SIZE - 1) / PAGE_SIZE
    }
    return render_template('store/list.html', **render_params)


class AddStoreForm(Form):
    name = StringField('name', [validators.DataRequired(), validators.Length(min=2, max=20)])
    address = StringField('address', [validators.DataRequired(), validators.Length(min=2, max=20)])
    latitude = DecimalField('latitude', [validators.DataRequired()])
    longitude = DecimalField('longitude', [validators.DataRequired()])
    

@bp.route('/add', methods=['POST', 'GET'])
@auth_required
def add():
    form = AddStoreForm(request.form)
    if request.method == 'POST' and form.validate():
        cnt = db_session.query(Store).filter(Store.name == form.name.data and Store.name == form.address.data).count()
        if cnt != 0:
            flash('Store already exists', 'error')
        else:
            db_session.add(Store(form.name.data, form.address.data, form.latitude.data, form.longitude.data))
            db_session.commit()
            flash('Store succesfully added.', 'info')
    return render_template('store/add.html', form=form)

