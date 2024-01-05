var foodlist = {}

const addToList = (food, id) => {
    if (foodlist[id] == undefined) {
        foodlist[id] = {'name': food.textContent, 'price': 0, 'amount': 1}
    } else {
        foodlist[id]['amount'] += 1; // add up to 1
    }
    // update
    updateList();
}

const updateList = () => {
    const checkout_list = document.querySelector("#checkout-list");
    checkout_list.innerHTML = "";
    for (let i in foodlist) {
        checkout_list.innerHTML += 
        `<div class="item"> x${foodlist[i]["amount"]} ${foodlist[i]["name"]}</div>`;
    }
}