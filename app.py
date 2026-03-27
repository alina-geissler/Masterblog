from flask import Flask, render_template, request, redirect, url_for
import json
import os

DATA_PATH = 'data/blog_posts.json'
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

app = Flask(__name__)


def load_blogposts(file_path):
    """
    Load blog posts from a JSON file.
    :param file_path: path to JSON file
    :return: list of dicts representing the blog posts
    """
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as e:
        return f"Error in file: {e}"
    except OSError as e:
        return f"Error: {e}"


def save_blogposts(file_path, posts):
    """
    Save all blog posts to the JSON file.
    :param file_path: path to JSON file
    :param posts: list of blog post dicts
    """
    with open(file_path, "w", encoding="utf-8") as file_updater:
        json.dump(posts, file_updater)


def fetch_post_by_id(post_id):
    """
    Fetch a specific blog post by its ID.
    :param post_id: ID of the blog post to be updated
    :return: blog post to be updated
    """
    blog_posts = load_blogposts(DATA_PATH)
    if isinstance(blog_posts, str):
        alert = blog_posts
        return render_template('index.html', alert_type='danger', alert=alert)
    requested_post = next((post for post in blog_posts if post.get('id') == post_id), None)
    return requested_post


@app.route('/')
def index():
    """
    Get blog posts from JSON file and render template.
    :return: rendered index.html template with all blog posts
    """
    blog_posts = load_blogposts(DATA_PATH)
    if isinstance(blog_posts, str):
        alert = blog_posts
        return render_template('index.html', alert_type='danger', alert=alert)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle creating a new blog post.
    Accept GET requests to display the add form and POST requests
    to create a new blog post.
    Save the new blog post with a unique ID to the JSON file.
    :return: rendered add.html template if GET, redirect to index page after saving if POST
    """
    if request.method == 'POST':
        author = request.form.get('author')
        if not author:
            author = 'Unknown Author'
        title = request.form.get('title')
        if not title:
            title = 'New Blog Post'
        content = request.form.get('content')
        if not content:
            content = 'No Content Available'
        blog_posts = load_blogposts(DATA_PATH)
        if blog_posts is str:
            alert = blog_posts
            return render_template('index.html', alert_type='danger', alert=alert)
        new_id = max((post.get('id', 0) for post in blog_posts), default=0) + 1
        blog_posts.append({
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        })
        save_blogposts(DATA_PATH, blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    Handle deleting a blog post from the JSON file.
    :param post_id: ID of the blog post to be deleted
    :return: redirect to the index page after saving
    """
    blog_posts = load_blogposts(DATA_PATH)
    if isinstance(blog_posts, str):
        alert = blog_posts
        return render_template('index.html', alert_type='danger', alert=alert)
    updated_posts = [post for post in blog_posts if post.get('id') != post_id]
    save_blogposts(DATA_PATH, updated_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handle updating a blog post.
    Accept GET requests to display the update form and POST requests
    to update a blog post.
    Update the blog post in the JSON file.
    :param post_id: ID of the blog post to be updated
    :return: rendered update.html template if GET, redirect to index page after saving if POST
    """
    blog_posts = load_blogposts(DATA_PATH)
    if isinstance(blog_posts, str):
        alert = blog_posts
        return render_template('index.html', alert_type='danger', alert=alert)
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        author = request.form.get('author')
        if not author:
            author = 'Unknown Author'
        title = request.form.get('title')
        if not title:
            title = 'New Blog Post'
        content = request.form.get('content')
        if not content:
            content = 'No Content Available'
        for post in blog_posts:
            if post.get('id') == post_id:
                post['author'] = author
                post['title'] = title
                post['content'] = content
                break
        save_blogposts(DATA_PATH, blog_posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
