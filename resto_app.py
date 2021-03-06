from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restomenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

#Restaurant

#Restaurant APIGetPoint (GET Request)

@app.route('/JSON')
@app.route('/restaurants/JSON')

def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants = [resto.serialize for resto in restaurants])

@app.route('/restaurants/<int:restaurant_id>/JSON')
def restaurantJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return jsonify(restaurant = restaurant.serialize)

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
@app.route('/restaurant/<int:restaurant_id>/JSON')

def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return jsonify(MenuItems = [item.serialize for item in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')

def itemMenuJSON(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(menuItem = menu_item.serialize)



#Home wep App list All restaurants
@app.route('/')
@app.route('/restaurants')
def home():
    restaurants = session.query(Restaurant).all()
    return render_template('index.html', restaurants = restaurants)



# Add a new Restaurant
@app.route('/restaurant/new', methods = ['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newResto = Restaurant(name=request.form['restoName'])
        session.add(newResto)
        session.commit()
        flash("Restaurant successefully has been added")
        return redirect(url_for('home'))
    else:
        return render_template('newRestaurant.html')



# Edit a Restaurant @params id restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['restoName']:
            restaurant.name = request.form['restoName']
            session.add(restaurant)
            session.commit()
            flash("Restaurant successefully has been edited")
            return redirect(url_for('showMenuItem', restaurant_id = restaurant_id))
    else:
        return render_template('editRestaurant.html', restaurant = restaurant)



# Delete a restaurant @params id restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant successefully has been deleted")
        return redirect(url_for('home'))
    else:
        return render_template('deleteRestaurant.html', restaurant = restaurant)


#Manu Items


# Show menu of restaurant @params id restaurant
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def showMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('showMenuItem.html', restaurant = restaurant, items = items)



#new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        menu_item = MenuItem(name = request.form['nameMenu'], description=request.form['description'], price= request.form['price'], course= request.form['course'], restaurant_id = restaurant_id)
        session.add(menu_item)
        session.commit()
        flash("Menu item successefully has been added")
        return redirect(url_for('showMenuItem', restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant = restaurant )



#edit menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id = menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    print menu_item
    if request.method == 'POST':
        if request.form['nameMenu']:
            menu_item.name = request.form['nameMenu']
        if request.form['description']:
            menu_item.description = request.form['description']
        if request.form['price']:
            menu_item.price = request.form['price']
        if request.form['nameMenu']:
            menu_item.course = request.form['course']
        session.add(menu_item)
        session.commit()
        flash("Menu item successefully has been edited")
        return redirect(url_for('showMenuItem', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', item = menu_item, restaurant = restaurant)



# delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id= menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(menu_item)
        session.commit()
        flash("Menu item successefully has been deleted")
        return redirect(url_for('showMenuItem', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item = menu_item, restaurant = restaurant)



if __name__ == '__main__':
    app.secret_key = "my_super_secret_key"
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
