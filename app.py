# Imports
from flask import Flask, redirect, render_template, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# My App
app = Flask(__name__)
Scss(app, static_dir="static", asset_dir="assets")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# Data Class ~ row of data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"



# Index is homepage so we create route using Flask decorator
# Routes to Webpages
## Homespage ##
@app.route("/",methods=["POST","GET"]) # Route Decorator for Flask ~ also allows for sending/recingin data
def index():
    # Add a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    # See all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)

# Delete an Item
@app.route("/delete/<int:id>") #Route to page url and id #
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"

# Edit an item
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error:{e}"
    else:
        return render_template('edit.html', task=task)

# Runner and Debugger
if __name__ in "__main__":
    with app.app_context():   
        db.create_all()

    app.run(debug=True)