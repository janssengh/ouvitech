from flask import render_template, session, url_for, flash, redirect, request
from loja import app, bcrypt, db

from .fomularios import LoginFormulario, RegistrationForm, ZipcodeForm, StoreForm
from .models import User, Store


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/index.html', titulo='Ouvitech - Página Administrativa')


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginFormulario(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'{form.email.data} logado com sucesso!', 'success')
            return redirect(request.args.get('next')or url_for('admin'))
        else:
            flash('Não foi possível acessar o sistema!', 'danger')
    return render_template('admin/login.html', form=form, titulo='Login')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, user=form.user.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Obrigado {form.name.data} por registrar !','success')
        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form, titulo='Registrar')

@app.route('/lojacep', methods=['GET','POST'])
def lojacep():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    loja = Store.query.all()
    if loja:
        flash(f'Loja já foi registrada!', 'danger')
        return redirect(url_for('admin'))
    form = ZipcodeForm()
    return render_template('admin/lojacep.html', form=form)

@app.route('/dadosloja', methods=['GET','POST'])
def dadosloja():
    form = ZipcodeForm()
    if form.validate_on_submit():
        # Dados pesquisados VIACEP no formulário do CEP
        dicCep = session['dicCep']
        localidade = (dicCep['localidade'])
        uf = (dicCep['uf'])
        bairro = (dicCep['bairro'])
        complemento = (dicCep['complemento'])
        logradouro = (dicCep['logradouro'])

        # cria dicionário
        zipcode = form.zipcode.data
        DicZipcode = {'zipcode': zipcode}
        session['ZipCode'] = DicZipcode

        form = StoreForm()
        form.city.data = localidade
        form.region.data = uf
        form.neighborhood.data = bairro
        form.complement.data = complemento
        form.address.data = logradouro

        return render_template('admin/lojainc.html', form=form)
    return render_template('admin/lojacep.html', form=form)

@app.route('/lojainc', methods=['GET','POST'])
def lojainc():
    form = StoreForm()
    if form.validate_on_submit():
        ZipCode = session['ZipCode']
        zipcode = (ZipCode['zipcode'])
        address = form.address.data
        number = form.number.data
        complement = form.complement.data
        neighborhood = form.neighborhood.data
        city = form.city.data
        region = form.region.data
        freight_rate = form.freight_rate.data
        name = form.name.data
        pages = form.pages.data
        phone = form.phone.data
        logo = form.logo.data

        loja = Store(zipcode, name, address, number, complement, neighborhood, city,
                         region, freight_rate, phone, pages, logo)

        db.session.add(loja)
        flash(f'A loja {name} foi cadastrada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin/lojainc.html', form=form)

