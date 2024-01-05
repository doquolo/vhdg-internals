from flask import Flask, render_template, send_file, request
import json

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/assets")
def serveAssets():
    args = request.args
    img_name = args.get("image", default="", type=str)
    return send_file(f"assets//{img_name}")

@app.route("/foodlist")
def serveFoodlist():
    with open("data/foodlist.json", "r", encoding="utf-8") as file:
        food_obj = json.loads(file.read())
        food_list = {}
        for id in food_obj:
            food_list[id] = food_obj[id]["name"]
        return food_list
    
@app.route("/price")
def price():
    args = request.args
    id = args.get("id", default="", type=str)
    with open("data/foodlist.json", "r", encoding="utf-8") as file:
        food_obj = json.loads(file.read())
        return food_obj[id]["price"]

app.run("0.0.0.0", 80, True)