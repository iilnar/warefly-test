from flask import Flask
from routes import auth, store, purchase, product

from db import db_session

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


app.register_blueprint(auth.bp)
app.register_blueprint(store.bp)
app.register_blueprint(purchase.bp)
app.register_blueprint(product.bp)
app.secret_key = b'abacaba'
