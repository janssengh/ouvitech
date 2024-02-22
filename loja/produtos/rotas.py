import json
import os
import secrets
import flask
from loja.produtos.formularios import ProductForm, BrandForm
from flask import render_template, request, redirect, url_for, flash, current_app, session, make_response, jsonify
#from flask_sqlalchemy_session import flask_scoped_session
from loja import app, db, photos
from loja.produtos.models import Brand, Category, Store, VwStore, Color, Size, Packaging, VwPackaging, Product


# Cadastro de Marcas - inclusão 
@app.route('/marcainc', methods=['GET','POST'])
def marcainc():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    
    lojaid = (session['Store']['Id'])
    if request.method == "POST":
        getmarca = request.form.get('marca')
        marcas = Brand(store_id=lojaid, name=getmarca)
        try:
            db.session.add(marcas)
            flash(f'A marca {getmarca} foi cadastrada com sucesso!', 'success')
            db.session.commit()
            return redirect(url_for('marcainc'))
        except Exception as erro:
            db.session.rollback()
            flash(f'A marca {getmarca} não foi cadastrada, verifique se a loja foi cadastrada!', 'success')
            return redirect(url_for('marcainc'))
    return render_template('produtos/marcainc.html', marcas='marcas')

# Cadastro de Marcas - alteração 
@app.route('/marcaalt/<int:id>' , methods=['GET','POST'])
def marcaalt(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updatemarca = Brand.query.get_or_404(id)
    form = BrandForm(request.form)

    if request.method == 'POST':
        updatemarca.name = form.name.data

        flash(f'Sua Marca foi Atualizada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('marcas'))
    
    form.name.data = updatemarca.name
    #name = request.form.get('name')

    return render_template('produtos/marcaalt.html', titulo='Atualizar Fabricantes', updatemarca=updatemarca, form=form)

# Cadastro de Marcas - exclusão 
@app.route('/marcaexc/<int:id>' , methods=['POST'])
def marcaexc(id):

    marcas = Brand.query.get_or_404(id)
    if request.method == 'POST':
        try:
            db.session.delete(marcas)
            db.session.commit()
            flash(f'A Marca {marcas.name} foi excluída com sucesso!', 'success')
            return redirect(url_for('admin'))
        except Exception as erro:
            db.session.rollback()
            flash(f'A Marca {marcas.name} NÃO EXCLUÍDA! Verifique se há produtos desta marca !', 'success')
            return redirect(url_for('admin'))
    flash(f'A Marca {marcas.name} não foi excluída!', 'warning')
    return redirect(url_for('admin'))

# Cadastro de Categorias - inclusão 
@app.route('/categinc', methods=['GET','POST'])
def categinc():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    lojaid = (session['Store']['Id'])
    if request.method == "POST":
        getmarca = request.form.get('categoria')
        categorias = Category(store_id=lojaid, name=getmarca)
        try:
            db.session.add(categorias)
            flash(f'A Categoria {getmarca} foi cadastrada com sucesso!', 'success')
            db.session.commit()
            return redirect(url_for('categinc'))
        except Exception as erro:
            db.session.rollback()
            flash(f'A Categoria {getmarca} não foi cadastrada, verifique se a loja foi cadastrada!', 'success')
            return redirect(url_for('categinc'))
    return render_template('produtos/marcainc.html')

# Cadastro de Categorias - alteração 
@app.route('/categalt/<int:id>' , methods=['GET','POST'])
def categalt(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updatecat = Category.query.get_or_404(id)
    form = BrandForm(request.form)
    if request.method == 'POST':
        updatecat.name = form.name.data
        flash(f'Sua Categoria foi Atualizada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('categorias'))

    form.name.data = updatecat.name
    #name = request.form.get('name')
    return render_template('produtos/marcaalt.html', titulo='Atualizar Categoria', updatecat=updatecat, form=form)

# Cadastro de Categorias - exclusão
@app.route('/categexc/<int:id>' , methods=['POST'])
def categexc(id):

    categorias = Category.query.get_or_404(id)
    if request.method == 'POST':
        try:
            db.session.delete(categorias)
            db.session.commit()
            flash(f'A Categoria {categorias.name} foi excluída com sucesso!', 'success')
            return redirect(url_for('admin'))
        except Exception as erro:
            db.session.rollback()
            flash(f'A Categoria {categorias.name} NÃO EXCLUÍDA! Verifique se há produtos desta categoria !', 'success')
            return redirect(url_for('admin'))
    flash(f'A Categoria {categorias.name} não foi excluída!', 'warning')
    return redirect(url_for('admin'))


# Cadastro de Cores - inclusão 
@app.route('/corinc', methods=['GET','POST'])
def corinc():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    
    lojaid = (session['Store']['Id'])

    if request.method == "POST":
        getcor = request.form.get('cor')
        cores = Color(store_id=lojaid, name=getcor)
        try:
            db.session.add(cores)
            flash(f'A Cor {getcor} foi cadastrada com sucesso!', 'success')
            db.session.commit()
            return redirect(url_for('corinc'))
        except Exception as erro:
            db.session.rollback()
            flash(f'A Cor {getcor} não foi cadastrada, verifique se a loja foi cadastrada!', 'success')
            return redirect(url_for('corinc'))
    return render_template('produtos/corinc.html', cores='cores')

# Cadastro de Cores - alteração 
@app.route('/coralt/<int:id>' , methods=['GET','POST'])
def coralt(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updatecor = Color.query.get_or_404(id)
    form = BrandForm(request.form)

    if request.method == 'POST':
        updatecor.name = form.name.data
        flash(f'Sua Cor foi Atualizada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('cores'))
    
    form.name.data = updatecor.name
    return render_template('produtos/coralt.html', titulo='Atualizar Cores', updatecor=updatecor, form=form)

# Cadastro de Cores - exclusão 
@app.route('/corexc/<int:id>' , methods=['POST'])
def corexc(id):

    cores = Color.query.get_or_404(id)
    if request.method == 'POST':
        try:
            db.session.delete(cores)
            db.session.commit()
            flash(f'A Cor {cores.name} foi excluída com sucesso!', 'success')
            return redirect(url_for('admin'))
        except Exception as erro:
            db.session.rollback()
            flash(f'A Cor {cores.name} NÃO EXCLUÍDA! Verifique se há produtos desta cor !', 'success')
            return redirect(url_for('admin'))
    flash(f'A Cor {cores.name} não foi excluída!', 'warning')
    return redirect(url_for('admin'))

# Cadastro de Tamanhos - inclusão
@app.route('/tamanhoinc', methods=['GET','POST'])
def tamanhoinc():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    
    lojaid = (session['Store']['Id'])

    if request.method == "POST":
        getcor = request.form.get('tamanho')
        tamanhos = Size(store_id=lojaid, name=getcor)
        try:
            db.session.add(tamanhos)
            flash(f'O Tamanho {getcor} foi cadastrado com sucesso!', 'success')
            db.session.commit()
            return redirect(url_for('tamanhoinc'))
        except Exception as erro:
            db.session.rollback()
            flash(f'O Tamanho {getcor} não foi cadastrado, verifique se a loja foi cadastrada!', 'success')
            return redirect(url_for('tamanhoinc'))
    return render_template('produtos/corinc.html')

# Cadastro de Tamanhos - alteração 
@app.route('/tamanhoalt/<int:id>' , methods=['GET','POST'])
def tamanhoalt(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    
    updatetamanho = Size.query.get_or_404(id)
    form = BrandForm(request.form)

    if request.method == 'POST':
        updatetamanho.name = form.name.data
        flash(f'Seu Tamanho foi Atualizado com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('tamanhos'))
    
    form.name.data = updatetamanho.name
    return render_template('produtos/coralt.html', titulo='Atualizar Tamanho', updatetamanho=updatetamanho, form=form)

# Cadastro de Tamanhos - exclusão 
@app.route('/tamanhoexc/<int:id>' , methods=['POST'])
def tamanhoexc(id):

    tamanhos = Size.query.get_or_404(id)
    if request.method == 'POST':
        try:
            db.session.delete(tamanhos)
            db.session.commit()
            flash(f'O Tamanho {tamanhos.name} foi excluído com sucesso!', 'success')
            return redirect(url_for('admin'))
        except Exception as erro:
            db.session.rollback()
            flash(f'O Tamanho {tamanhos.name} NÃO EXCLUÍDO! Verifique se há produtos deste tamanho !', 'success')
            return redirect(url_for('admin'))
    flash(f'O Tamanho {tamanhos.name} não foi excluído!', 'warning')
    return redirect(url_for('admin'))

# Cadastro de Embalagem - Inclusão
@app.route('/embalinc', methods=['GET','POST'])
def embalinc():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    lojaid = (session['Store']['Id'])

    if request.method == "POST":
        format = request.form.get('format')
        weight = request.form.get('weight')
        length = request.form.get('length')
        height = request.form.get('height')
        width = request.form.get('width')

        if format == "1":
            format_name = "Caixa/Pacote"
        elif format == "2":
            format_name = "Rolo/Prisma"
        else:
            format_name = "Envelope"

        embalagens = Packaging(format=format, weight=weight, length=length, height=height,
                               width=width, store_id=lojaid)
        try:
            db.session.add(embalagens)
            flash(f'A embalagem {format_name} foi cadastrada com sucesso!', 'success')
            db.session.commit()
        except Exception as erro:
            db.session.rollback()
            flash(f'A embalagem {format_name}|{erro} não foi cadastrado, verifique se a mesma já foi cadastrada!', 'success')
        return redirect(url_for('embalinc'))
    return render_template('produtos/embalinc.html', embalagens='embalagens')

# Cadastro de Embalagem - Alteração
@app.route('/embalalt/<int:id>' , methods=['GET','POST'])
def embalalt(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updatepack = Packaging.query.get_or_404(id)
    weight = request.form.get('weight')
    length = request.form.get('length')
    height = request.form.get('height')
    width = request.form.get('width')
    format = request.form.get('format')
    if updatepack.format == 1:
        discformat = "Caixa/Pacote"
    elif updatepack.format == 2:
        discformat = "Rolo/Prisma"
    else:
        discformat = "Envelope"
    

    if request.method == 'POST':

        updatepack.format = format
        updatepack.weight = weight
        updatepack.length = length
        updatepack.height = height
        updatepack.width = width

        if updatepack.format == "1":
            format_name = "Caixa/Pacote"
        elif updatepack.format == "2":
            format_name = "Rolo/Prisma"
        else:
            format_name = "Envelope"

        flash(f'A sua Embalagem {format_name} foi Atualizada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('embalagens'))
    return render_template('produtos/embalalt.html', titulo='Atualizar Embalagens', updatepack=updatepack,
                           discformat=discformat)

# Cadastro de Embalagem - Exclusão
@app.route('/embalexc/<int:id>' , methods=['POST'])
def embalexc(id):

    embalagens = Packaging.query.get_or_404(id)
    if request.method == 'POST':
        if embalagens.format == 1:
            format_name = "Caixa/Pacote"
        elif embalagens.format == 2:
            format_name = "Rolo/Prisma"
        else:
            format_name = "Envelope"
        
        db.session.delete(embalagens)
        db.session.commit()
        flash(f'A Embalagem {format_name} foi excluída com sucesso!', 'success')
        return redirect(url_for('admin'))
    flash(f'A Marca {format_name} não foi excluída!', 'warning')
    return redirect(url_for('admin'))

# Cadastro do Produto - Inclusão
@app.route('/produtoinc', methods=['GET','POST'])
def produtoinc():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    marcas = Brand.query.all()
    categorias = Category.query.all()

    cores = Color.query.all()
    tamanhos = Size.query.all()

    embalagens = VwPackaging.query.all()

    form = ProductForm(request.form)

    lojaid = (session['Store']['Id'])

    if request.method == "POST":

        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        discription = form.discription.data
        if discount >= price:
            flash(f'Desconto maior ou igual ao preço não permitido!', 'danger')
            return render_template('produtos/produtoinc.html', form=form, titulo='Cadastro de Produto', marcas=marcas, categorias=categorias,
                           cores=cores, tamanhos=tamanhos, embalagens=embalagens)


        marca = request.form.get('marca')
        categoria = request.form.get('categoria')

        # colocar numa lista o id e name da cor e separa
        coridname = request.form.get('cor')
        coridname = (coridname.split(','))
        cor = coridname[0]
        colors = coridname[1]

        tamanho = request.form.get('tamanho')
        embalagem = request.form.get('embalagem')

        if not request.files.get('image_2'):
            flash(f'Imagem 2 é obrigatória !', 'danger')
            return render_template('produtos/produtoinc.html', form=form, titulo='Cadastro de Produto', marcas=marcas, categorias=categorias,
                           cores=cores, tamanhos=tamanhos, embalagens=embalagens)
        elif not request.files.get('image_3'):
            flash(f'Imagem 3 obrigatória !', 'danger')
            return render_template('produtos/produtoinc.html', form=form, titulo='Cadastro de Produto', marcas=marcas, categorias=categorias,
                           cores=cores, tamanhos=tamanhos, embalagens=embalagens)
        elif not request.files.get('image_1'):
            flash(f'Imagem 1 é obrigatória !', 'danger')
            return render_template('produtos/produtoinc.html', form=form, titulo='Cadastro de Produto', marcas=marcas, categorias=categorias,
                           cores=cores, tamanhos=tamanhos, embalagens=embalagens)

        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")

        try:

            addpro = Product(name=name, price=price, discount=discount, stock=stock, colors=colors, discription=discription,
                            brand_id=marca, category_id=categoria, image_1=image_1, image_2=image_2, image_3=image_3,
                            size_id=tamanho, color_id=cor, packaging_id=embalagem, store_id=lojaid)

            db.session.add(addpro)
            flash(f'Produto {name} foi cadastrado com sucesso!', 'success')
            db.session.commit()
            return redirect(url_for('admin'))
        except Exception as erro:
            db.session.rollback()
            flash(f'Produto {name} não foi cadastrado, verifique se o mesmo já foi cadastrado!', 'danger')
            return redirect(url_for('admin'))
    return render_template('produtos/produtoinc.html', form=form, titulo='Cadastro de Produto', marcas=marcas, categorias=categorias,
                           cores=cores, tamanhos=tamanhos, embalagens=embalagens)

# Cadastro de Produto - Alteração
@app.route('/produtoalt/<int:id>' , methods=['GET','POST'])
def produtoalt(id):
    marcas = Brand.query.all()
    categorias = Category.query.all()

    cores = Color.query.all()
    tamanhos = Size.query.all()
    embalagens = VwPackaging.query.all()

    produto = Product.query.get_or_404(id)
    ########################################
    marca = request.form.get('marca')
    categoria = request.form.get('categoria')
    ########################################
    cor = request.form.get('cor')
    tamanho = request.form.get('tamanho')
    ########################################
    embalagem = request.form.get('embalagem')
    vwpacks = VwPackaging.query.filter(VwPackaging.id == produto.embalagem.id)
    for vwpack in vwpacks:
        dimension = vwpack.dimension

    form = ProductForm(request.form)
    if request.method == "POST":

        produto.name = form.name.data
        produto.price = form.price.data
        produto.discount = form.discount.data
        #########################################
        produto.brand_id = marca
        produto.category_id = categoria
        #########################################
        produto.color_id = cor
        produto.size_id = tamanho
        #########################################
        produto.packaging_id = embalagem

        produto.stock = form.stock.data
        produto.colors = produto.cor.name
        produto.discription = form.discription.data
        if produto.discount >= produto.price:
            flash(f'Desconto maior ou igual ao preço não permitido!', 'danger')
            return render_template('produtos/produtoalt.html', titulo='Alterar Produtos', form=form, marcas=marcas,
                           categorias=categorias, produto=produto, cores=cores, tamanhos=tamanhos,
                           embalagens=embalagens, dimension=dimension)

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_1))
                produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_2))
                produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_3))
                produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f'Produto foi atualizado com sucesso!', 'success')
        return redirect(url_for('admin'))


    form.name.data = produto.name
    form.price.data = produto.price
    form.discount.data = produto.discount
    form.stock.data = produto.stock
    form.discription.data = produto.discription

    return render_template('produtos/produtoalt.html', titulo='Alterar Produtos', form=form, marcas=marcas,
                           categorias=categorias, produto=produto, cores=cores, tamanhos=tamanhos,
                           embalagens=embalagens, dimension=dimension)

# Cadastro de Produto - Exclusão
@app.route('/produtoexc/<int:id>' , methods=['POST'])
def produtoexc(id):

    produto = Product.query.get_or_404(id)

    if request.method == 'POST':
        try:
            if request.files.get('image_1'):
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_1))
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_2))
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_3))
        except Exception as e:
            print('Erro ')


        db.session.delete(produto)
        db.session.commit()
        flash(f'Produto {produto.name} foi excluído com sucesso!', 'success')
        return redirect(url_for('admin'))

    return redirect(url_for('admin'))