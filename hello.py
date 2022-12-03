from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# import base64
# from PIL import Image
# import torch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(50), nullable = False)
    lastname = db.Column(db.String(50), nullable = False)
    username = db.Column(db.String(50), unique = True, nullable = False)
    image_file = db.Column(db.String(50), nullable = False, default = 'default.jpg')
    items = db.relationship('Item', backref = 'user', lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.image_file}')"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    itemname = db.Column(db.String(20), nullable = False)
    link = db.Column(db.String(100), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    state = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Item('{self.itemname}', '{self.link}')"


@app.route("/")
def intro():
    user = User.query.all()[2]
    return render_template('profile.html', user=user)

@app.route("/edit", methods = ['GET', 'POST'])
def edit_my_profile():
    if request.method == 'POST': 
        file = request.files['imagefile']
        file.save('static/3.jpg')
        user = User.query.all()[2]
        user.firstname = request.form['firstName']
        user.lastname = request.form['lastName']
        user.username = request.form['username']
        user.image_file = '3.jpg'
        db.session.commit()
        return render_template('profile.html', user=user)
    elif request.method == 'GET':
        user = User.query.all()[2]
        return render_template('edit.html', user=user)
    


@app.route("/wishlist", methods = ['GET', 'POST'])
def wishlist():
    if request.method == 'POST':
        print(request.form)
        print(request.json)
        item = Item(itemname = request.json['itemname'], link = request.json['link'], user_id = 3)
        db.session.add(item)
        db.session.commit()
        return render_template('wishlist.html', item=item)
    elif request.method == 'GET':
        items = Item.query.filter(Item.state != 2).all()
        print(items)
        return render_template('wishlist.html', items=items)


@app.route("/itemstate", methods = ['POST'])
def itemstate():
    print(request.json)
    item = Item.query.get(request.json['id'])
    item.state = request.json['state']
    db.session.commit()
    return ""