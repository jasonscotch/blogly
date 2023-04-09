from flask import Flask, render_template, request, redirect

from models import db, connect_db, User

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
    default = 'https://louisianadirectseafood.com/wp-content/uploads/2017/10/default-img.png'
    
    first_name = request.form['First Name']
    last_name = request.form['Last Name']
    image_url = request.form['Image URL']
    image_url = image_url if image_url else default
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Displays user details"""
    user=User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Shows the edit details form to fill out"""
    user=User.query.get_or_404(user_id)
    return render_template('edit_details.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Submits updates to user to the db and redirects back to the user details page"""
    default = 'https://louisianadirectseafood.com/wp-content/uploads/2017/10/default-img.png'
    
    user = User.query.get(user_id)
    user.first_name = request.form['First Name']
    user.last_name = request.form['Last Name']
    user.image_url = request.form['Image URL'] or default
    
    db.session.commit()
    
    return redirect(f"/users/{user.id}")

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


