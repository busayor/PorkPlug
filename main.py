from flask import Flask, render_template, url_for, request, session, flash, redirect
from admin.admin import my_admin_blueprint
from recipes.recipes import my_recipe_blueprint
from flask_material import Material
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Material(app)
#  in order to use session, you must set a secret key
app.secret_key = "l10nHear7"
app.permanent_session_lifetime = timedelta(minutes=1)
app.register_blueprint(my_admin_blueprint, url_prefix="/admin")
app.register_blueprint(my_recipe_blueprint, url_prefix="/recipes")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_users.sqlite3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a db as a model and give values
db = SQLAlchemy(app)
class my_users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")
    # return "<h1>Default landing page</h1>"


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form["email"]
        # session["email"] = email

        check_email = my_users.query.filter_by(email = email).first()
        if check_email != None:
            session["email"] = check_email.email
            return redirect(url_for("view"))
        else:
            flash("Invalid username or password")
            return render_template("login.html")
        
    return render_template("login.html")


@app.route("/signup", methods = ["GET", "POST"])
def signup():
        # here, we are about to receive the email from the use but first you must check the method type
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            session["email"] = email

            # check if email already exists before inserting
            found_user = my_users.query.filter_by(email = email).first()
            if found_user:
                flash("This email already exists!")
                return render_template("signup.html")
            else:
                # actual insertion happens here
                newUser = my_users(email = email,password = password)
                db.session.add(newUser)   
                db.session.commit()
                flash("Account successfully created!")
        return render_template("signup.html")


# page to render all the records of the my_users table
@app.route("/view")
def view():
    return render_template("viewusers.html", values = my_users.query.all())


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)