from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
# MySQL connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="GayatriMysql@123",
    database="company1"
)

# Create a cursor object
cursor = db.cursor()

# Route for the form
@app.route('/')
def form():
    return render_template('form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    cursor.execute("SELECT * FROM logininfo WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        # If the user already exists, return a message or redirect them
        return "User with this email already logged in!"
    else:
        # If the user doesn't exist, insert their data
        cursor.execute("INSERT INTO logininfo (name, email) VALUES (%s, %s)", (name, email))
        db.commit()
    return redirect('/')

# Route to handle logout
@app.route('/logout', methods=['POST'])
def logout():
    email = request.form['email']
    cursor.execute('DELETE FROM logininfo WHERE email=%s', (email,))
    
    # Commit the transaction
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
