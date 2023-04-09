from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()

"""Models for Blogly."""
class User(db.Model):
    
    __tablename__ = 'users'
    
    default = 'https://louisianadirectseafood.com/wp-content/uploads/2017/10/default-img.png'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False,
                          server_default=default,
                          default=default)
    
    # def edit_user(self, first_name=first_name, last_name=last_name, image_url=image_url):
        