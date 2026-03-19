from flask import Flask, render_template, request
import json
import uuid

DATA_PATH = 'blog_posts.json'

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
    :return:
    """
    with open(file_path, "w", encoding="utf-8") as file_updater:
        json.dump(posts, file_updater)


@app.route('/')
def index():
    blog_posts = load_blogposts(DATA_PATH)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        blog_posts = load_blogposts(DATA_PATH)
        new_id = str(uuid.uuid7())
        blog_posts.append({
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        })
        save_blogposts(DATA_PATH, blog_posts)
        return render_template('index.html', posts=blog_posts)
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
