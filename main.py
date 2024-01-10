from flask import Flask, render_template, send_file, request, redirect, url_for, jsonify
import json
import os
import datetime
from htmlPrintTemplate import head, template
import subprocess
import os

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

def print_bill(bill):
    sum = 0
    list = ""
    print(bill)
    for dish in bill["data"]:
        dish = str(dish)
        print(bill["data"][dish])
        dishSum = int(bill["data"][dish]["amount"]) * int(bill["data"][dish]["price"])
        sum += dishSum
        list += f'''
<tr>
    <td>x{bill["data"][dish]["amount"]} {bill["data"][dish]["name"]}</td>
    <td>{bill["data"][dish]["price"]}.000đ</td>
    <td>{dishSum}.000đ</td>
</tr>
'''
    
    html = head + template.format(
        id=bill["id"], 
        datetime=datetime.datetime.fromtimestamp(int(bill["id"]) / 1e3), 
        payment_method=("Tiền mặt" if bill["mode"] == "cash" else "Chuyển khoản"),
        payment_list=list,
        sum=f"{sum}.000đ"
    )

    with open("temp.html", "w", encoding="utf-8") as file:
        file.write(html)
        file.close()

    # define path to essensial files
    path_to_converter = r"tools\printer\wkhtmltox\bin\wkhtmltopdf.exe"
    path_to_input_file = r"temp.html"
    path_to_output_file = r"temp.pdf"

    # run converter
    converter = subprocess.run([path_to_converter, path_to_input_file, path_to_output_file])

    # print
    path_to_printer = r"tools\printer\pdftoprinter\PDFtoPrinter.exe"
    printer = subprocess.run([path_to_printer, path_to_output_file, "/s"])


@app.route('/pay', methods=['POST'])
def json_post():
    if request.is_json:
        # try:
        data = request.get_json()
        payment_list.append(data)
        
        with open(f"data/{datetime.datetime.now().strftime('%d%m%Y')}.json", "w", encoding="utf-8") as file:
            raw_json = json.dumps(payment_list)
            file.write(raw_json)
            file.close()

        # print bill
        print_bill(data)

        result = {'status': 'success'}
        return jsonify(result)
        # except Exception as e:
        #     error_message = {'status': 'error', 'message': str(e)}
        #     print(error_message)
        #     return jsonify(error_message), 400
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

        # print bill
        print_bill(json_data)
            
        return redirect("/")
    
app.run("0.0.0.0", 80, True)