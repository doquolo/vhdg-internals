import json

with open("data/foodlist.json", "w") as file:
    data = {}
    counter = 0
    while True:
        counter += 1
        dish = input("Nhập tên món: ")
        if (dish == "c"): break
        price = input("Nhập giá tiền: ")
        data[counter] = {
            "name": dish, 
            "price": price
        }
    file.write(json.dumps(data))
    file.close()


        