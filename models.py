from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):

  __tablename__ = "users"

  def __repr__(self):
    p = self
    return f"<User id = {p.id} first_name = {p.first_name} last_name = {p.last_name} image_url = {p.image_url}>"
 

  id = db.Column(db.Integer, 
                 primary_key=True, 
                 autoincrement=True)

  first_name = db.Column(db.String(25), 
                         nullable=False, 
                         unique=False)

  last_name = db.Column(db.String(25), 
                        nullable=False, 
                        unique=False)

  image_url = db.Column(db.VARCHAR(), 
                        nullable=False, 
                        unique=True)