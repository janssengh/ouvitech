from loja import db, app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    user = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False, default='profile.jpg')
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    loja = db.relationship('Store', backref=db.backref('lojas.user', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.user
    


with app.app_context():
    db.create_all()