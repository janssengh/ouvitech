from flask import session
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf import FlaskForm
from wtforms import Form, IntegerField, StringField, TextAreaField, validators, DecimalField, SubmitField
from wtforms.validators import Length, DataRequired



class ProductForm(FlaskForm):
    name = StringField('Nome', validators=[validators.Length(min=20, max=80, message="Nome produto deve ter no mínimo 20 e no máximo 80 caracteres"),
                                                  validators.DataRequired('Faltou digitar o nome do produto')
                                                  ])
    price = DecimalField('Preço', validators=[validators.NumberRange(min=1, max=None, message="O preço deve ter valor no mínimo 1"),
                                                  validators.DataRequired('Faltou digitar o preço do produto')
                                                  ])
    discount = IntegerField('Valor do Desconto', validators=[validators.DataRequired('Faltou digitar o valor desconto do produto')])
    #discount = IntegerField('Valor do Desconto',[validators.DataRequired()])
    stock = IntegerField('Quantidade Estoque', validators=[validators.NumberRange(min=1, max=None, message="O preço deve ter valor no mínimo 1"),
                                                  validators.DataRequired('Faltou digitar a quantidade do estoque produto')])
    discription = TextAreaField('Descrição', validators=[validators.Length(min=20, max=250, message="Descrição do produto deve ter no mínimo 20 e no máximo 250 caracteres"),
                                                  validators.DataRequired('Faltou digitar a descrição do produto')
                                                  ])
    colors = TextAreaField('Cor :',[validators.DataRequired()])
    #url = StringField('URL :',[validators.DataRequired()])

    image_1 = FileField('Imagem 1 :', validators=[
                                                  FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_2 = FileField('Imagem 2 :', validators=[
                                                  FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_3 = FileField('Imagem 3 :', validators=[
                                                  FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    

    #submit = SubmitField('Cadastrar')
    

class BrandForm(FlaskForm):
    name = StringField('', validators=[validators.Length(min=1, max=45, message="Nome deve ter no mínimo 6 e no máximo 45 caracteres"),
                        validators.DataRequired(message='Entrada obrigatória !')])

