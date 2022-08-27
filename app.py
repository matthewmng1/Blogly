from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db' #must do this data base before the other db below
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ITSASECRET'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_users():
  users = User.query.all()
  return render_template('list.html', users=users)

@app.route('/', methods=['POST'])
def create_user():
  first_name = request.form["first_name"]
  last_name = request.form["last_name"]
  image_url = request.form["image_url"]

  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)  
  db.session.add(new_user)
  db.session.commit()
  return redirect(f"/{new_user.id}")

@app.route('/<int:user_id>')
def show_user(user_id):
  """Show details about a single user"""
  user = User.query.get_or_404(user_id)
  return render_template("details.html", user=user)

@app.route('/edit/<int:user_id>')
def edit_page(user_id):
  """Edit user details"""
  user = User.query.get_or_404(user_id)
  return render_template("edit_user.html", user=user)

@app.route('/edit/<int:user_id>', methods=['POST'])
def edit_user(user_id):
  user = User.query.get(user_id)

  user.first_name = request.form["edit-first-name"]
  user.last_name = request.form["edit-last-name"]
  user.image_url = request.form["edit-image-url"]
  
  db.session.add(user)
  db.session.commit()
  
  return redirect(f"/{user.id}")

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
  user = User.query.get(user_id)

  User.query.filter(User.id == user_id).delete()

  db.session.commit()

  return render_template("confirm-delete.html", user=user)

  


#  <form action="/edit/{{user.id}}" method="POST">
#     First Name <br>
#     <input type="text" name="edit-first-name" value="{{user.first_name}}"><br>
#     Last Name <br>
#     <input type="text" name="edit-last-name" value="{{user.last_name}}"><br>
#     Profile Picture <br>
#     <input type="text" name="edit-image-url" value="{{user.image_url}}"><br>
#     <button>Save</button>
# @app.route('/species/<species_id>')
# def show_pets_by_species(species_id):
#   pets = Pet.get_by_species(species_id)
#   return render_template("species.html", pets=pets, species=species_id)