from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restomenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

#Home wep App list All restaurants
@app.route('/')
@app.route('/restaurants')
def home():
    return "Home here"

# Add a new Restaurant
@app.route('/restaurant/new')
def newRestaurant():
    return "Create new Restautant"

# Edit a Restaurant @params id restaurant
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return "Edit restaurant"

# Delete a restaurant @params id restaurant
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return "Delete Restaurant "

# Show menu of restaurant @params id restaurant
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')

def showMenuItem(restaurant_id):
    return "Show menu of restaurant"
#new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return "Add a new menu item"

#edit menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "Edit menu item"

# delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuITem(restaurant_id, menu_id):
    return "Delete menu item"


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
