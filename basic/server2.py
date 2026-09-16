from flask import Flask,render_template

app = Flask(__name__)
def create_database():
    #1. connect to database
    connection = sqlite3.connect("users.db")
    #2. store db in objection
    #3. Write the Query using the object
    #4. commit the query
    #5. close the connection

@app.route("/")
def home():
    return render_template("register2.html")

if __name__ == "__main__":
    create_database()
    app.run(debug=True)