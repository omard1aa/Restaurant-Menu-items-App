from flask import Flask, url_for, render_template, redirect, request, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Base


app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/restaurants/')
def show_restaurants():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    print('GET !!!  ! ! ! ! !')
    return render_template('show_restaurants.html', restaurants=restaurants)


@app.route('/restaurants/new/', methods=['GET', 'POST'])
def new_restaurant():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('show_restaurants'))
    else:
        return render_template("new_restaurant.html")


@app.route('/restaurant/<int:restaurant_id>/menu/')
def show_menu(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('restaurant_menu.html', restaurant_id=restaurant_id, items=items, restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def new_item(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item =''
    if request.method == 'POST':
        item = MenuItem(name=request.form['name'], description=request.form['description'],
                        price=request.form['price'], course=request.form['course'],
                        restaurant_id=restaurant_id)
        session.add(item)
        session.commit()
        flash("New menu %s item has been created!" %item.name)
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template('new_item.html', restaurant_id=restaurant_id, item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['POST', 'GET'])
def edit_menu(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    print("hi out of the post")
    if request.method == 'POST':
        print("Hi from post")
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['price']:
            item.price = request.form['price']
        if request.form['course']:
            item.course = request.form['course']
        session.commit()
        flash("%s has been edited!" %item.name)
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template('edit_item.html', restaurant_id=restaurant_id, item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['POST', 'GET'])
def delete_item(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("%s has been deleted!" % item.name)
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template('delete_item.html', restaurant_id=restaurant_id, menu_id=menu_id, item=item)


@app.route('/restaurant/delete/', methods=['POST', 'GET'])
def delete_restaurant():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(id=int(request.form['id'])).one()
        session.delete(restaurant)
        session.commit()
        flash("%s Restaurant has been deleted" % restaurant.name)
        return redirect(url_for('show_restaurants'))
    return render_template('delete_restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/json')
def show_restaurant_JSON(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return jsonify(Restaurant=restaurant.serialize)
    # return "This page is made to retrieve restaurants JSON data "


@app.route('/restaurants/json')
def show_restaurants_JSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[restaurant.serialize for restaurant in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/json')
def show_restaurantMenus_JSON(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    menus = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItem=[menu.serialize for menu in menus])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/json')
def menuItemJSON(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


if __name__ == '__main__':
    app.secret_key = "Super_secret_power_key"
    _host_ = '0.0.0.0'
    _port_ = 8080
    app.debug = True
    app.run(host=_host_, port=_port_)
