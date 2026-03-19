from flask import Flask, render_template
import json

DATA_PATH = 'blog_posts.json'

app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = load_blogposts(DATA_PATH)
    return render_template('index.html', posts=blog_posts)


def load_blogposts(file_path):
    """
    Load blog posts from a JSON file.
    :return:
    """
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

