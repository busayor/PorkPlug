from flask import Flask, render_template
from admin.admin import my_admin_blueprint
from recipes.recipes import my_recipe_blueprint
from flask_material import Material

app = Flask(__name__)
Material(app)
app.register_blueprint(my_admin_blueprint, url_prefix="/admin")
app.register_blueprint(my_recipe_blueprint, url_prefix="/recipes")

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")
    # return "<h1>Default landing page</h1>"


if __name__ == "__main__":
    app.run(debug=True)