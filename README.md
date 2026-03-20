# :pencil: Masterblog - My Flask Blog Project

**Web-based Blog Manager with Full CRUD Functionality**

A Flask web application to manage your personal blog.
Add, edit and delete blog posts via a clean web interface,
store them in JSON, and view all posts on a responsive index page.

## :sparkles: Features

- **CRUD Operations**: Add, update and delete blog posts
- **Pre-filled Forms**: Update form auto-populates with existing post data
- **Unique IDs**: Each post gets a UUID7 on creation
- **Default Values**: Fallback values for empty form fields
- **Storage**: JSON file-based persistence
- **Responsive UI**: Clean CSS layout with color-coded action buttons

## :file_folder: Project Structure

```
Masterblog/
├── data/
│   └── blog_posts.json
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   ├── add.html
│   └── update.html
├── app.py
├── README.md
└── requirements.txt 
```

## :wrench: Setup & Usage

1. **Clone the repository**  
`git clone ...`
2. **Install virtual env**  
Windows: `python -m venv .venv`  
Linux / macOS: `python3 -m venv .venv`
3. **Install dependencies**  
Windows: `pip install -r requirements.txt`  
Linux / macOS: `pip3 install -r requirements.txt`
4. **Run the application**  
Windows: `python app.py`  
Linux / macOS: `python3 app.py`
5. **Open in browser**  
`http://127.0.0.1:5000`


## :clipboard: Routes

| Route               | Method    | Description                            |
|---------------------|-----------|----------------------------------------|
| `/`                 | GET       | Show all blog posts                    |
| `/add`              | GET, POST | Display form / save new post           |
| `/update/<post_id>` | GET, POST | Display pre-filled form / save changes |
| `/delete/<post_id>` | GET       | Delete post by ID                      |

## :package: Dependencies

`flask` - web framework for routing, templates and form handling

