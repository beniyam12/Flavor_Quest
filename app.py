import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://flavor_quest_ofxa_user:dcCHNtDq9shCZaqjTGjLy2jX8NZ7LZfk@dpg-cv1scraj1k6c73975bcg-a/flavor_quest_ofxa"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'inebbeni'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Contact {self.name}>'
    





API_KEY = "0329312fa1b943a49b245640c08a2872"
BASE_URL = "https://api.spoonacular.com/recipes/findByIngredients"

def get_recipes(ingredients, number):
    url = f"{BASE_URL}?apiKey={API_KEY}&ingredients={ingredients}&number={number}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  
    return None 

def get_recipe_instructions(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("analyzedInstructions", [])
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    
    return render_template("app_home.html") 

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        ingredients = request.form.get("ingredients")
        number = request.form.get("number")
        recipes = get_recipes(ingredients, number)

        recipes_with_instructions = []
        if recipes:
            for recipe in recipes:
                instructions = get_recipe_instructions(recipe['id'])
                recipe['instructions'] = instructions
                recipes_with_instructions.append(recipe)

        return render_template('recipe_results.html', recipes=recipes) 

    return render_template('recipe_form.html')

@app.route("/about")
def about():
    
    return render_template("app_about.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()

        flash("Thank you for contacting us! We will get back to you soon.", "success")
        
        
        return redirect(url_for('contact'))
    
    return render_template("app_contact.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
