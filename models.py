from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

"""Models for Blogly."""
class User(db.Model):
    
    __tablename__ = 'users'
    
    default = 'https://louisianadirectseafood.com/wp-content/uploads/2017/10/default-img.png'
    
    id = db.Column(db.Integer,
                   primary_key=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.Text,
                          server_default=default,
                          default=default)
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    
    # def __repr__(self):
    #     return f"<User {self.first_name} {self.last_name} {self.image_url} >"


class Post(db.Model):
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(db.String(70),
                    nullable=False)
    content = db.Column(db.Text,
                    nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), 
                           server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    
    # user = db.relationship("User", backref='post_user')
    
    @property
    def friendly_date(self):
        """Return nice for human eyes date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
    def __repr__(self):
        return f"<Post {self.title} {self.content} {self.created_at} {self.user_id} >"
    
    

class PostTag(db.Model):
    
    __tablename__ = 'posts_tags'
    
    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tags.id'), primary_key=True)
    
    def __repr__(self):
        return f"<PostTag {self.post_id} {self.tag_id} >"
    
class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, 
                   primary_key=True)
    name = db.Column(db.Text, 
                     nullable=False, 
                     unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )
    
    
def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()