var foodlist = {}
var sum = 0

document.addEventListener("DOMContentLoaded", () => {
    initList();
});

// prevent zooming
document.addEventListener('gesturestart', function (e) {
    e.preventDefault();
});

document.ondblclick = function(e) {
    e.preventDefault();
}

async function initList() {
    const menu_list = document.querySelector("#menu-list");
    menu_list.innerHTML = "";

    const request = await fetch("/foodlist");
    const list = await request.json();
    for (let i in list) {
        menu_list.innerHTML += `
        <div class="item" onclick="addToList(this, ${i})" style="background-image: url('/assets?image=${i}.png')">
            <div>${list[i]}</div>
        </div>
        `;
    }
}

async function getPrice(id) {
    return await (await fetch(`/price?id=${id}`)).json()
}

async function addToList(food, id) {
    if (foodlist[id] == undefined) {
        foodlist[id] = {'name': food.textContent, 'price': await getPrice(id), 'amount': 1}
    } else {
        foodlist[id]['amount'] += 1; // add up to 1
    }
    // update
    updateList();
}

const substractFood = (id) => {
    if (foodlist[id]['amount'] <= 1) {
        delete foodlist[id];
    } else {
        foodlist[id]['amount'] -= 1;
    }
    //update
    updateList();
}

async function updateList() {
    const checkout_list = document.querySelector("#checkout-list");
    await prepareList(checkout_list);
}

async function updateReceipt() {
    const receipt_list = document.querySelector("#receipt")
    await prepareList(receipt_list);
    receipt_list.innerHTML = `
    <div class="item header" style="border: none">
        <div class="text" id="id">ID: <div>${Date.now()}</div></div>
    </div>
    ` 
    + receipt_list.innerHTML;
}

async function prepareList(list_object) {

    const formatter = new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND',
      
        minimumFractionDigits: 0, // (this suffices for whole numbers, but will print 2500.10 as $2,500.1)
        maximumFractionDigits: 0, // (causes 2500.99 to be printed as $2,501)
      });

    list_object.innerHTML = `<div class="item header">
    <div class="text">Món ăn</div>
    <div class="price">Đơn giá</div>
    <div class="price">Tổng</div>
</div>`;
    var total = 0;
    for (let i in foodlist) {
        const price = await (await fetch(`/price?id=${i}`)).json();
        const subtotal = Number(foodlist[i]["amount"]) * price;
        total += subtotal;

        list_object.innerHTML += 
        `
        <div class="item" onclick="substractFood(${i})">
            <div class="text"><p>x${foodlist[i]["amount"]}</p><p>${foodlist[i]["name"]}</p></div>
            <div class="price">${formatter.format(price*1000)}</div>
            <div class="price">${formatter.format(subtotal*1000)}</div>
        </div>
        `
    }
    list_object.innerHTML += 
        `
    <div class="item header">
        <div class="text">Tổng đơn</div>
        <div class="price" id="sum">${formatter.format(total*1000)}</div>
    </div>
        `;
    sum = total; // for later access
}

const hideCheckout = () => {
    document.querySelector("body > div.container.popup").style.display = "none"
}

const showCheckout = () => {
    if (JSON.stringify(foodlist) === "{}") {
        alert("Hoá đơn không được để trống !");
    } else {
        document.querySelector("body > div.container.popup").style.display = "flex"
        // clear out old transition data
        document.querySelector("#payment-info").innerHTML = "";
        updateReceipt();
    }
}

const handleCash = () => { 
    const id = document.querySelector("#id > div").textContent;
    fetch('/pay', {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({mode: "cash", id: id, data: foodlist})
    }).then(res => res.json())
    .then(res => console.log(res));

    alert("Đã lưu giao dịch tiền mặt !");
    location.reload();
}
const handleContactless = () => {
    const id = document.querySelector("#id > div").textContent;
    const beneficial_acc = {
        bank_bin: "970422", // techcombank
        acc_num: "0794574608"
    }
    const receipt_info = {
        id: id,
        type: "compact2",
        amount: sum*1000,
        acc_name: "THANH TOAN DO AN VHDG"
    }
    document.querySelector("#payment-info").innerHTML = `
    <form action="/contactlesspay" method="post" enctype="multipart/form-data">
        <img id="qrcode" src="https://img.vietqr.io/image/${beneficial_acc.bank_bin}-${beneficial_acc.acc_num}-${receipt_info.type}.jpg?amount=${receipt_info.amount}&addInfo=${receipt_info.id}&accountName=${receipt_info.acc_name}" alt="">
        <input type="file" name="file" accept="image/*">
        <br>
        <textarea name="json_data" id="json_data" style="display: none;">${JSON.stringify({mode: "contactless", id: id, data: foodlist})}</textarea>
        <br>
        <input type="submit" value="Tải lên" onclick="this.form.submit(); alert('Đã lưu giao dịch chuyển khoản!'); location.redirect('/');">
    </form>
    `
}