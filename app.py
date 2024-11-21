from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your Spoonacular API key
API_KEY = "0329312fa1b943a49b245640c08a2872"
BASE_URL = "https://api.spoonacular.com/recipes/findByIngredients"

# Function to get recipes from the Spoonacular API
def get_recipes(ingredients, number):
    url = f"{BASE_URL}?apiKey={API_KEY}&ingredients={ingredients}&number={number}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  
    return None 

def get_recipe_instructions(recipe_id):
    url = f"{BASE_URL}/{recipe_id}/information?apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("analyzedInstructions", [])
    return None

# Route to display form and handle recipe search
@app.route("/", methods=["GET", "POST"])
def index():
    
    return render_template("app_home.html")  # Render the form on GET request

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        ingredients = request.form.get("ingredients")
        number = request.form.get("number")
        recipes = get_recipes(ingredients, number)
        instructions = get_recipe_instructions(recipe_id)
        return render_template('recipe_results.html', recipes=recipes, instructions=instructions)

    return render_template('recipe_form.html')

@app.route("/about")
def about():
    
    return render_template("app_about.html")

@app.route("/contact")
def contact():
    
    return render_template("app_contact.html")

app.run(host="0.0.0.0", port=5001, debug=True)
