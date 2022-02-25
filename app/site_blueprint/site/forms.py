from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

# class ItemForm(FlaskForm):
#     name = StringField(validators=[DataRequired()])
#     submit = SubmitField('Pokemon Name')
    
#     item_id = StringField(validators=[DataRequired()])
#     submit2 = SubmitField('Pokemen Delete')
    
class ItemForm(FlaskForm):
    upc = StringField('UPC', validators=[DataRequired()])
    item_name = StringField('Item Name', validators=[DataRequired()])
    item_desc = StringField('Description', validators=[DataRequired()])
    item_price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('New Item')