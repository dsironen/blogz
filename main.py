from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'ThisIsMySecretKey'

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    '''Displays previous blog posts.'''
    blogs = Blog.query.all()

    if request.args:
        return redirect('/blogpost')

    return render_template('index.html', blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    '''Displays newpost.html and delivers form data to index.html'''
    if request.method == 'POST':
        title = request.form['blog-title']
        body = request.form['blog-body']

        if title == "":
            flash('Please enter a blog title', 'error')
            return render_template('newpost.html', body=body)
        elif body == "":
            flash("Please enter a blog title and an new blog entry!", 'error')
            return render_template('newpost.html', title=title)

        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.flush()
        db.session.commit()

        num = new_blog.id
        return redirect('/blogpost?id={0}'.format(num))

    return render_template('newpost.html')


@app.route('/blogpost', methods=['POST', 'GET'])
def blogpost():
    '''Displays individual blog entries as selected by blog.id.'''
    num = request.args.get('id')
    blog = Blog.query.filter_by(id=num).first()
    return render_template('blogpost.html', blog=blog)

if __name__ == "__main__":
    app.run()      