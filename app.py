from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config.from_pyfile('config.py')

connect_db(app)
db.create_all()

@app.route('/')
def home():
    """Redirects user to home page"""
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/new')
def create_user_form():
    """Displays the New User form to fill out"""
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """Submits form data to db, creates new user, and redirects back to users page"""
    
    first_name = request.form['First Name']
    last_name = request.form['Last Name']
    image_url = request.form['Image URL']
    image_url = image_url if image_url else None
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Displays user details"""
    user = User.query.get_or_404(user_id)
    
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Shows the edit details form to fill out"""
    user=User.query.get_or_404(user_id)
    return render_template('edit_details.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Submits updates to user to the db and redirects back to the user details page"""
    
    user = User.query.get(user_id)
    user.first_name = request.form['First Name']
    user.last_name = request.form['Last Name']
    user.image_url = request.form['Image URL'] or None
    
    db.session.commit()
    
    return redirect(f"/users/{user.id}")

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Displays a user's post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

@app.route('/users/<int:user_id>/posts/new')
def create_post_form(user_id):
    """Displays the New User form to fill out"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    """Submits form data to db, creates new user, and redirects back to users page"""
    user = User.query.get_or_404(user_id)
    title = request.form['Title']
    content = request.form['Content']
    
    tags_id = [int(num) for num in request.form.getlist('Tags')]
    tags = Tag.query.filter(Tag.id.in_(tags_id)).all()    
    
    new_post = Post(title=title, content=content, user=user, tags=tags)
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    """Shows the edit details form to fill out"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Submits updates to user to the db and redirects back to the user details page"""
        
    post = Post.query.get_or_404(post_id)
    post.title = request.form['Title']
    post.content = request.form['Content']
    
    tags_id = [int(num) for num in request.form.getlist('Tags')]
    tags = Tag.query.filter(Tag.id.in_(tags_id)).all()
    post.tags = tags if len(tags_id) > 0 else []
        
    db.session.add(post)
    db.session.commit()
    
    return redirect(f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete a user"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')


@app.route('/tags')
def list_tags():
    """Generates a list of all tags"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Shows details on a soecific tag"""
    tag = Tag.query.get_or_404(tag_id)
    # posts = Post.query.filter_by(tag_id=tag_id).all()
    
    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new')
def create_tag_form():
    """Displays the new tag form to fill out"""
    tags = Tag.query.all()
    return render_template('new_tag.html', tags=tags)

@app.route('/tags/new', methods=['POST'])
def create_tag():
    """Submits form data to db, creates new tag, and redirects back to tag page"""
    name = request.form['Name']
    
    post_ids = [int(num) for num in request.form.getlist('Posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    
    new_tag = Tag(name=name, posts=posts)
    db.session.add(new_tag)
    db.session.commit()
    
    return redirect('/tags')
    
@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag(tag_id):
    """Shows the edit details form to fill out"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit_tag.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """Submits updates to tags to the db and redirects back to the tag details page """
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['Name']
    post_ids = [int(num) for num in request.form.getlist('Posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    
    db.session.add(tag)
    db.session.commit()
    
    return redirect(f'/tags/{tag.id}')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Delete a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(f'/tags')
