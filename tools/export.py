import openpyxl
import json

with open("08012024.json", "r", encoding="utf-8") as file:
    data = json.loads(file.read())


print(data)

