from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/assets")
def serveAssets():
    

app.run("0.0.0.0", 80, True)