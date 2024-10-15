
from flask import render_template, request, flash,redirect, url_for
from models import db, Post, User, app



@app.route('/')
def home():
    user = Post.query.limit(100).all()
    return render_template('home.html', users=user)

@app.route('/blog/<int:id>')
def blog(id):
    blog = Post.query.get_or_404(id)
    return render_template ('blog.html', blog=blog)



@app.route('/link', methods=["GET", "POST"])
def link():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        email = request.form['email']
        slug = request.form['slug']
        blog = request.form['blog']
        post = Post(Title=title, Author=author, Email=email, Slug=slug, blog_post=blog, )

        db.session.add(post)
        db.session.commit()

        flash("Blog was added successfully.")

        return redirect('/')
    return render_template('form.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        data = User(Username=username, Name=name, Email=email, Password=password,)
        
        data.set_password(password)

        db.session.add(data)
        db.session.commit()

        flash("Login is Done.")

    log = User.query.limit(100).all()    
    return render_template('login.html', logs=log)
    

if __name__ == '__main__':
    app.run(debug=True)
