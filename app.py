from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

users = {
    "Dhaval": generate_password_hash("Shah"),
    "Admin": generate_password_hash("Admin")
}


class Todo(db.Model) :

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():

    todo_list = Todo.query.all()
    return render_template("index.html", todo_list = todo_list)

@app.route("/add", methods = ["POST"])
def add():

    title = request.form.get("title")
    new_todo = Todo(title = title, complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>", methods = ["POST"])
def update(todo_id):
    
    edit_text = request.form['edit_text']
    todo = Todo.query.get(todo_id)
    todo.title = edit_text
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    
    todo = Todo.query.filter_by(id = todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__" :
    db.create_all()
    app.run(debug=True)