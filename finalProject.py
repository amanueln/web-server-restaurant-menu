from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name': 'Blue Burgers', 'id': '2'},
               {'name': 'Taco Hut', 'id': '3'}]

# Fake Menu Items
items = [
    {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'},
    {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert',
     'id': '2'},
    {'name': 'Caesar Salad', 'description': 'with fresh organic vegetables', 'price': '$5.99', 'course': 'Entree',
     'id': '3'}, {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'},
    {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer',
     'id': '5'}]
item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree'}

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def restaurantDb():
    showRestaurant = session.query(Restaurant).all()
    return showRestaurant


@app.route('/restaurant/')
def showRestaurants():
    return render_template('restaurants.html', restaurants=restaurantDb())


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    #make = Restaurant(name=request.form['name'])
    #session.add(make)
    #session.commit()
    return render_template('newrestaurant.html', restaurants=restaurantDb())


@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    editRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('editrestaurant.html', restaurants=editRestaurant)


@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    deleteRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('deleterestaurant.html', restaurants=deleteRestaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return render_template('newmenuitem.html', restaurants=restaurants)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurantMenu = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurants=restaurantMenu, items=menu)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenut(restaurant_id, menu_id):
    editMenu = session.query(MenuItem).filter_by(id=menu_id).one()
    return render_template('editmenuitem.html', menu=editMenu)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenut(restaurant_id, menu_id):
    deletetMenu = session.query(MenuItem).filter_by(id=menu_id).one()
    return render_template('deletemenuitem.html', menu=deletetMenu)


if __name__ == '__main__':
    app.secret_key = 'key'
    app.debug = True
    app.run(host='0.0.0.0', port=8081)
