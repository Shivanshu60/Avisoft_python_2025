import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse

# Database file name
DB_FILE = "blog.db"

# Initialize the database: create the posts table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# HTML templates (very basic) using Python string formatting
INDEX_TEMPLATE = """
<html>
<head><title>My Blog</title></head>
<body>
<h1>My Blog</h1>
<ul>
{posts}
</ul>
<a href="/new">New Post</a>
</body>
</html>
"""

POST_TEMPLATE = """
<html>
<head><title>{title}</title></head>
<body>
<h1>{title}</h1>
<div>{content}</div>
<br>
<a href="/">Back</a>
</body>
</html>
"""

NEW_POST_TEMPLATE = """
<html>
<head><title>New Post</title></head>
<body>
<h1>Create New Post</h1>
<form method="POST" action="/new">
  Title: <input type="text" name="title"><br>
  Content:<br>
  <textarea name="content" rows="10" cols="30"></textarea><br>
  <input type="submit" value="Submit">
</form>
<a href="/">Back</a>
</body>
</html>
"""

class BlogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path
        query = urlparse.parse_qs(parsed_path.query)
        
        if path == '/':
            self.handle_index()
        elif path == '/post':
            self.handle_post(query)
        elif path == '/new':
            self.handle_new_post_form()
        else:
            self.send_error(404, "Page not found")
    
    def do_POST(self):
        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path
        
        if path == '/new':
            self.handle_new_post_submit()
        else:
            self.send_error(404, "Page not found")
    
    def handle_index(self):
        """Display a list of blog posts."""
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT id, title FROM posts ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        
        # Build the list of posts as HTML list items
        posts_list = ""
        for post_id, title in rows:
            posts_list += f'<li><a href="/post?id={post_id}">{title}</a></li>'
        
        content = INDEX_TEMPLATE.format(posts=posts_list)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())
    
    def handle_post(self, query):
        """Display a single post, given an 'id' query parameter."""
        if 'id' not in query:
            self.send_error(400, "Bad Request: missing id")
            return
        
        post_id = query['id'][0]
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT title, content FROM posts WHERE id = ?", (post_id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            title, content_post = row
            content = POST_TEMPLATE.format(title=title, content=content_post)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode())
        else:
            self.send_error(404, "Post not found")
    
    def handle_new_post_form(self):
        """Display the form for creating a new post."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(NEW_POST_TEMPLATE.encode())
    
    def handle_new_post_submit(self):
        """Process the form submission for a new post."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode()
        post_params = urlparse.parse_qs(post_data)
        
        title = post_params.get('title', [''])[0]
        content_post = post_params.get('content', [''])[0]
        
        if not title or not content_post:
            self.send_error(400, "Title and content are required")
            return
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content_post))
        conn.commit()
        conn.close()
        
        # Redirect back to the homepage after successful submission
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

def run(server_class=HTTPServer, handler_class=BlogHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Blog server running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
