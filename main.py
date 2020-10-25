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
app.permanent_session_lifetime = timedelta(minutes=5)
app.register_blueprint(my_admin_blueprint, url_prefix="/admin")
# app.register_blueprint(my_recipe_blueprint, url_prefix="/recipes")
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


class recipes_db(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    meal_category = db.Column(db.String(20))
    recipe_name = db.Column(db.String(100))
    recipe_ingredients = db.Column(db.String(100))
    recipe_method = db.Column(db.String(100))
    recipe_image = db.Column(db.String(100))
    added_by = db.Column(db.String(100))

    def __init__(self, meal_category, recipe_name, recipe_ingredients, recipe_method, recipe_image, added_by):
        self.meal_category = meal_category
        self.recipe_name = recipe_name
        self.recipe_ingredients = recipe_ingredients
        self.recipe_method = recipe_method
        self.recipe_image = recipe_image
        self.added_by = added_by


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", values = recipes_db.query.all())
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
            return redirect(url_for("addrecipe"))
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
            cpassword = request.form["cpassword"]
            session["email"] = email

            # check if password == confirm password
            if password == cpassword:
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
            else:
                flash("Password and confirm password must be the same!")

        return render_template("signup.html")


@app.route("/logout")
def logout():
    flash("You have been logged out!", "info")
    session.pop("email", None)
    return redirect(url_for("login"))

# page to render all the records of the my_users table
@app.route("/view")
def view():
    return render_template("viewusers.html", values = my_users.query.all())


# page to render all the records of the recipesDB table
@app.route("/added_recipes")
def added_recipes():
    value = request.args.get('value', None)
    view_recipe = recipes_db.query.filter_by(_id = value).first()
    name = view_recipe.recipe_name
    flash(view_recipe)
    return render_template("added_recipes.html", name = name)


@app.route("/addrecipe", methods = ["GET", "POST"])
def addrecipe():
    if request.method == "POST":
            meal_category = request.form["meal_category"]
            recipe_name = request.form["recipe_name"]
            recipe_ingredients = request.form["recipe_ingredients"]
            recipe_method = request.form["recipe_method"]
            recipe_image = request.form["recipe_image"]
            added_by = session["email"]

            newRecipe = recipes_db(meal_category = meal_category,
            recipe_name = recipe_name,
            recipe_ingredients = recipe_ingredients,
            recipe_method = recipe_method,
            recipe_image = recipe_image,
            added_by = added_by
            )
            db.session.add(newRecipe)   
            db.session.commit()
            flash("New recipe added successfully!")
            # return redirect(url_for("recipes", values = recipes_db.query.all()))
    
    return render_template("addrecipe.html", email = session["email"])


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)