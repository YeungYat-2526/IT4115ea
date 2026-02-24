from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FloatField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    is_merchant = BooleanField('註冊為商戶帳號')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Add Product')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    content = TextAreaField('Content', validators=[Length(max=1000)])
    submit = SubmitField('Submit Review')

# 新增表單
class CategoryForm(FlaskForm):
    name = StringField('分類名稱', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('新增分類')

class OrderForm(FlaskForm):
    status = StringField('訂單狀態', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('建立訂單')

class OrderItemForm(FlaskForm):
    product_id = IntegerField('商品ID', validators=[DataRequired()])
    quantity = IntegerField('數量', validators=[DataRequired(), NumberRange(min=1)])
    price = FloatField('單價', validators=[DataRequired()])
    submit = SubmitField('新增訂單項目')

class AddressForm(FlaskForm):
    address = StringField('地址', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('新增地址')

class PaymentForm(FlaskForm):
    order_id = IntegerField('訂單ID', validators=[DataRequired()])
    amount = FloatField('金額', validators=[DataRequired()])
    submit = SubmitField('付款')

class EditProductForm(FlaskForm):
    name = StringField('商品名稱', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('商品描述')
    price = FloatField('價格', validators=[DataRequired()])
    submit = SubmitField('更新商品')

