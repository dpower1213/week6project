from sqlalchemy import false
from .import bp as site
from flask import render_template, request, flash, redirect, url_for
import requests
from flask_login import login_required, current_user
from .forms import ItemForm
from app.models import Inv, User, db, UserCart

@site.route('/delete_item/<int:id2>')
@login_required
def delete_item(id2):
    item_to_delete = Inv.query.get(id2)
    i = UserCart.query.filter(UserCart.user_id == current_user.user_id, UserCart.item_id == item_to_delete.item_id).first()
    print(i)
    i.delete()
    db.session.commit()
    flash('Item Sucessfully Deleted')
    return redirect(url_for('site.show_cart'))
        
@site.route('/')
def index():
    return render_template('index.html.j2')
    
@site.route('/item', methods=['GET','POST'])
@login_required
def item():
    form = ItemForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_item_data = {
            "upc":form.upc.data.title(),
            "item_name":form.item_name.data.title(),
            "item_desc":form.item_desc.data.lower(),
            "item_price":form.item_price.data 
            }
            
            new_item_object=Inv()
            new_item_object.from_dict(new_item_data)
            new_item_object.save()
                
        except:
            flash('Oooppps, that was awful......awful entertaining')
            return render_template('item.html.j2',form=form)    
        return render_template('item.html.j2',form=form)
    return render_template('item.html.j2',form=form)

@site.route('/show_items')
@login_required
def show_items():
    items=Inv.query.all()
    return render_template('show_items.html.j2', items=items)
    
@site.route('/add_items<int:id>')
@login_required
def add_items(id):
    addition = Inv.query.get(id)
    current_user.itemss.append(addition)
    db.session.commit()
    return redirect (url_for('site.show_items'))
    
@site.route('/show_cart')
@login_required
def show_cart():
    return render_template('show_cart.html.j2')
    
@site.route('/delete_cart')
@login_required
def delete_cart():
    cart_to_delete = current_user.itemss.all()
    print(cart_to_delete)
    try:
        for thing in cart_to_delete:
            i = UserCart.query.filter(UserCart.user_id == current_user.user_id, UserCart.item_id == thing.item_id)
            i.delete()
            db.session.commit()
        flash('Cart Sucessfully Deleted')
        return redirect(url_for('site.show_cart'))
    except:
        flash("Error Deleting the Cart")
        return redirect(url_for('site.show_cart'))
    
@site.route('/show_item<int:id>')
@login_required
def show_item(id):
    a = Inv.query.get(id)
    return render_template('show_item.html.j2', a=a)