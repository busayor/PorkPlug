from flask import Blueprint, render_template

my_admin_blueprint = Blueprint("second", __name__, static_folder="static", template_folder="templates")

@my_admin_blueprint.route("/home")
@my_admin_blueprint.route("/")
def home():
    return render_template("index.html")


@my_admin_blueprint.route("/super")
def superAdmin():
    # return render_template("index.html")
    return "<h1>Super Admin landing page</h1>"