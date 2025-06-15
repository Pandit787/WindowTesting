from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Database setup (will create a new SQLite database file)
def init_db():
    conn = sqlite3.connect('testdb.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    c.execute("INSERT INTO users (username, password) VALUES ('user', 'user123')")
    conn.commit()
    conn.close()

# Home route for testing SQL injection
@app.route('/')
def home():
    return '''
        <form action="/login" method="GET">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# Login route (vulnerable to SQL injection)
@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    # SQL Injection vulnerable query
    conn = sqlite3.connect('testdb.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    c.execute(query)
    result = c.fetchall()

    if result:
        return "Login successful!"
    else:
        return "Invalid credentials."

# Run the application and initialize the database
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
