from flask import Flask, render_template, request, redirect, url_for
import json
import uuid

DATA_PATH = 'data/blog_posts.json'

app = Flask(__name__)


def load_blogposts(file_path):
    """
    Load blog posts from a JSON file.
    :param file_path: path to JSON file
    :return: list of dicts representing the blog posts
    """
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


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
    requested_post = next((post for post in blog_posts if post.get('id').strip() == post_id.strip()), None)
    return requested_post


@app.route('/')
def index():
    """
    Get blog posts from JSON file and render template.
    :return: rendered index.html template with all blog posts
    """
    blog_posts = load_blogposts(DATA_PATH)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle creating a new blog post.
    Accept GET requests to display the add form and POST requests
    to create a new blog post.
    Saves the new blog post with a UUID to the JSON file.
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
        new_id = str(uuid.uuid7())
        blog_posts.append({
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        })
        save_blogposts(DATA_PATH, blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<path:post_id>')
def delete(post_id):
    """
    Handle deleting a blog post from the JSON file.
    :param post_id: ID of the blog post to be deleted
    :return: redirect to the index page after saving
    """
    blog_posts = load_blogposts(DATA_PATH)
    updated_posts = [post for post in blog_posts if post.get('id').strip() != post_id.strip()]
    save_blogposts(DATA_PATH, updated_posts)
    return redirect(url_for('index'))


@app.route('/update/<path:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handle updating a blog post.
    Accept GET requests to display the update form and POST requests
    to update a blog post.
    Saves the updated blog post to the JSON file.
    :param post_id: ID of the blog post to be updated
    :return: rendered update.html template if GET, redirect to index page after saving if POST
    """
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
        updated_post = {'id': post.get('id').strip(), 'author': author, 'title': title, 'content': content}
        blog_posts = load_blogposts(DATA_PATH)
        blog_posts.remove(post)
        blog_posts.append(updated_post)
        save_blogposts(DATA_PATH, blog_posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
