from flask import render_template
from loja import app


@app.route('/')
def home():
    return render_template('home/index.html', titulo='Ouvitech - Aparelhos Auditivos')