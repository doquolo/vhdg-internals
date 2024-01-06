from flask import Flask, render_template, send_file, request, redirect, url_for, jsonify
import json
import os
import datetime

app = Flask(__name__)

payment_list = []

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

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER    

@app.route('/pay', methods=['POST'])
def json_post():
    if request.is_json:
        try:
            data = request.get_json()
            payment_list.append(data)
            
            with open(f"data/{datetime.datetime.now().strftime('%d%m%Y')}.json", "w", encoding="utf-8") as file:
                raw_json = json.dumps(payment_list)
                file.write(raw_json)
                file.close()

            result = {'status': 'success'}
            return jsonify(result)
        except Exception as e:
            error_message = {'status': 'error', 'message': str(e)}
            print(error_message)
            return jsonify(error_message), 400
    else:
        # Return an error response if the request does not contain JSON data
        error_message = {'status': 'error', 'message': 'Request must contain JSON data'}
        print(error_message)
        return jsonify(error_message), 400

@app.route('/contactlesspay', methods=['POST'])
def upload_file():
    # Check if the POST request has a file part and JSON data
    if 'file' not in request.files or 'json_data' not in request.form:
        return redirect(request.url)

    file = request.files['file']
    json_raw = request.form['json_data']
    json_data = json.loads(json_raw)


    # If the user submits an empty form, redirect to the index page
    if file.filename == '' or json_raw == '':
        return redirect("/")

    # If the file is present and has a valid filename, save it to the server
    if file:
        # Ensure the 'uploads' folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save the file to the 'uploads' folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{json_data['id']}.{str(file.filename).split('.')[1]}")
        file.save(file_path)

        # save data
        payment_list.append(json_data)
        with open(f"data/{datetime.datetime.now().strftime('%d%m%Y')}.json", "w", encoding="utf-8") as file:
            raw_json = json.dumps(payment_list)
            file.write(raw_json)
            file.close()
            
        return redirect("/")
    
app.run("0.0.0.0", 80, True)