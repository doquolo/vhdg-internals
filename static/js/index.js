var foodlist = {}

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
        <div class="item" onclick="addToList(this, ${i})" style="background-image: url('/assets?image=${i}.png')">${list[i]}</div>
        `;
    }
}

const addToList = (food, id) => {
    if (foodlist[id] == undefined) {
        foodlist[id] = {'name': food.textContent, 'price': 0, 'amount': 1}
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
    checkout_list.innerHTML = `<div class="item header">
    <div class="text">Món ăn</div>
    <div class="price">Đơn giá</div>
    <div class="price">Tổng</div>
</div>`;
    var total = 0;
    for (let i in foodlist) {
        const price = await (await fetch(`/price?id=${i}`)).json();
        const subtotal = Number(foodlist[i]["amount"]) * price;
        total += subtotal;

        checkout_list.innerHTML += 
        `
        <div class="item" onclick="substractFood(${i})">
            <div class="text"><p>x${foodlist[i]["amount"]}</p><p>${foodlist[i]["name"]}</p></div>
            <div class="price">${price}.000đ</div>
            <div class="price">${subtotal}.000đ</div>
        </div>
        `
    }
    checkout_list.innerHTML += 
        `
        <div class="item header">
        <div class="text">Tổng đơn</div>
        <div class="price">${total}.000đ</div>
    </div>
        `;
}