from flask import Blueprint, render_template

my_recipe_blueprint = Blueprint("recipes", __name__, static_folder="static", template_folder="templates")

@my_recipe_blueprint.route("/home")
@my_recipe_blueprint.route("/")
def home():
    return render_template("index.html")
