# para uso do MYSQL
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash

from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os

from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
uri = 'sqlite:///' + os.path.join(basedir, 'minhaloja.db')

app = Flask(__name__)

# criar base de dados sqlite
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config['SECRET_KEY'] = 'rejoinders1963'

# usando o prompt do mysql command line, vamos criar uma base de dados
# create database bancodados

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:roeland@localhost:3306/ouvitech'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc2_0YlAAAAAB5JMKSTh9e843n2NI1YgUZzjAFP'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc2_0YlAAAAABAiIufL9fiAcQptQIF3LnddKwJo'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

db = SQLAlchemy(app)

lista = []

bcrypt = Bcrypt(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqllite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)



app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

from loja.home import rotas
from loja.admin import rotas
from loja.produtos import rotas
