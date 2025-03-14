from flask import render_template, request, flash, redirect, url_for, session
from models import db, Post, User, Reaction, app, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirects to login page if user is not logged in

# load_user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    session['unauthorized_access'] = True
    # Flash the message when the user is not authorized
    flash('Please login to access this page.', 'danger')
    return redirect('/login')

@app.route('/')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', users=posts)

@app.route('/blog/<int:id>')
@login_required
def blog(id):
    blog = Post.query.get_or_404(id)
    return render_template('blog.html', blog=blog)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    edit = Post.query.get_or_404(id)
    if edit.user_id != current_user.id:
        flash("You are not authorized to edit this post.", 'danger')
        return redirect(url_for('home'))

    if request.method == "POST":
        edit.Title = request.form['title']
        edit.Author = request.form['author']
        edit.Email = request.form['email']
        edit.Slug = request.form['slug']
        edit.blog_post = request.form['blog']

        db.session.commit()

        flash("Blog was edited successfully.", 'primary')
        return redirect('/')
    return render_template('edit.html', edit=edit)

@app.route('/delete_blog/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_blog(id):
    delete_blog = Post.query.get_or_404(id)
    if delete_blog.user_id != current_user.id:
        flash("You are not authorized to delete this post.", 'danger')
        return redirect(url_for('home'))

    db.session.delete(delete_blog)
    db.session.commit()

    flash("Blog was deleted successfully.", 'success')
    return redirect('/')

@app.route('/react/<int:post_id>/<string:reaction_type>', methods=['POST'])
@login_required
def react(post_id, reaction_type):
    post = Post.query.get_or_404(post_id)
    existing_reaction = Reaction.query.filter_by(post_id=post_id, user_id=current_user.id).first()

    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            # Remove the reaction if the user clicks the same button again
            db.session.delete(existing_reaction)
            db.session.commit()
        else:
            # Update reaction type if the user switches from like to dislike or vice versa
            existing_reaction.reaction_type = reaction_type
            db.session.commit()
    else:
        # Add a new reaction
        new_reaction = Reaction(post_id=post_id, user_id=current_user.id, reaction_type=reaction_type)
        db.session.add(new_reaction)
        db.session.commit()

    # Recalculate like and dislike counts
    like_count = Reaction.query.filter_by(post_id=post_id, reaction_type='like').count()
    dislike_count = Reaction.query.filter_by(post_id=post_id, reaction_type='dislike').count()

    # Update the Post model
    post.like_count = like_count
    post.dislike_count = dislike_count
    db.session.commit()

    flash('Reaction updated!', 'success')
    return redirect(url_for('home'))

@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '')
    search_results = Post.query.filter(
        Post.Title.like(f'%{query}%') |
        Post.blog_post.like(f'%{query}%')
    ).all()

    return render_template('search_result.html', results=search_results, query=query)



@app.route('/link', methods=["GET", "POST"])
@login_required
def link():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        email = request.form['email']
        slug = request.form['slug']
        blog = request.form['blog']
        post = Post(Title=title, Author=author, Email=email, Slug=slug, blog_post=blog, user_id=current_user.id)

        db.session.add(post)
        db.session.commit()

        flash("Blog was added successfully.", 'success')
        return redirect('/')
    return render_template('form.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    sign = User.query.all()
    if request.method == "POST":
        user_name = request.form.get('username')
        name = request.form.get('name')
        user_email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(Username=user_name).first()
        id_match = User.query.filter_by(Email=user_email).first()

        if user is None and id_match is None:
            data = User(Username=user_name, Name=name, Email=user_email, Password=password)
            data.set_password(password)
            db.session.add(data)
            db.session.commit()

            flash("Signup is Done.", "success")
            return redirect(url_for('home'))
        else:
            if user is not None:
                flash(f'Username {user_name} already exists', 'danger')
            elif id_match is not None:
                flash(f'Email {user_email} already exists', 'danger')
            else:
                flash('An error occurred. Please try again.', 'danger')

    return render_template('signup.html', signs=sign)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        user_email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user exists in the database
        user = User.query.filter_by(Email=user_email).first()

        # Validate user credentials
        if user:
            if user.check_password(password):
                # If the credentials are valid, log the user in
                session.pop('unauthorized_access', None)

                login_user(user)

                flash('Login successful!', 'success')
                return redirect(url_for('home'))  # Redirect to the home page
            else:
                # If the credentials are invalid, show an error message
                flash('Invalid email or password. Please try again.', 'danger')
        else:
            flash(f"User email {user_email} doesn't exist", 'danger')

    # Render the login page for GET requests
    return render_template('login.html')

@app.route('/logout')
@login_required  # Restricting access to logged-in users only
def logout():
    logout_user()  # Logs the user out
    flash('You have been logged out.', 'info')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5002)
