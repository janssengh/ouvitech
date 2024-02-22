from flask import render_template, session, url_for, flash, redirect, request, session, make_response, jsonify
from loja import app, bcrypt, db

from .fomularios import LoginFormulario, RegistrationForm, ZipcodeForm, StoreForm, StoreUpdateForm

from loja.produtos.models import Brand, Category, Store, VwStore, Color, Size, Packaging, Product
from loja.admin.models import User

# parâmetros da loja - chamado pela rota admin 
def parametrosloja():
    store_id = int(session['Store']['Id'])

    stores = VwStore.query.filter_by(id=store_id).first()
    if stores:
        session['Store'] = {'Cep origem': stores.zipcode, 'Taxa frete': stores.freight_rate,
                            'Página': stores.pages, 'Id': stores.id, 'Name': stores.name}
    return stores

# admin - lista de produtos
@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    parametrosloja()

    produtos = Product.query.all()
    return render_template('admin/index.html', titulo='Produtos', produtos=produtos)

# entrar com login do user
@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginFormulario(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            session['Store'] = None
            session['Store'] = {'Id': user.store_id}

            if user.store_id is None:
                session['Store'] = {'Id': 0}
                flash(f'Loja não vinculado ao seu login, comunique ao seu administrador!', 'danger')
                return render_template('admin/login.html', form=form, titulo='Login')
            session['email'] = form.email.data
            flash(f'{form.email.data} logado com sucesso!', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Não foi possível acessar o sistema!', 'danger')
    session['Store'] = ' '            
    return render_template('admin/login.html', form=form, titulo='Login')

# Registrar login do user
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

# Lista de Usuários - registrar a loja no usuário
@app.route('/registrarloja', methods=['GET','POST'])
def registrarloja():
    email = session["email"]
    print(f'email: {email}')
    if email != 'roeland.e.janssen@gmail.com':
        flash(f'Voce não está autorizado, ou faça o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    usuarios = User.query.all()
    return render_template('admin/usuarloja.html', titulo='Usuário | Loja', usuarios=usuarios)

# Cadastro de Usuários - alteração 
@app.route('/usuarlojaalt/<int:id>' , methods=['GET','POST'])
def usuarlojaalt(id):
    
    lojas = Store.query.all()
    loja = request.form.get('loja')    
    usuarios = User.query.get_or_404(id)

    if request.method == 'POST':
        usuarios.store_id = loja

        flash(f'Sua Marca foi Atualizada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('marcas'))
    

    return render_template('admin/usuarlojaalt.html', titulo='Atualizar Usuário | Loja', usuarios=usuarios, lojas=lojas)


# Cadastro de Usuários - exclusão 
@app.route('/usuarlojaexc/<int:id>' , methods=['POST'])
def usuarlojaexc(id):

    usuarios = User.query.get_or_404(id)
    if request.method == 'POST':
        try:
            db.session.delete(usuarios)
            db.session.commit()
            flash(f'Usuário(a) {usuarios.name} foi excluído(a) com sucesso!', 'success')
            return redirect(url_for('admin'))
        except Exception as erro:
            db.session.rollback()
            flash(f'Usuário(a) {usuarios.name} NÃO EXCLUÍDO(A)!', 'success')
            return redirect(url_for('admin'))
    flash(f'Usuário(a) {usuarios.name} não foi excluído(a)!', 'warning')
    return redirect(url_for('admin'))

# lista da loja
@app.route('/loja')
def loja():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    loja = Store.query.all()
    return render_template('admin/loja.html', titulo='Pagina Loja', loja=loja)

# Solicita cep da loja 
@app.route('/lojacep', methods=['GET','POST'])
def lojacep():
    loja = Store.query.all()
    if loja:
        flash(f'Loja já foi registrada!', 'danger')
        return redirect(url_for('admin'))
    form = ZipcodeForm()
    return render_template('admin/lojacep.html', form=form)

# Solicita dos dados da loja
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

# Inclusão da loja na base de dados
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

# Alteração da loja na base de dados
@app.route('/lojaalt/<int:id>' , methods=['GET','POST'])
def lojaalt(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updateloja = Store.query.get_or_404(id)
    name = request.form.get('name')
    freight = request.form.get('freight')
    pages = request.form.get('pages')
    form = StoreForm(request.form)


    if request.method == 'POST':
        updateloja.freight_rate = form.freight_rate.data
        updateloja.pages = form.pages.data
        updateloja.name = form.name.data
        flash(f'Sua Loja foi Atualizada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('loja'))
    
    form.name.data = updateloja.name
    form.freight_rate.data = updateloja.freight_rate
    form.pages.data = updateloja.pages

    return render_template('admin/lojaalt.html', titulo='Atualizar Fabricantes', updateloja=updateloja, form=form)

# Exclusão da loja na base de dados
@app.route('/lojaexc/<int:id>' , methods=['POST'])
def lojaexc(id):
    loja = Store.query.get_or_404(id)
    if request.method == 'POST':
        try:
            db.session.delete(loja)  
            db.session.commit()
            flash(f'A Loja {loja.name} foi excluída com sucesso!', 'success')
            return redirect(url_for('admin'))        
        except Exception as erro:
            db.session.rollback()
    flash(f'A Loja {loja.name} não foi excluída!', 'warning')
    return redirect(url_for('admin'))

# Lista das marcas
@app.route('/marcas')
def marcas():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    #marcas = Marca.query.all()
    store_id = int(session['Store']['Id'])
    marcas = Brand.query.filter_by(store_id=store_id).order_by(Brand.id.desc()).all()

    return render_template('admin/marca.html', titulo='Marcas', marcas=marcas)

# Lista das categorias
@app.route('/categorias')
def categorias():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    #categorias = Categoria.query.all()
    store_id = int(session['Store']['Id'])
    categorias = Category.query.filter_by(store_id=store_id).order_by(Category.id.desc()).all()

    return render_template('admin/marca.html', titulo='Categorias', categorias=categorias)

# Lista das cores
@app.route('/cores')
def cores():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    cores = Color.query.order_by(Color.id.desc()).all()

    return render_template('admin/cor.html', titulo='Cores', cores=cores)

# Lista dos tamanhos
@app.route('/tamanhos')
def tamanhos():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    tamanhos = Size.query.order_by(Size.id.desc()).all()

    return render_template('admin/cor.html', titulo='Tamanhos', tamanhos=tamanhos)

# Lista das embalagens
@app.route('/embalagens')
def embalagens():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    embalagens = Packaging.query.order_by(Packaging.id.desc()).all()

    return render_template('admin/embalagem.html', titulo='Embalagens', embalagens=embalagens)




